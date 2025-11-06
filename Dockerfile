# Network Pinpointer - Production Docker Image
FROM python:3.11-slim

LABEL maintainer="Network Pinpointer Contributors"
LABEL description="Semantic network diagnostic tool using LJPW framework"
LABEL version="1.0.0"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tcpdump \
    net-tools \
    iputils-ping \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
    influxdb-client \
    prometheus-client \
    redis \
    psycopg2-binary \
    fastapi \
    uvicorn \
    python-multipart

# Copy application code
COPY network_pinpointer/ ./network_pinpointer/
COPY pinpoint ./pinpoint
COPY test_semantic_imbuing.py ./

# Create necessary directories
RUN mkdir -p /app/config /app/data /app/captures /app/logs

# Make pinpoint executable
RUN chmod +x ./pinpoint

# Create non-root user for security
RUN useradd -m -u 1000 netpin && \
    chown -R netpin:netpin /app

# Switch to non-root user
USER netpin

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose API port
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LOG_LEVEL=info

# Start application
CMD ["python", "-m", "network_pinpointer.api_server"]
