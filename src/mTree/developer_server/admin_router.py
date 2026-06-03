import pathlib

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from mTree.developer_server.connection_manager import ConnectionManager

admin_router = APIRouter()


manager = ConnectionManager()

templates_folder = pathlib.Path(__file__).parent.joinpath("templates").absolute()

templates = Jinja2Templates(directory=templates_folder)


@admin_router.get("", tags=["experiment admin"])
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


@admin_router.websocket("/turbo-stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.admin_connect(websocket, "ts")
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@admin_router.websocket("/experiment_ws")
async def experiment_websocket_endpoint(websocket: WebSocket):
    await manager.admin_connect(websocket, "ws")
    # await manager.admin_connect(websocket, "ts")

    try:
        await websocket.send_json({"msg": "Connected to admin router"})
        while True:
            data = await websocket.receive_text() # receiving the next message from the websocket connection to the admin browser
            await manager.route_actor_system_destination_message(data) # send the message along to the actor system
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@admin_router.websocket("/actor_system_ws")
async def actor_system_websocket_endpoint(websocket: WebSocket):
    """
    This route manages the websocket connection between the web server and the actor system
    """
    await manager.actor_system_connect(websocket)
    try:
        while True:
            await websocket.send_json({"msg": "Connected to admin router"})
            data = await websocket.receive_text()
            await manager.route_actor_system_origin_message(data)
    except WebSocketDisconnect:
        manager.actor_system_disconnect(websocket)
