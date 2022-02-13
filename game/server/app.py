from fastapi import FastAPI

from . import debuggeometries

app = FastAPI()
app.include_router(debuggeometries.router)
