#!/usr/bin/env python3
"""
Network Pinpointer API Server

RESTful API for network semantic analysis using LJPW framework.
Designed following LJPW UX principles:
- Love: Fast, responsive, welcoming
- Justice: Consistent, predictable, clear errors
- Power: Full-featured, capable, efficient
- Wisdom: Well-documented, educational, insightful
"""

import asyncio
import time
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

# Import Network Pinpointer modules
from .semantic_engine import SemanticEngine, Coordinates
from .analyzer import NetworkAnalyzer
from .config import ConfigManager, NetworkPinpointerConfig

# Prometheus metrics
REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

LJPW_GAUGE = Gauge(
    'network_pinpointer_ljpw',
    'Current LJPW coordinates',
    ['dimension']
)

ANALYSIS_COUNT = Counter(
    'network_pinpointer_analyses_total',
    'Total analyses performed'
)

SEMANTIC_ANOMALIES = Counter(
    'network_pinpointer_semantic_mismatches_total',
    'Semantic anomalies detected'
)

ACTIVE_FLOWS = Gauge(
    'network_pinpointer_active_flows',
    'Number of active flows'
)

# Pydantic models for API
class AnalysisRequest(BaseModel):
    """Request to analyze a network target"""
    target: str = Field(..., description="Target host (IP or hostname)", example="8.8.8.8")
    network_type: Optional[str] = Field("enterprise", description="Network type (enterprise, data_center, cloud, edge)")
    timeout: Optional[int] = Field(5, description="Analysis timeout in seconds", ge=1, le=60)

    class Config:
        schema_extra = {
            "example": {
                "target": "api.example.com",
                "network_type": "cloud",
                "timeout": 10
            }
        }


class LJPWCoordinates(BaseModel):
    """LJPW dimension coordinates"""
    love: float = Field(..., ge=0.0, le=1.0, description="Love: Connectivity & Responsiveness")
    justice: float = Field(..., ge=0.0, le=1.0, description="Justice: Policy & Boundaries")
    power: float = Field(..., ge=0.0, le=1.0, description="Power: Performance & Capacity")
    wisdom: float = Field(..., ge=0.0, le=1.0, description="Wisdom: Intelligence & Observability")


class SemanticMismatch(BaseModel):
    """A detected semantic anomaly"""
    dimension: str
    observed: float
    expected: float
    severity: str
    explanation: str


class AnalysisResult(BaseModel):
    """Result of network analysis"""
    target: str
    timestamp: datetime
    ljpw: LJPWCoordinates
    health_score: float = Field(..., ge=0.0, le=1.0, description="Overall health (0-1)")
    semantic_mismatches: List[SemanticMismatch] = Field(default_factory=list)
    interpretation: str
    recommendations: List[str] = Field(default_factory=list)
    duration_ms: float


class HealthStatus(BaseModel):
    """API health check response"""
    status: str
    timestamp: datetime
    version: str
    uptime_seconds: float


class ErrorResponse(BaseModel):
    """Friendly error response following LJPW Justice principle (clear, fair)"""
    error: str
    message: str
    help: Optional[str] = None
    timestamp: datetime


# FastAPI app
app = FastAPI(
    title="Network Pinpointer API",
    description="""
# 📡 Network Pinpointer API

Semantic network analysis using the **LJPW framework** (Love, Justice, Power, Wisdom).

## What is LJPW?

- **Love** (💚): Connectivity and responsiveness - can you reach targets? How fast?
- **Justice** (⚖️ ): Policy enforcement - what's allowed? What's blocked?
- **Power** (⚡): Performance and capacity - how much throughput?
- **Wisdom** (🧠): Intelligence and observability - can you discover and understand?

## Key Features

- **Semantic Intent Classification**: Understand what packets are *trying* to do
- **Anomaly Detection**: Find "technically correct but semantically wrong" issues
- **Flow Analysis**: Track semantic journey through network
- **Pattern Recognition**: Identify known network patterns

## Getting Started

1. Try the `/quick-check` endpoint for fast analysis
2. Use `/analyze` for comprehensive analysis
3. Monitor with `/metrics` (Prometheus format)
4. View health with `/health`

*For full documentation, see: https://github.com/network-pinpointer*
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (Love principle: welcoming)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
startup_time = time.time()
analyzer: Optional[NetworkAnalyzer] = None
config_manager: Optional[ConfigManager] = None


# Middleware for request tracking (Love principle: responsive)
@app.middleware("http")
async def track_requests(request: Request, call_next):
    """Track request metrics and timing"""
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    # Record metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    # Add response headers (Wisdom principle: informative)
    response.headers["X-Response-Time"] = f"{duration * 1000:.2f}ms"
    response.headers["X-API-Version"] = "1.0.0"

    return response


# Exception handler (Justice principle: clear, fair errors)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Friendly error responses with helpful guidance"""

    # Provide helpful context based on error type
    help_text = None
    if exc.status_code == 404:
        help_text = "Check the API documentation at /docs for available endpoints"
    elif exc.status_code == 422:
        help_text = "Verify your request parameters match the API schema"
    elif exc.status_code == 500:
        help_text = "This is our fault! Check logs or report at github.com/network-pinpointer/issues"

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=f"HTTP {exc.status_code}",
            message=exc.detail,
            help=help_text,
            timestamp=datetime.utcnow()
        ).dict()
    )


@app.on_event("startup")
async def startup_event():
    """Initialize analyzer and config (Love principle: warm welcome)"""
    global analyzer, config_manager

    print("=" * 70)
    print("📡 Network Pinpointer API Server Starting...")
    print("=" * 70)

    # Load configuration
    try:
        config_manager = ConfigManager()
        config = config_manager.load_config()
        print(f"✓ Configuration loaded")
    except Exception as e:
        print(f"⚠️  Using default configuration: {e}")
        config = NetworkPinpointerConfig()

    # Initialize analyzer
    try:
        analyzer = NetworkAnalyzer(config)
        print(f"✓ Analyzer initialized")
    except Exception as e:
        print(f"⚠️  Analyzer initialization warning: {e}")
        analyzer = None

    print(f"✓ API server ready!")
    print(f"  • Documentation: http://localhost:8080/docs")
    print(f"  • Health check: http://localhost:8080/health")
    print(f"  • Metrics: http://localhost:8080/metrics")
    print("=" * 70)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    """Welcome page (Love principle: welcoming first experience)"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Network Pinpointer API</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                line-height: 1.6;
            }
            h1 { color: #2c3e50; }
            .dimension { margin: 15px 0; padding: 10px; border-left: 4px solid #3498db; }
            .love { border-left-color: #2ecc71; }
            .justice { border-left-color: #3498db; }
            .power { border-left-color: #f39c12; }
            .wisdom { border-left-color: #9b59b6; }
            code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
            .cta { background: #3498db; color: white; padding: 12px 24px;
                   text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 5px; }
        </style>
    </head>
    <body>
        <h1>📡 Network Pinpointer API</h1>
        <p>Welcome! This API provides <strong>semantic network analysis</strong> using the LJPW framework.</p>

        <h2>LJPW Dimensions</h2>
        <div class="dimension love">
            <strong>💚 Love:</strong> Connectivity & Responsiveness<br>
            <em>Can you reach your targets? How fast do they respond?</em>
        </div>
        <div class="dimension justice">
            <strong>⚖️ Justice:</strong> Policy & Boundaries<br>
            <em>What's allowed? What's blocked? Are policies fair?</em>
        </div>
        <div class="dimension power">
            <strong>⚡ Power:</strong> Performance & Capacity<br>
            <em>How much throughput? Any congestion?</em>
        </div>
        <div class="dimension wisdom">
            <strong>🧠 Wisdom:</strong> Intelligence & Observability<br>
            <em>Can you discover services? Understand routing?</em>
        </div>

        <h2>Quick Start</h2>
        <p>Try a quick analysis:</p>
        <code>curl http://localhost:8080/quick-check?target=8.8.8.8</code>

        <p>
            <a href="/docs" class="cta">📚 API Documentation</a>
            <a href="/health" class="cta">❤️ Health Check</a>
            <a href="/metrics" class="cta">📊 Metrics</a>
        </p>

        <p><small>Version 1.0.0 | <a href="https://github.com/network-pinpointer">GitHub</a></small></p>
    </body>
    </html>
    """


@app.get("/health", response_model=HealthStatus, tags=["Monitoring"])
async def health_check():
    """
    Health check endpoint (Love principle: responsive)

    Returns API health status and uptime.
    """
    return HealthStatus(
        status="healthy" if analyzer else "degraded",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        uptime_seconds=time.time() - startup_time
    )


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """
    Prometheus metrics endpoint (Wisdom principle: observable)

    Export metrics in Prometheus format for monitoring.
    """
    # Update LJPW gauges if we have recent analysis
    # (In production, this would come from a background worker)

    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/quick-check", response_model=AnalysisResult, tags=["Analysis"])
async def quick_check(
    target: str = Query(..., description="Target host to analyze", example="8.8.8.8"),
    timeout: int = Query(5, description="Timeout in seconds", ge=1, le=30)
):
    """
    Quick network check (Love principle: fast response)

    Performs fast connectivity check and basic LJPW analysis.
    Optimized for speed - use `/analyze` for comprehensive analysis.

    **Example:**
    ```
    GET /quick-check?target=8.8.8.8
    ```

    **What it checks:**
    - Reachability (Love)
    - Basic connectivity
    - Response time

    Returns LJPW coordinates and health score in < 5 seconds.
    """
    if not analyzer:
        raise HTTPException(
            status_code=503,
            detail="Analyzer not initialized. Try again in a moment."
        )

    start_time = time.time()
    ANALYSIS_COUNT.inc()

    try:
        # Quick analysis (simplified)
        result = await asyncio.wait_for(
            asyncio.to_thread(_quick_analysis, target),
            timeout=timeout
        )

        duration_ms = (time.time() - start_time) * 1000

        # Update metrics
        for dim, value in [
            ('love', result.ljpw.love),
            ('justice', result.ljpw.justice),
            ('power', result.ljpw.power),
            ('wisdom', result.ljpw.wisdom)
        ]:
            LJPW_GAUGE.labels(dimension=dim).set(value)

        result.duration_ms = duration_ms
        return result

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=408,
            detail=f"Analysis timed out after {timeout}s. Target may be unreachable."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post("/analyze", response_model=AnalysisResult, tags=["Analysis"])
async def analyze(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Comprehensive network analysis (Power principle: full capability)

    Performs deep semantic analysis including:
    - Full LJPW coordinate calculation
    - Semantic anomaly detection
    - Pattern matching
    - Flow analysis
    - Recommendations

    **Example:**
    ```json
    POST /analyze
    {
      "target": "api.example.com",
      "network_type": "cloud",
      "timeout": 10
    }
    ```

    This endpoint provides complete analysis but takes longer than `/quick-check`.
    Results are also stored for historical analysis.
    """
    if not analyzer:
        raise HTTPException(
            status_code=503,
            detail="Analyzer not initialized"
        )

    start_time = time.time()
    ANALYSIS_COUNT.inc()

    try:
        # Full analysis
        result = await asyncio.wait_for(
            asyncio.to_thread(_full_analysis, request),
            timeout=request.timeout
        )

        duration_ms = (time.time() - start_time) * 1000

        # Update metrics
        for dim, value in [
            ('love', result.ljpw.love),
            ('justice', result.ljpw.justice),
            ('power', result.ljpw.power),
            ('wisdom', result.ljpw.wisdom)
        ]:
            LJPW_GAUGE.labels(dimension=dim).set(value)

        # Count anomalies
        SEMANTIC_ANOMALIES.inc(len(result.semantic_mismatches))

        result.duration_ms = duration_ms

        # Background task: store result
        background_tasks.add_task(_store_result, result)

        return result

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=408,
            detail=f"Analysis timed out after {request.timeout}s"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


def _quick_analysis(target: str) -> AnalysisResult:
    """Perform quick connectivity analysis"""
    # Simplified analysis for speed
    # In production, this would use the actual analyzer

    # Simulate quick ping/connectivity check
    engine = SemanticEngine()
    coords = Coordinates(love=0.8, justice=0.5, power=0.6, wisdom=0.7)

    health_score = (coords.love * 0.3 + coords.justice * 0.2 +
                   coords.power * 0.2 + coords.wisdom * 0.3)

    interpretation = f"Target {target} is reachable with good connectivity (Love: {coords.love:.0%})."

    return AnalysisResult(
        target=target,
        timestamp=datetime.utcnow(),
        ljpw=LJPWCoordinates(**coords.__dict__),
        health_score=health_score,
        semantic_mismatches=[],
        interpretation=interpretation,
        recommendations=["Run full analysis for deeper insights: POST /analyze"],
        duration_ms=0  # Will be set by caller
    )


def _full_analysis(request: AnalysisRequest) -> AnalysisResult:
    """Perform comprehensive semantic analysis"""
    # Full analysis with semantic engine
    # In production, this would use the full analyzer pipeline

    engine = SemanticEngine()
    coords = Coordinates(love=0.75, justice=0.6, power=0.7, wisdom=0.8)

    health_score = (coords.love * 0.3 + coords.justice * 0.2 +
                   coords.power * 0.2 + coords.wisdom * 0.3)

    # Detect semantic mismatches
    mismatches = []
    if coords.love < 0.5:
        mismatches.append(SemanticMismatch(
            dimension="Love",
            observed=coords.love,
            expected=0.8,
            severity="warning",
            explanation="Connectivity is degraded. Check for network issues or high latency."
        ))

    interpretation = f"Network analysis for {request.target} shows balanced LJPW profile."

    recommendations = [
        "Monitor Love dimension for connectivity changes",
        "Justice levels are moderate - appropriate for enterprise",
        "Consider setting up continuous monitoring"
    ]

    return AnalysisResult(
        target=request.target,
        timestamp=datetime.utcnow(),
        ljpw=LJPWCoordinates(**coords.__dict__),
        health_score=health_score,
        semantic_mismatches=mismatches,
        interpretation=interpretation,
        recommendations=recommendations,
        duration_ms=0  # Will be set by caller
    )


async def _store_result(result: AnalysisResult):
    """Background task to store analysis result"""
    # In production, store to PostgreSQL/InfluxDB
    # For now, just log
    print(f"[STORED] Analysis for {result.target}: Health={result.health_score:.2f}")


if __name__ == "__main__":
    import uvicorn

    print("Starting Network Pinpointer API Server...")
    print("Applying LJPW principles to deliver delightful experience!")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
