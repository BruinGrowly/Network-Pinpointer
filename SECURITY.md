# Security Guidelines for Network Pinpointer

## Default Passwords in Docker Compose

⚠️ **IMPORTANT**: The `docker-compose.yml` file contains default passwords for development purposes. These **MUST** be changed before deploying to production.

### Default Credentials

The following services use default passwords that should be changed:

1. **InfluxDB**
   - Default password: `changeme123`
   - Environment variable: `INFLUXDB_PASSWORD`
   - Default token: `changeme`
   - Environment variable: `INFLUXDB_TOKEN`

2. **PostgreSQL**
   - Default password: `changeme123`
   - Environment variable: `POSTGRES_PASSWORD`

3. **Redis**
   - Default password: `changeme123`
   - Environment variable: `REDIS_PASSWORD`

4. **Grafana**
   - Default admin password: `admin123`
   - Environment variable: `GRAFANA_PASSWORD`

### Production Deployment

Before deploying to production:

1. **Generate strong passwords**:
   ```bash
   # Generate secure random passwords
   openssl rand -hex 32  # For InfluxDB token
   openssl rand -base64 24  # For passwords
   ```

2. **Use environment variables**:
   Create a `.env` file (and add it to `.gitignore`):
   ```bash
   INFLUXDB_TOKEN=$(openssl rand -hex 32)
   INFLUXDB_PASSWORD=$(openssl rand -base64 24)
   POSTGRES_PASSWORD=$(openssl rand -base64 24)
   REDIS_PASSWORD=$(openssl rand -base64 24)
   GRAFANA_PASSWORD=$(openssl rand -base64 24)
   ```

3. **Update docker-compose.yml**:
   The compose file already uses environment variables with defaults. In production, ensure these are set via:
   - `.env` file (not committed to git)
   - Environment variables in your deployment system
   - Secrets management system (e.g., Kubernetes secrets, Docker secrets)

4. **Network Security**:
   - Restrict access to database ports (5432, 6379, 8086) to internal networks only
   - Use firewall rules to limit access
   - Consider using Docker networks to isolate services

5. **API Security**:
   - Enable authentication on the API server
   - Use HTTPS/TLS for API endpoints
   - Implement rate limiting
   - Add API key authentication for production use

## Best Practices

1. **Never commit secrets to version control**
   - Use `.gitignore` for `.env` files
   - Use secrets management tools for production

2. **Rotate credentials regularly**
   - Set up a schedule for password rotation
   - Document credential locations

3. **Monitor access**
   - Enable logging for database access
   - Monitor for unauthorized access attempts

4. **Keep dependencies updated**
   - Regularly update Docker images
   - Update Python packages for security patches

5. **Network isolation**
   - Use Docker networks to isolate services
   - Restrict external access to sensitive services

## Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:
- Do not open public issues
- Contact the maintainers directly
- Allow time for fixes before public disclosure
