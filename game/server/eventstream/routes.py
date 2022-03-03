from asyncio import wait

from fastapi import APIRouter, WebSocket
from fastapi.encoders import jsonable_encoder

from .eventstream import EventStream
from .models import GameUpdateEventsJs
from .. import GameContext

router: APIRouter = APIRouter()


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def shutdown(self) -> None:
        futures = []
        for connection in self.active_connections:
            futures.append(connection.close())
        await wait(futures)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def broadcast(self, events: GameUpdateEventsJs) -> None:
        futures = []
        for connection in self.active_connections:
            futures.append(connection.send_json(jsonable_encoder(events)))
        await wait(futures)


manager = ConnectionManager()


@router.websocket("/eventstream")
async def event_stream(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    while True:
        if not (events := await EventStream.get()).empty:
            if events.shutting_down:
                await manager.shutdown()
                return

            await manager.broadcast(
                GameUpdateEventsJs.from_events(events, GameContext.get())
            )
