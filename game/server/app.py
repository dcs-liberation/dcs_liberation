from fastapi import Depends, FastAPI

from . import debuggeometries, eventstream, flights, navmesh, waypoints
from .security import ApiKeyManager

app = FastAPI(dependencies=[Depends(ApiKeyManager.verify)])
app.include_router(debuggeometries.router)
app.include_router(eventstream.router)
app.include_router(flights.router)
app.include_router(navmesh.router)
app.include_router(waypoints.router)
