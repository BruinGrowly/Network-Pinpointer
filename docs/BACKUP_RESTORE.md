# Backup and Restore Procedures

**Network-Pinpointer Backup & Restore Guide**

This guide covers backing up and restoring all data, configurations, and state for Network-Pinpointer deployments.

---

## Table of Contents

1. [Overview](#overview)
2. [What to Back Up](#what-to-back-up)
3. [Automated Backup](#automated-backup)
4. [Manual Backup](#manual-backup)
5. [Restore Procedures](#restore-procedures)
6. [Disaster Recovery](#disaster-recovery)
7. [Backup Testing](#backup-testing)
8. [Cloud Backup](#cloud-backup)

---

## Overview

### Backup Strategy

Network-Pinpointer uses a **3-2-1 backup strategy**:
- **3** copies of data (production + 2 backups)
- **2** different storage types (disk + cloud)
- **1** off-site backup

### Backup Components

```
┌─────────────────────────────────────────────────────┐
│              What Gets Backed Up                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  1. Configuration Files                              │
│     • .env                                           │
│     • ~/.network-pinpointer/config.yaml             │
│     • docker-compose.yml (if modified)              │
│                                                      │
│  2. Database Data                                    │
│     • InfluxDB (LJPW time-series)                   │
│     • PostgreSQL (flow records)                     │
│     • Redis (cache - optional)                      │
│                                                      │
│  3. Application Data                                 │
│     • History files (.jsonl)                        │
│     • State files                                   │
│     • Baselines                                     │
│                                                      │
│  4. Grafana                                         │
│     • Dashboards (JSON)                             │
│     • Settings                                      │
│     • Users                                         │
│                                                      │
│  5. SSL Certificates (if applicable)                │
│     • cert.pem                                      │
│     • key.pem                                       │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## What to Back Up

### Critical (Daily Backups)

1. **InfluxDB Data** - LJPW coordinates and metrics
   - Location: Docker volume `influxdb-data`
   - Size: ~100MB-10GB depending on retention
   - Importance: ⚠️ CRITICAL - Contains all time-series data

2. **PostgreSQL Data** - Flow records and analysis
   - Location: Docker volume `postgres-data`
   - Size: ~50MB-5GB depending on traffic
   - Importance: ⚠️ CRITICAL - Contains historical flows

3. **Configuration Files**
   - `.env` - Environment variables and secrets
   - `~/.network-pinpointer/config.yaml` - User configuration
   - Importance: ⚠️ CRITICAL - Cannot run without these

### Important (Weekly Backups)

4. **Application State**
   - `~/.network-pinpointer/history.jsonl` - Command history
   - `~/.network-pinpointer/state.json` - Application state
   - Importance: 🟡 IMPORTANT - Useful for continuity

5. **Grafana Dashboards**
   - Docker volume `grafana-data`
   - Custom dashboards and settings
   - Importance: 🟡 IMPORTANT - Can be recreated but time-consuming

### Optional (Monthly Backups)

6. **Redis Cache**
   - Docker volume `redis-data`
   - Importance: 🟢 OPTIONAL - Regenerates automatically

7. **Prometheus Data**
   - Docker volume `prometheus-data`
   - Importance: 🟢 OPTIONAL - Short retention, can be rebuilt

---

## Automated Backup

### Setup Automated Daily Backups

**1. Create backup script:**

```bash
sudo nano /usr/local/bin/netpin-backup.sh
```

**Paste this script:**

```bash
#!/bin/bash
#
# Network Pinpointer Automated Backup Script
#
# Usage: ./netpin-backup.sh [destination]
#

set -e  # Exit on error

# Configuration
BACKUP_ROOT="${1:-/backup/network-pinpointer}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="${BACKUP_ROOT}/${TIMESTAMP}"
RETENTION_DAYS=30
LOG_FILE="${BACKUP_ROOT}/backup.log"

# Docker Compose location
COMPOSE_DIR="/path/to/Network-Pinpointer"  # UPDATE THIS

# Create backup directory
mkdir -p "${BACKUP_DIR}"
mkdir -p "${BACKUP_ROOT}/logs"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "${LOG_FILE}"
}

log "=== Starting Network Pinpointer Backup ==="
log "Backup destination: ${BACKUP_DIR}"

# 1. Backup Configuration Files
log "Backing up configuration files..."
mkdir -p "${BACKUP_DIR}/config"

# .env file (contains secrets - secure it!)
if [ -f "${COMPOSE_DIR}/.env" ]; then
    cp "${COMPOSE_DIR}/.env" "${BACKUP_DIR}/config/.env"
    chmod 600 "${BACKUP_DIR}/config/.env"
    log "✓ Backed up .env"
fi

# User config
if [ -f "$HOME/.network-pinpointer/config.yaml" ]; then
    cp "$HOME/.network-pinpointer/config.yaml" "${BACKUP_DIR}/config/config.yaml"
    log "✓ Backed up user config"
fi

# Docker compose (if modified)
if [ -f "${COMPOSE_DIR}/docker-compose.yml" ]; then
    cp "${COMPOSE_DIR}/docker-compose.yml" "${BACKUP_DIR}/config/docker-compose.yml"
    log "✓ Backed up docker-compose.yml"
fi

# 2. Backup InfluxDB
log "Backing up InfluxDB..."
mkdir -p "${BACKUP_DIR}/influxdb"

docker exec netpin-influxdb influx backup /tmp/influxdb-backup -t "${INFLUXDB_TOKEN}" || true
docker cp netpin-influxdb:/tmp/influxdb-backup "${BACKUP_DIR}/influxdb/"
docker exec netpin-influxdb rm -rf /tmp/influxdb-backup

if [ -d "${BACKUP_DIR}/influxdb/influxdb-backup" ]; then
    log "✓ Backed up InfluxDB ($(du -sh ${BACKUP_DIR}/influxdb | cut -f1))"
else
    log "✗ InfluxDB backup failed"
fi

# 3. Backup PostgreSQL
log "Backing up PostgreSQL..."
mkdir -p "${BACKUP_DIR}/postgresql"

docker exec netpin-postgres pg_dump -U netpin network_pinpointer | gzip > "${BACKUP_DIR}/postgresql/dump.sql.gz"

if [ -f "${BACKUP_DIR}/postgresql/dump.sql.gz" ]; then
    log "✓ Backed up PostgreSQL ($(du -sh ${BACKUP_DIR}/postgresql/dump.sql.gz | cut -f1))"
else
    log "✗ PostgreSQL backup failed"
fi

# 4. Backup Grafana
log "Backing up Grafana..."
mkdir -p "${BACKUP_DIR}/grafana"

# Export Grafana dashboards via API
GRAFANA_URL="http://localhost:3000"
GRAFANA_USER="${GRAFANA_USER:-admin}"
GRAFANA_PASSWORD="${GRAFANA_PASSWORD:-admin123}"

curl -s -u "${GRAFANA_USER}:${GRAFANA_PASSWORD}" \
    "${GRAFANA_URL}/api/search?type=dash-db" | \
    jq -r '.[] | .uid' | \
while read -r uid; do
    curl -s -u "${GRAFANA_USER}:${GRAFANA_PASSWORD}" \
        "${GRAFANA_URL}/api/dashboards/uid/${uid}" | \
        jq '.dashboard' > "${BACKUP_DIR}/grafana/${uid}.json"
done

log "✓ Backed up Grafana dashboards"

# 5. Backup Application State
log "Backing up application state..."
mkdir -p "${BACKUP_DIR}/state"

if [ -f "$HOME/.network-pinpointer/history.jsonl" ]; then
    cp "$HOME/.network-pinpointer/history.jsonl" "${BACKUP_DIR}/state/"
    log "✓ Backed up history"
fi

if [ -f "$HOME/.network-pinpointer/state.json" ]; then
    cp "$HOME/.network-pinpointer/state.json" "${BACKUP_DIR}/state/"
    log "✓ Backed up state"
fi

# 6. Create backup manifest
log "Creating backup manifest..."
cat > "${BACKUP_DIR}/MANIFEST.txt" << EOF
Network Pinpointer Backup
=========================
Date: $(date)
Hostname: $(hostname)
Version: 1.0.1

Contents:
- Configuration files: ${BACKUP_DIR}/config/
- InfluxDB data: ${BACKUP_DIR}/influxdb/
- PostgreSQL data: ${BACKUP_DIR}/postgresql/
- Grafana dashboards: ${BACKUP_DIR}/grafana/
- Application state: ${BACKUP_DIR}/state/

Sizes:
$(du -sh ${BACKUP_DIR}/*)

Total Size: $(du -sh ${BACKUP_DIR} | cut -f1)
EOF

log "✓ Created manifest"

# 7. Create compressed archive
log "Creating compressed archive..."
cd "${BACKUP_ROOT}"
tar -czf "${TIMESTAMP}.tar.gz" "${TIMESTAMP}/" 2>/dev/null || true

if [ -f "${TIMESTAMP}.tar.gz" ]; then
    ARCHIVE_SIZE=$(du -sh "${TIMESTAMP}.tar.gz" | cut -f1)
    log "✓ Created archive: ${TIMESTAMP}.tar.gz (${ARCHIVE_SIZE})"
    
    # Remove uncompressed directory
    rm -rf "${TIMESTAMP}"
else
    log "✗ Archive creation failed, keeping uncompressed backup"
fi

# 8. Clean up old backups (retention policy)
log "Cleaning up old backups (retention: ${RETENTION_DAYS} days)..."
find "${BACKUP_ROOT}" -name "*.tar.gz" -mtime +${RETENTION_DAYS} -delete
find "${BACKUP_ROOT}" -maxdepth 1 -type d -mtime +${RETENTION_DAYS} -exec rm -rf {} \; 2>/dev/null || true

# 9. Backup summary
log "=== Backup Complete ==="
log "Location: ${BACKUP_ROOT}"
log "Recent backups:"
ls -lh "${BACKUP_ROOT}"/*.tar.gz 2>/dev/null | tail -5 | while read line; do log "  $line"; done

# 10. Verify backup integrity
log "Verifying backup integrity..."
if tar -tzf "${BACKUP_ROOT}/${TIMESTAMP}.tar.gz" >/dev/null 2>&1; then
    log "✓ Backup archive is valid"
else
    log "✗ WARNING: Backup archive may be corrupted!"
    exit 1
fi

log "=== Backup Script Completed Successfully ==="
```

**2. Make script executable:**

```bash
sudo chmod +x /usr/local/bin/netpin-backup.sh
```

**3. Configure environment variables:**

Edit the script and set:
- `COMPOSE_DIR` - Path to your Network-Pinpointer directory
- `INFLUXDB_TOKEN` - Your InfluxDB token from .env
- `GRAFANA_USER/PASSWORD` - Your Grafana credentials

**4. Set up cron job for daily backups:**

```bash
sudo crontab -e
```

Add this line for daily backup at 2 AM:

```cron
0 2 * * * /usr/local/bin/netpin-backup.sh /backup/network-pinpointer >> /backup/network-pinpointer/logs/cron.log 2>&1
```

**5. Test the backup:**

```bash
sudo /usr/local/bin/netpin-backup.sh /tmp/test-backup
```

Check `/tmp/test-backup/` for the backup archive.

---

## Manual Backup

### Quick Manual Backup

```bash
#!/bin/bash
# Quick manual backup script

BACKUP_DIR="netpin-backup-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "Creating manual backup in $BACKUP_DIR..."

# 1. Configuration
mkdir -p "$BACKUP_DIR/config"
cp .env "$BACKUP_DIR/config/" 2>/dev/null || echo "No .env found"
cp ~/.network-pinpointer/config.yaml "$BACKUP_DIR/config/" 2>/dev/null || echo "No config.yaml found"

# 2. InfluxDB
echo "Backing up InfluxDB..."
docker exec netpin-influxdb influx backup /tmp/backup -t "$INFLUXDB_TOKEN"
docker cp netpin-influxdb:/tmp/backup "$BACKUP_DIR/influxdb"
docker exec netpin-influxdb rm -rf /tmp/backup

# 3. PostgreSQL
echo "Backing up PostgreSQL..."
docker exec netpin-postgres pg_dump -U netpin network_pinpointer | gzip > "$BACKUP_DIR/postgres.sql.gz"

# 4. Compress
echo "Compressing..."
tar -czf "${BACKUP_DIR}.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo "✓ Backup complete: ${BACKUP_DIR}.tar.gz"
echo "  Size: $(du -sh ${BACKUP_DIR}.tar.gz | cut -f1)"
```

### Individual Component Backups

**Backup only configuration:**
```bash
tar -czf config-backup-$(date +%Y%m%d).tar.gz .env ~/.network-pinpointer/
```

**Backup only InfluxDB:**
```bash
docker exec netpin-influxdb influx backup /tmp/influx-backup -t "$INFLUXDB_TOKEN"
docker cp netpin-influxdb:/tmp/influx-backup ./influxdb-backup-$(date +%Y%m%d)
```

**Backup only PostgreSQL:**
```bash
docker exec netpin-postgres pg_dump -U netpin network_pinpointer | gzip > postgres-backup-$(date +%Y%m%d).sql.gz
```

**Backup only Grafana:**
```bash
docker exec netpin-grafana tar -czf /tmp/grafana-backup.tar.gz /var/lib/grafana
docker cp netpin-grafana:/tmp/grafana-backup.tar.gz ./grafana-backup-$(date +%Y%m%d).tar.gz
```

---

## Restore Procedures

### Full System Restore

**1. Extract backup:**
```bash
tar -xzf netpin-backup-YYYYMMDD_HHMMSS.tar.gz
cd netpin-backup-YYYYMMDD_HHMMSS/
```

**2. Stop all services:**
```bash
docker-compose down
```

**3. Restore configuration:**
```bash
cp config/.env /path/to/Network-Pinpointer/.env
cp config/config.yaml ~/.network-pinpointer/config.yaml
```

**4. Restore InfluxDB:**
```bash
# Start only InfluxDB
docker-compose up -d influxdb

# Wait for it to start
sleep 10

# Copy backup into container
docker cp influxdb/influxdb-backup netpin-influxdb:/tmp/

# Restore
docker exec netpin-influxdb influx restore /tmp/influxdb-backup -t "$INFLUXDB_TOKEN"

# Verify
docker exec netpin-influxdb influx query 'from(bucket:"semantic_data") |> range(start: -1h) |> limit(n:1)'
```

**5. Restore PostgreSQL:**
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Wait for it to start
sleep 10

# Restore
gunzip < postgresql/dump.sql.gz | docker exec -i netpin-postgres psql -U netpin network_pinpointer

# Verify
docker exec netpin-postgres psql -U netpin -d network_pinpointer -c "SELECT COUNT(*) FROM flows;"
```

**6. Restore Grafana:**
```bash
# Start Grafana
docker-compose up -d grafana

# Wait for it to start
sleep 10

# Import dashboards via API
for dashboard in grafana/*.json; do
    curl -X POST http://admin:admin123@localhost:3000/api/dashboards/db \
        -H "Content-Type: application/json" \
        -d @"$dashboard"
done
```

**7. Restore application state:**
```bash
cp state/history.jsonl ~/.network-pinpointer/
cp state/state.json ~/.network-pinpointer/
```

**8. Start all services:**
```bash
docker-compose up -d
```

**9. Verify restoration:**
```bash
# Check all services
docker-compose ps

# Test API
curl http://localhost:8080/health

# Check Grafana
curl http://localhost:3000/api/health

# Test CLI
SKIP_FIRST_RUN=1 ./pinpoint health
```

### Partial Restore Examples

**Restore only configuration:**
```bash
tar -xzf config-backup-*.tar.gz
cp .env /path/to/Network-Pinpointer/
cp .network-pinpointer/config.yaml ~/.network-pinpointer/
```

**Restore only database:**
```bash
# InfluxDB only
docker cp influxdb-backup-* netpin-influxdb:/tmp/restore
docker exec netpin-influxdb influx restore /tmp/restore -t "$INFLUXDB_TOKEN"

# PostgreSQL only
gunzip < postgres-backup-*.sql.gz | docker exec -i netpin-postgres psql -U netpin network_pinpointer
```

---

## Disaster Recovery

### Complete System Loss

**Recovery Time Objective (RTO): 2-4 hours**  
**Recovery Point Objective (RPO): 24 hours** (with daily backups)

**Disaster Recovery Steps:**

1. **Provision new server** (same or similar specs)
   ```bash
   # Install Docker & Docker Compose
   curl -fsSL https://get.docker.com | sh
   ```

2. **Clone repository**
   ```bash
   git clone https://github.com/YourOrg/Network-Pinpointer.git
   cd Network-Pinpointer
   ```

3. **Retrieve backup** (from off-site location)
   ```bash
   # From S3
   aws s3 cp s3://your-bucket/netpin-backup-latest.tar.gz .

   # Or from backup server
   scp backup-server:/backups/netpin-backup-latest.tar.gz .
   ```

4. **Extract and restore** (follow Full System Restore above)

5. **Update DNS/networking** (if applicable)
   - Point domain to new server
   - Update firewall rules
   - Configure SSL certificates

6. **Verify and test**
   - Run full diagnostic suite
   - Check all dashboards
   - Test API endpoints
   - Validate data integrity

### Data Corruption Recovery

**Scenario: Database corruption detected**

1. **Identify corruption:**
   ```bash
   docker logs netpin-influxdb | grep -i error
   docker exec netpin-postgres pg_isready
   ```

2. **Stop affected service:**
   ```bash
   docker-compose stop influxdb  # or postgres
   ```

3. **Restore from most recent valid backup**
   ```bash
   # Follow restore procedures above for affected component
   ```

4. **Validate restoration:**
   ```bash
   # Query for recent data
   # Check data consistency
   ```

5. **Resume operations:**
   ```bash
   docker-compose up -d
   ```

---

## Backup Testing

### Monthly Backup Verification

**Test restore on a separate system:**

```bash
#!/bin/bash
# backup-test.sh - Test backup restoration

echo "Testing backup restoration..."

# 1. Create test environment
mkdir -p /tmp/restore-test
cd /tmp/restore-test

# 2. Copy latest backup
cp /backup/network-pinpointer/$(ls -t /backup/network-pinpointer/*.tar.gz | head -1) .

# 3. Extract
tar -xzf *.tar.gz

# 4. Test each component
echo "Testing InfluxDB backup..."
# Attempt to read backup manifest
tar -tzf */influxdb/*.tar.gz | head -10

echo "Testing PostgreSQL backup..."
# Verify SQL dump can be read
gunzip -c */postgresql/*.sql.gz | head -20

echo "Testing config files..."
# Verify config files are readable
cat */config/.env | grep -v PASSWORD | grep -v SECRET | grep -v TOKEN

# 5. Cleanup
cd /
rm -rf /tmp/restore-test

echo "✓ Backup test complete"
```

Run this monthly:
```bash
0 3 1 * * /usr/local/bin/backup-test.sh >> /var/log/backup-test.log 2>&1
```

---

## Cloud Backup

### AWS S3 Integration

**1. Install AWS CLI:**
```bash
pip install awscli
aws configure
```

**2. Sync backups to S3:**
```bash
#!/bin/bash
# sync-to-s3.sh

BACKUP_DIR="/backup/network-pinpointer"
S3_BUCKET="s3://your-backup-bucket/network-pinpointer"

# Sync to S3 (encrypted)
aws s3 sync "${BACKUP_DIR}" "${S3_BUCKET}" \
    --exclude "logs/*" \
    --storage-class STANDARD_IA \
    --sse AES256

# Set lifecycle policy (optional)
aws s3api put-bucket-lifecycle-configuration \
    --bucket your-backup-bucket \
    --lifecycle-configuration file://lifecycle.json
```

**lifecycle.json:**
```json
{
  "Rules": [
    {
      "Id": "ArchiveOldBackups",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "GLACIER"
        },
        {
          "Days": 90,
          "StorageClass": "DEEP_ARCHIVE"
        }
      ],
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

**3. Automate with cron:**
```cron
0 4 * * * /usr/local/bin/sync-to-s3.sh >> /var/log/s3-sync.log 2>&1
```

### Google Cloud Storage

```bash
# Install gcloud
# Configure: gcloud init

# Sync to GCS
gsutil -m rsync -r /backup/network-pinpointer gs://your-backup-bucket/network-pinpointer
```

### Azure Blob Storage

```bash
# Install Azure CLI
# Configure: az login

# Sync to Azure
az storage blob upload-batch \
    --destination network-pinpointer-backups \
    --source /backup/network-pinpointer \
    --account-name yourstorageaccount
```

---

## Backup Checklist

### Daily Tasks (Automated)
- [ ] InfluxDB backup runs successfully
- [ ] PostgreSQL backup runs successfully
- [ ] Configuration backed up
- [ ] Backup log checked for errors

### Weekly Tasks
- [ ] Review backup sizes (growth trends)
- [ ] Check backup retention policy
- [ ] Verify backup script execution
- [ ] Test restore of one component

### Monthly Tasks
- [ ] Full backup restoration test
- [ ] Review and update backup scripts
- [ ] Verify off-site backups
- [ ] Update disaster recovery documentation

### Quarterly Tasks
- [ ] Full disaster recovery drill
- [ ] Review backup strategy
- [ ] Audit backup security
- [ ] Update backup retention policy

---

## Troubleshooting

### Backup Fails

**InfluxDB backup fails:**
```bash
# Check InfluxDB is running
docker ps | grep influxdb

# Check logs
docker logs netpin-influxdb

# Verify token
docker exec netpin-influxdb influx ping
```

**PostgreSQL backup fails:**
```bash
# Check PostgreSQL is running
docker exec netpin-postgres pg_isready

# Test connection
docker exec netpin-postgres psql -U netpin -d network_pinpointer -c "SELECT 1"

# Check disk space
docker exec netpin-postgres df -h
```

### Restore Fails

**Check backup integrity:**
```bash
tar -tzf backup.tar.gz | head
```

**Verify backup contents:**
```bash
tar -xzf backup.tar.gz
cat */MANIFEST.txt
```

**Check logs:**
```bash
docker-compose logs -f
```

---

## Security Best Practices

### Backup Security

1. **Encrypt backups:**
   ```bash
   # Encrypt with GPG
   tar -czf - backup/ | gpg -c > backup-encrypted.tar.gz.gpg
   
   # Decrypt
   gpg -d backup-encrypted.tar.gz.gpg | tar -xz
   ```

2. **Secure .env file:**
   ```bash
   chmod 600 /backup/network-pinpointer/*/config/.env
   ```

3. **Use separate backup user:**
   ```bash
   useradd -m -s /bin/bash backupuser
   chown backupuser:backupuser /backup/network-pinpointer
   ```

4. **Audit backup access:**
   ```bash
   # Log all access to backups
   auditctl -w /backup/network-pinpointer -p rwa -k netpin_backup
   ```

---

## Summary

### Backup Schedule

| Component | Frequency | Retention | Method |
|-----------|-----------|-----------|--------|
| Configuration | Daily | 90 days | File copy |
| InfluxDB | Daily | 30 days | influx backup |
| PostgreSQL | Daily | 30 days | pg_dump |
| Grafana | Weekly | 30 days | API export |
| Application State | Daily | 90 days | File copy |
| Off-site Sync | Daily | 365 days | S3/GCS/Azure |

### Storage Requirements

| Backup Type | Typical Size | Notes |
|-------------|--------------|-------|
| Configuration | < 1 MB | Very small |
| InfluxDB | 100 MB - 10 GB | Depends on retention |
| PostgreSQL | 50 MB - 5 GB | Depends on traffic |
| Grafana | 10-50 MB | Dashboards only |
| Full Backup (compressed) | 200 MB - 15 GB | All components |

### Quick Reference

**Backup:**
```bash
/usr/local/bin/netpin-backup.sh /backup/network-pinpointer
```

**Restore:**
```bash
tar -xzf backup.tar.gz
docker-compose down
# Restore components (see sections above)
docker-compose up -d
```

**Test:**
```bash
/usr/local/bin/backup-test.sh
```

---

**Remember:** Backups are only useful if you can restore from them. **Test regularly!**
