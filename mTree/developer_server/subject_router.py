from fastapi import APIRouter
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form, File, UploadFile
from typing import Annotated
import pathlib
subject_router = APIRouter()

from mTree.components.registry import Registry
from mTree.system.actor_system_connector import ActorSystemConnector
from mTree.system.mes_simulation_library import MESSimulationLibrary


templates_folder = pathlib.Path(__file__).parent.joinpath("templates").absolute()

templates = Jinja2Templates(directory=templates_folder)

# TODO inject subject_ids 
# SUBJECT_IDS = MTree_configuration.instance.subject_ids
SUBJECT_IDS = ["3fed7","3ca90","658bf","5690d","8fee6","60e36","071b8","8070b","87732","7e80d","de206","8d781"]


@subject_router.get("", tags=["experiment subject"])
async def subject_landing_page(request: Request):    
    return templates.TemplateResponse(
            "subject_landing.html", {"request": request}
    )
    
@subject_router.post("", tags=["experiment subject"])
async def subject_with_id_page(response: Response, subject_id: Annotated[str, Form()], request: Request):    
    if subject_id in SUBJECT_IDS:
        # session['subject-id'] = subject_id
        response.set_cookie(key="subject_id", value=subject_id)
        return templates.TemplateResponse(
            "subject_viewer.html", {"request": request, "subject_id": subject_id}
        )
    else:
        return templates.TemplateResponse(
            "subject_landing.html", {"request": request, "error":"Invalid Subject ID"}
        )
    