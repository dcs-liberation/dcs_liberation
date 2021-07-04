from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import (
    controlpoints,
    debuggeometries,
    eventstream,
    flights,
    frontlines,
    game,
    mapzones,
    navmesh,
    qt,
    supplyroutes,
    tgos,
    waypoints,
    iadsnetwork,
)
from .settings import ServerSettings

app = FastAPI()
app.include_router(controlpoints.router)
app.include_router(debuggeometries.router)
app.include_router(eventstream.router)
app.include_router(flights.router)
app.include_router(frontlines.router)
app.include_router(game.router)
app.include_router(mapzones.router)
app.include_router(navmesh.router)
app.include_router(qt.router)
app.include_router(supplyroutes.router)
app.include_router(tgos.router)
app.include_router(waypoints.router)
app.include_router(iadsnetwork.router)


origins = []
if ServerSettings.get().cors_allow_debug_server:
    origins.append("http://localhost:3000")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
