from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import (
    controlpoints,
    debuggeometries,
    eventstream,
    flights,
    mapzones,
    navmesh,
    supplyroutes,
    tgos,
    waypoints,
)
from .security import ApiKeyManager
from .settings import ServerSettings

dependencies = []
if ServerSettings.get().require_api_key:
    dependencies.append(Depends(ApiKeyManager.verify))

app = FastAPI(dependencies=dependencies)
app.include_router(controlpoints.router)
app.include_router(debuggeometries.router)
app.include_router(eventstream.router)
app.include_router(flights.router)
app.include_router(mapzones.router)
app.include_router(navmesh.router)
app.include_router(supplyroutes.router)
app.include_router(tgos.router)
app.include_router(waypoints.router)


if ServerSettings.get().cors_allow_debug_server:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
