from fastapi import Depends, FastAPI

from . import debuggeometries, eventstream
from .security import ApiKeyManager

app = FastAPI(dependencies=[Depends(ApiKeyManager.verify)])
app.include_router(debuggeometries.router)
app.include_router(eventstream.router)
