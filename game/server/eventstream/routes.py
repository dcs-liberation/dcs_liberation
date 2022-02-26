from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.websockets import WebSocket

from .eventstream import EventStream
from .models import GameUpdateEventsJs
from .. import GameContext

router: APIRouter = APIRouter()


@router.websocket("/eventstream")
async def event_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        if not (events := await EventStream.get()).empty:
            if events.shutting_down:
                await websocket.close()
                return

            await websocket.send_json(
                jsonable_encoder(
                    GameUpdateEventsJs.from_events(events, GameContext.get())
                )
            )
