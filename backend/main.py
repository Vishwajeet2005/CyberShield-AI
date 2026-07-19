"""
CyberShield AI — FastAPI Application Entry Point
5-module AI-powered cyber resilience platform for India's CNI.
"""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import config
from database import init_db
from utils.simulator import simulator
from services.vpa_service import load_feeds
from services.crdt_service import build_digital_twin
from routers import bade, aapa, airo, vpa, crdt, system

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s: %(message)s")
logger = logging.getLogger("cybershield")


# ─────────────────────────────────────────────
# Lifespan (startup / shutdown)
# ─────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────
    logger.info("🛡️  CyberShield AI starting up...")

    logger.info("  [1/4] Initialising audit log database...")
    init_db()

    logger.info("  [2/4] Starting BADE event simulator...")
    await simulator.start()

    logger.info("  [3/4] Loading VPA threat feeds (NVD + CISA KEV)...")
    await load_feeds()

    logger.info("  [4/4] Building CRDT digital twin graph...")
    build_digital_twin()

    logger.info("✅  All modules operational. API ready.")
    yield

    # ── Shutdown ─────────────────────────────
    logger.info("🛑  Shutting down CyberShield AI...")
    await simulator.stop()
    logger.info("Shutdown complete.")


# ─────────────────────────────────────────────
# App
# ─────────────────────────────────────────────

app = FastAPI(
    title=config.APP_NAME,
    version=config.VERSION,
    description=config.DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─────────────────────────────────────────────
# Security Middleware
# ─────────────────────────────────────────────

MAX_BODY_BYTES = 1 * 1024 * 1024  # 1 MB hard cap

@app.middleware("http")
async def body_guard(request: Request, call_next):
    """
    Rejects:
      - Zero-byte bodies on POST/PUT/PATCH (the attack vector found in chaos testing)
      - Bodies larger than 1 MB to prevent memory exhaustion
    """
    if request.method in ("POST", "PUT", "PATCH"):
        content_length = request.headers.get("content-length")

        # Block explicit Content-Length: 0 with a JSON content-type
        if content_length is not None and int(content_length) == 0:
            if "application/json" in request.headers.get("content-type", ""):
                logger.warning("SECURITY: Zero-byte body rejected from %s %s",
                               request.method, request.url.path)
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Request body must not be empty for this method."}
                )

        # Block oversized bodies
        if content_length is not None and int(content_length) > MAX_BODY_BYTES:
            logger.warning("SECURITY: Oversized body (%s bytes) rejected from %s %s",
                           content_length, request.method, request.url.path)
            return JSONResponse(
                status_code=413,
                content={"detail": f"Request body exceeds maximum allowed size of {MAX_BODY_BYTES // 1024}KB."}
            )

    return await call_next(request)


# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_URL, config.FRONTEND_URL_ALT, "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Routers
# ─────────────────────────────────────────────

app.include_router(system.router)
app.include_router(bade.router)
app.include_router(aapa.router)
app.include_router(airo.router)
app.include_router(vpa.router)
app.include_router(crdt.router)


# ─────────────────────────────────────────────
# Root
# ─────────────────────────────────────────────

@app.get("/", tags=["Root"])
async def root():
    return {
        "name": config.APP_NAME,
        "version": config.VERSION,
        "status": "operational",
        "description": config.DESCRIPTION,
        "modules": {
            "BADE": "Behavioural Anomaly Detection Engine",
            "AAPA": "APT Attribution & Prediction Agent",
            "AIRO": "Autonomous Incident Response Orchestrator",
            "VPA":  "Vulnerability Prioritisation Agent",
            "CRDT": "Cyber Resilience Digital Twin",
        },
        "docs": "/docs",
        "api_prefix": "/api",
    }
