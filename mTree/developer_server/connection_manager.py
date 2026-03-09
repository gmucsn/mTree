from fastapi import APIRouter, FastAPI, Request, WebSocket, WebSocketDisconnect


class ConnectionManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.active_connections: list[WebSocket] = []
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self._initialized:
            self._initialized = True
        else:
            print("Instance already initialized.")

    # def __init__(self):
    #     self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self._instance.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self._instance.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self._instance.active_connections:
            await connection.send_text(message)
