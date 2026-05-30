import pathlib
from typing import Annotated

from fastapi import (
    APIRouter,
    Form,
    Request,
    Response,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.templating import Jinja2Templates
from mTree.developer_server.connection_manager import ConnectionManager

subject_router = APIRouter()


templates_folder = pathlib.Path(__file__).parent.joinpath("templates").absolute()

templates = Jinja2Templates(directory=templates_folder)

manager = ConnectionManager()


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


@subject_router.get("", tags=["experiment subject"])
async def subject_landing_page(request: Request):
    return templates.TemplateResponse("subject_landing.html", {"request": request})


@subject_router.post("/subject_sign_in", tags=["experiment subject"])
async def subject_sign_in(
    response: Response, subject_id: Annotated[str, Form()], request: Request
):
    if subject_id in manager._instance._subject_list:
        # session['subject-id'] = subject_id
        # Message start
        response.set_cookie(key="subject_id", value=subject_id)
        return templates.TemplateResponse(
            "subject_waiting_screen.html",
            {"request": request, "subject_id": subject_id},
            # # headers={"Content-Type": "text/vnd.turbo-stre1am.html; charset=utf-8"},
        )
    else:
        return templates.TemplateResponse(
            "subject_landing.html", {"request": request, "error": "Invalid Subject ID"}
        )


@subject_router.post("", tags=["experiment subject"])
async def subject_with_id_page(
    response: Response, subject_id: Annotated[str, Form()], request: Request
):
    if subject_id in manager._instance._subject_list:
        # Message start
        # session['subject-id'] = subject_id
        response.set_cookie(key="subject_id", value=subject_id)
        return templates.TemplateResponse(
            "subject_viewer.html", {"request": request, "subject_id": "faddfgasdgasd"}
        )
    else:
        return templates.TemplateResponse(
            "subject_landing.html", {"request": request, "error": "Invalid Subject ID"}
        )


####
# Web Socket Endpoints for Subjects
####


@subject_router.websocket("/turbo-stream/{subject_id}")
async def websocket_endpoint(websocket: WebSocket, subject_id: str):
    await manager.subject_connect(websocket, "ts", subject_id)
    # Message start
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.subject_disconnect(websocket, "ts", subject_id)


@subject_router.websocket("/experiment_ws/{subject_id}")
async def experiment_websocket_endpoint(websocket: WebSocket, subject_id: str):
    await manager.subject_connect(websocket, "ws", subject_id)
    # Message start
    try:
        while True:
            data = await websocket.receive_text()
            await manager.route_actor_system_destination_message(data)
    except WebSocketDisconnect:
        await manager.subject_disconnect(websocket, "ws", subject_id)
