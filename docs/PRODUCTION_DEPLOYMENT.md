# Network Pinpointer - Production Deployment Guide

Complete guide to deploying Network Pinpointer in production with full monitoring stack.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Accessing Services](#accessing-services)
- [First-Time Setup](#first-time-setup)
- [Monitoring & Dashboards](#monitoring--dashboards)
- [Troubleshooting](#troubleshooting)
- [Scaling](#scaling)
- [Security](#security)

---

## Overview

Network Pinpointer production deployment includes:

- **Network Pinpointer**: Semantic network analysis engine
- **InfluxDB**: Time-series storage for LJPW coordinates
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Interactive dashboards
- **PostgreSQL**: Long-term flow storage
- **Redis**: Caching and real-time data
- **Nginx**: Reverse proxy (optional)

**Total resource requirements:**
- CPU: 4+ cores recommended
- RAM: 8GB minimum, 16GB recommended
- Disk: 50GB+ for logs and time-series data
- Network: Full packet capture requires promiscuous mode

---

## Quick Start

### 1. Prerequisites

```bash
# Docker and Docker Compose
docker --version  # Should be 20.10+
docker-compose --version  # Should be 1.29+ or 2.x

# Git
git clone https://github.com/YourOrg/Network-Pinpointer.git
cd Network-Pinpointer
```

### 2. Deploy Everything

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f network-pinpointer
```

### 3. Access Services

- **API**: http://localhost:8080
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

### 4. First Analysis

```bash
# CLI (if installed locally)
./pinpoint quick-check 8.8.8.8

# Or via API
curl http://localhost:8080/quick-check?target=8.8.8.8
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User/Browser                            │
└───────────────┬─────────────────────────────────────────────┘
                │
        ┌───────▼────────┐
        │  Nginx :80     │  (Optional reverse proxy)
        └───────┬────────┘
                │
    ┌───────────┼───────────────────┐
    │           │                   │
┌───▼───┐  ┌───▼─────┐      ┌─────▼────┐
│ API   │  │ Grafana │      │Prometheus│
│ :8080 │  │  :3000  │      │  :9090   │
└───┬───┘  └───┬─────┘      └────┬─────┘
    │          │                  │
    │      ┌───▼──────────────────▼───┐
    │      │   Network Pinpointer     │
    │      │   (Analysis Engine)      │
    │      └───┬──────────────────┬───┘
    │          │                  │
┌───▼──────┐ ┌▼────────┐    ┌───▼──────┐
│InfluxDB  │ │PostgreSQL│   │  Redis   │
│Time-series│ │Long-term │   │ Cache    │
└──────────┘ └──────────┘    └──────────┘
```

**Data Flow:**

1. **Analysis Request** → API Server
2. **Packet Capture** → Semantic Analysis → LJPW Calculation
3. **Storage**:
   - Real-time LJPW → InfluxDB
   - Flow metadata → PostgreSQL
   - Cache/state → Redis
4. **Metrics** → Prometheus → Grafana
5. **Visualization** → Grafana Dashboards

---

## Installation

### Option 1: Docker Compose (Recommended)

**Step 1: Clone repository**

```bash
git clone https://github.com/YourOrg/Network-Pinpointer.git
cd Network-Pinpointer
```

**Step 2: Configure environment**

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration
nano .env

# IMPORTANT: Change these default passwords in production:
# - INFLUXDB_TOKEN
# - POSTGRES_PASSWORD
# - REDIS_PASSWORD
# - GRAFANA_PASSWORD
# - JWT_SECRET
```

**Security Note**: The `.env.example` file includes 250+ configuration options with comprehensive security notes. Review all settings before deploying to production.

**Step 3: Start services**

```bash
# Pull images
docker-compose pull

# Start in background
docker-compose up -d

# View startup logs
docker-compose logs -f
```

**Step 4: Verify health**

```bash
# Check all services running
docker-compose ps

# Check API health
curl http://localhost:8080/health
```

### Option 2: CLI Installation (Local)

For local CLI usage without Docker:

**Choose your installation tier:**

See the main README for detailed installation options. Quick summary:

**Minimal (Core CLI only)**:
```bash
# Core functionality only
pip install pyyaml

# Make CLI executable
chmod +x pinpoint

# Skip first-run wizard for automation
SKIP_FIRST_RUN=1 ./pinpoint version
```

**With Packet Capture**:
```bash
# Add real packet capture
pip install pyyaml scapy

# Run setup wizard
./pinpoint setup
```

**Full Installation**:
```bash
# Install all dependencies
pip install -r requirements.txt

# First analysis
./pinpoint quick-check 8.8.8.8
```

**Environment Variables**:
```bash
# Skip first-run wizard (useful for automation/CI)
export SKIP_FIRST_RUN=1

# Run tests in offline mode (useful for CI/CD)
export OFFLINE_MODE=1
```

---

## Configuration

### Environment Variables (.env)

A complete `.env.example` template is provided with 250+ configuration options. Copy and customize it:

```bash
cp .env.example .env
nano .env
```

**Key settings to customize:**

```bash
# ============================================================================
# CRITICAL: Change these before production deployment!
# ============================================================================

# InfluxDB
INFLUXDB_TOKEN=changeme_generate_secure_token  # Generate: openssl rand -base64 32
INFLUXDB_PASSWORD=changeme123

# PostgreSQL
POSTGRES_PASSWORD=changeme123

# Redis
REDIS_PASSWORD=changeme123

# Grafana
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin123  # CHANGE THIS!

# Security
JWT_SECRET=changeme_generate_secure_random_string_here  # Generate: openssl rand -base64 32

# Network Pinpointer
NETWORK_TYPE=enterprise  # enterprise, datacenter, cloud, edge
LOG_LEVEL=info
ENABLE_API=true
API_PORT=8080

# Optional: Skip first-run wizard (for automation)
SKIP_FIRST_RUN=0  # Set to 1 to skip

# Optional: Alerting
SLACK_WEBHOOK=  # Your Slack webhook URL
ALERT_EMAIL=    # Email for alerts
```

**Complete configuration**: See `.env.example` for all 250+ options including:
- Database connections (InfluxDB, PostgreSQL, Redis)
- Monitoring (Grafana, Prometheus)
- Alerting (Slack, Email, PagerDuty)
- Security (Rate limiting, JWT, IP whitelist)
- LJPW baselines
- Packet capture settings
- Feature flags
- Backup configuration

### Network Pinpointer Config (YAML)

Create `~/.network-pinpointer/config.yaml`:

```yaml
network_type: enterprise

targets:
  gateway:
    host: 192.168.1.1
    description: Default gateway
    expected_love: 0.9
    expected_justice: 0.5
    expected_power: 0.7
    expected_wisdom: 0.8

  dns-server:
    host: 192.168.1.10
    description: Internal DNS
    expected_love: 0.85
    expected_wisdom: 0.95

baseline:
  auto_learn: true
  learning_period_hours: 24

monitoring:
  interval_seconds: 300
  enable_drift_detection: true
  drift_threshold: 0.15

alerts:
  slack_webhook: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
  enabled: true
  severity_threshold: warning
```

### Prometheus Alerts

Alerts are defined in `monitoring/rules/ljpw_rules.yml`:

- **LoveDimensionCritical**: Love < 0.3 (connectivity loss)
- **JusticeDimensionTooHigh**: Justice > 0.85 (over-restrictive)
- **PowerDimensionDegraded**: Power < 0.4 (performance issues)
- **SemanticAnomalySpike**: Anomalies > 10/min (security)

Edit to customize thresholds for your environment.

---

## Accessing Services

### API Server

**Base URL**: http://localhost:8080

**Endpoints:**

- `GET /` - Welcome page with documentation links
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /health` - Health check
- `GET /quick-check?target=8.8.8.8` - Fast connectivity check
- `POST /analyze` - Comprehensive analysis
- `GET /metrics` - Prometheus metrics

**Example API call:**

```bash
# Quick check
curl http://localhost:8080/quick-check?target=8.8.8.8

# Full analysis
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "target": "api.example.com",
    "network_type": "cloud",
    "timeout": 10
  }'
```

### Grafana Dashboards

**URL**: http://localhost:3000

**Default credentials**: `admin` / `admin` (change immediately!)

**Pre-installed dashboards:**

1. **LJPW Overview** (`/d/network-pinpointer-ljpw`)
   - Real-time LJPW gauges
   - Health score
   - Active alerts
   - Dimension trends

2. **Semantic Flows** (`/d/network-pinpointer-flows`)
   - Flow analysis
   - Intent distribution
   - Anomalous flows
   - Top destinations

**First-time setup:**

1. Login with admin/admin
2. Change password immediately
3. Navigate to "Dashboards" → "Network Pinpointer"
4. Pin your favorite dashboard

### Prometheus

**URL**: http://localhost:9090

**Useful queries:**

```promql
# Current LJPW dimensions
network_pinpointer_love
network_pinpointer_justice
network_pinpointer_power
network_pinpointer_wisdom

# Health score
ljpw:health_score

# Semantic anomaly rate
network:semantic_anomaly_rate

# Active alerts
ALERTS{alertstate="firing"}
```

### CLI

If installed locally:

```bash
# Interactive setup wizard (first run)
./pinpoint setup

# Quick health check
./pinpoint quick-check 8.8.8.8

# Comprehensive analysis
./pinpoint analyze gateway

# Continuous monitoring
./pinpoint watch gateway dns-server api-server

# View history
./pinpoint history gateway --hours 24 --dimension love

# Show patterns
./pinpoint patterns

# Compare before/after
./pinpoint diff before.json after.json

# Export report
./pinpoint export analysis.json --format html
```

---

## First-Time Setup

### Welcome Experience

Network Pinpointer includes a welcoming first-run experience following **LJPW UX principles**:

**Run the setup wizard:**

```bash
./pinpoint setup
```

**The wizard will:**

1. ✅ Explain LJPW dimensions
2. ✅ Ask about your network type (enterprise, cloud, etc.)
3. ✅ Help you add monitoring targets
4. ✅ Configure monitoring preferences
5. ✅ Save configuration
6. ✅ Offer to run first analysis

**What happens:**

```
👋 Welcome to Network Pinpointer!

Network Pinpointer helps you understand your network using the LJPW framework.

What is LJPW?

  💚 Love: Connectivity & Responsiveness
    Can you reach your targets? How fast?

  ⚖️  Justice: Policy & Boundaries
    What's allowed? What's blocked?

  ⚡ Power: Performance & Capacity
    How much throughput? Any congestion?

  🧠 Wisdom: Intelligence & Observability
    Can you discover services? Understand routing?

Let's get you set up in just a minute...

Would you like a quick guided setup? [Y/n]:
```

**After setup completes:**

- Configuration saved to `~/.network-pinpointer/config.yaml`
- Ready to run first analysis
- Suggestions for next steps

---

## Monitoring & Dashboards

### Setting Up Alerting

**1. Configure Slack notifications:**

Edit `~/.network-pinpointer/config.yaml`:

```yaml
alerts:
  slack_webhook: https://hooks.slack.com/services/T00/B00/XXX
  enabled: true
  severity_threshold: warning
```

**2. Configure email notifications:**

Edit `monitoring/alertmanager.yml` (create if not exists):

```yaml
global:
  smtp_smarthost: 'smtp.example.com:587'
  smtp_from: 'alerts@example.com'
  smtp_auth_username: 'alerts@example.com'
  smtp_auth_password: 'password'

route:
  receiver: 'email-notifications'

receivers:
  - name: 'email-notifications'
    email_configs:
      - to: 'ops@example.com'
```

### Creating Custom Dashboards

**Import dashboard JSON:**

1. Go to Grafana → Create → Import
2. Upload JSON from `grafana/provisioning/dashboards/json/`
3. Customize as needed

**Create new panel:**

```json
{
  "datasource": "InfluxDB-NetworkPinpointer",
  "targets": [
    {
      "query": "from(bucket: \"ljpw_metrics\") |> range(start: -1h) |> filter(fn: (r) => r._measurement == \"ljpw\") |> filter(fn: (r) => r._field == \"love\")"
    }
  ]
}
```

### Metrics to Monitor

**Key metrics:**

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `network_pinpointer_love` | Connectivity | < 0.4 (critical) |
| `network_pinpointer_justice` | Security policy | > 0.85 (warning) |
| `network_pinpointer_power` | Performance | < 0.4 (warning) |
| `network_pinpointer_wisdom` | Observability | < 0.4 (warning) |
| `network:semantic_anomaly_rate` | Anomalies/min | > 10 (critical) |
| `ljpw:health_score` | Overall health | < 0.5 (warning) |

---

## Troubleshooting

### Services Won't Start

**Check logs:**

```bash
docker-compose logs network-pinpointer
docker-compose logs influxdb
docker-compose logs grafana
```

**Common issues:**

1. **Port already in use:**
   ```bash
   # Check what's using port 8080
   lsof -i :8080

   # Change port in docker-compose.yml
   ports:
     - "8081:8080"  # Use 8081 instead
   ```

2. **Insufficient permissions:**
   ```bash
   # Network Pinpointer needs cap_net_raw for packet capture
   # Already configured in docker-compose.yml
   cap_add:
     - NET_ADMIN
     - NET_RAW
   ```

3. **Out of disk space:**
   ```bash
   # Check disk usage
   docker system df

   # Clean up old data
   docker system prune -a
   ```

### Grafana Dashboards Empty

**Check data sources:**

1. Go to Configuration → Data Sources
2. Verify InfluxDB connection: Test & Save
3. Verify Prometheus connection: Test & Save

**Check data is being written:**

```bash
# Query InfluxDB directly
docker-compose exec influxdb influx query 'from(bucket:"ljpw_metrics") |> range(start: -1h) |> limit(n:10)'
```

### No Metrics in Prometheus

**Check Prometheus targets:**

1. Go to http://localhost:9090/targets
2. Verify `network-pinpointer` target is UP
3. Check error messages

**Debug:**

```bash
# Check if metrics endpoint is working
curl http://localhost:8080/metrics

# Should see Prometheus format:
# network_pinpointer_love 0.85
# network_pinpointer_justice 0.60
# ...
```

### CLI Commands Fail

**Check configuration:**

```bash
# Show current config
./pinpoint config show

# Create example config
./pinpoint config create-example

# Re-run setup
./pinpoint setup
```

**Check Python dependencies:**

```bash
# Verify installation
pip list | grep -E 'scapy|influxdb|prometheus'

# Reinstall if needed
pip install -r requirements.txt
```

---

## Scaling

### Horizontal Scaling

**Option 1: Multiple analysis workers**

```yaml
# docker-compose.yml
services:
  network-pinpointer-worker-1:
    <<: *network-pinpointer-service
    environment:
      - WORKER_ID=1

  network-pinpointer-worker-2:
    <<: *network-pinpointer-service
    environment:
      - WORKER_ID=2
```

**Option 2: Kubernetes deployment**

See `k8s/` directory for Kubernetes manifests (coming soon).

### Database Scaling

**InfluxDB:**

```bash
# Enable clustering (InfluxDB Enterprise)
# Or use InfluxDB Cloud for managed scaling
```

**PostgreSQL:**

```yaml
# Add read replicas
services:
  postgres-primary:
    # ...

  postgres-replica:
    image: postgres:15
    environment:
      - POSTGRES_PRIMARY_HOST=postgres-primary
```

**Redis:**

```yaml
# Redis Sentinel for high availability
services:
  redis-master:
    # ...

  redis-replica:
    # ...

  redis-sentinel:
    # ...
```

### Resource Limits

**docker-compose.yml:**

```yaml
services:
  network-pinpointer:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

---

## Security

### Securing Services

**1. Change default passwords:**

```bash
# Grafana admin password
# Set in .env:
GRAFANA_ADMIN_PASSWORD=strong-password-here

# PostgreSQL password
POSTGRES_PASSWORD=strong-password-here

# InfluxDB token
INFLUXDB_TOKEN=$(openssl rand -hex 32)
```

**2. Enable HTTPS:**

Uncomment SSL configuration in `nginx/nginx.conf`:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    # ...
}
```

**3. Restrict network access:**

```yaml
# docker-compose.yml
services:
  postgres:
    ports:
      - "127.0.0.1:5432:5432"  # Only localhost

  prometheus:
    ports:
      - "127.0.0.1:9090:9090"  # Only localhost
```

**4. Enable firewall:**

```bash
# UFW (Ubuntu)
ufw allow 80/tcp
ufw allow 443/tcp
ufw deny 8080/tcp  # Block direct API access
ufw enable
```

### Data Security

**Encrypt sensitive data:**

```yaml
# config.yaml
security:
  mask_pii: true
  encrypt_flows: true
  retention_days: 90
```

**Backup configuration:**

```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf backup-$DATE.tar.gz \
  ~/.network-pinpointer/ \
  docker-compose.yml \
  .env
```

---

## Support

### Documentation

- **GitHub**: https://github.com/YourOrg/Network-Pinpointer
- **Docs**: https://docs.network-pinpointer.com
- **API Reference**: http://localhost:8080/docs

### Community

- **Issues**: https://github.com/YourOrg/Network-Pinpointer/issues
- **Discussions**: https://github.com/YourOrg/Network-Pinpointer/discussions

### Professional Support

For enterprise support, custom development, or consulting:
- Email: support@network-pinpointer.com

---

## Next Steps

After deployment:

1. ✅ Run setup wizard: `./pinpoint setup`
2. ✅ Configure monitoring targets
3. ✅ Set up alerting (Slack, email)
4. ✅ Create Grafana dashboards
5. ✅ Configure baseline learning
6. ✅ Schedule regular health checks
7. ✅ Document your network topology
8. ✅ Train team on LJPW framework

**Happy monitoring with LJPW! 📡💚⚖️⚡🧠**
