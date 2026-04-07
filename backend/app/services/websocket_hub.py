from __future__ import annotations

from collections import defaultdict

from fastapi import WebSocket


class NotificationHub:
    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[user_id].add(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        connections = self._connections.get(user_id)
        if not connections:
            return
        connections.discard(websocket)
        if not connections:
            self._connections.pop(user_id, None)

    async def push_to_user(self, user_id: str, payload: dict[str, object]) -> None:
        dead_connections: list[WebSocket] = []
        for websocket in self._connections.get(user_id, set()):
            try:
                await websocket.send_json(payload)
            except Exception:
                dead_connections.append(websocket)

        for websocket in dead_connections:
            self.disconnect(user_id, websocket)


notification_hub = NotificationHub()
