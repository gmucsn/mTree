import pathlib
import random

from fastapi import APIRouter, FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mTree.components.registry import Registry
from mTree.developer_server.connection_manager import ConnectionManager
from mTree.system.actor_system_connector import ActorSystemConnector
from mTree.system.mes_simulation_library import MESSimulationLibrary

experiment_admin_router = APIRouter()


manager = ConnectionManager()

templates_folder = pathlib.Path(__file__).parent.joinpath("templates").absolute()

templates = Jinja2Templates(directory=templates_folder)


@experiment_admin_router.get("", tags=["experiment admin"])
async def admin_dashboard(request: Request):
    # TODO replace password check
    return templates.TemplateResponse(
        "admin_base.html", {"request": request, "manager": manager._instance}
    )


example = """<turbo-stream action="append" target="messages">
  <template>
    <div id="message_1">
      This div will be appended to the element with the DOM ID "messages".
    </div>
  </template>
</turbo-stream>
"""
example = """<turbo-stream action="after" target="messages">
  <template>
    <!-- The contents of this template will be added after the
    the element with ID "current_step". -->
    <li>New item</li>
  </template>
</turbo-stream>"""


@experiment_admin_router.websocket("/turbo-stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(example, websocket)
            await manager.broadcast(example)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(example)


@experiment_admin_router.websocket("/experiment_ws")
async def experiment_websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(example, websocket)
            await manager.broadcast(example)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(example)
