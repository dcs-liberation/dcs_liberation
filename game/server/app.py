from fastapi import FastAPI

from . import debuggeometries, eventstream

app = FastAPI()
app.include_router(debuggeometries.router)
app.include_router(eventstream.router)
