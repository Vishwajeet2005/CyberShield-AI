"""
CyberShield AI — FastAPI Application Entry Point
5-module AI-powered cyber resilience platform for India's CNI.
"""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
