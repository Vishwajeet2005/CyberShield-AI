from fastapi import APIRouter
from services.vpa_service import get_prioritized_vulnerabilities, get_assets, get_kev_matches, refresh_feeds

router = APIRouter(prefix="/api/vpa", tags=["VPA"])

@router.get("/vulnerabilities")
async def vulnerabilities():
    return get_prioritized_vulnerabilities()

@router.get("/assets")
async def assets():
    return get_assets()

@router.get("/kev-status")
async def kev_status():
    return get_kev_matches()

@router.post("/refresh")
async def refresh():
    return await refresh_feeds()
