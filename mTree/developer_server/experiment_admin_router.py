from fastapi import APIRouter
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pathlib
experiment_admin_router = APIRouter()

from mTree.components.registry import Registry
from mTree.system.actor_system_connector import ActorSystemConnector
from mTree.system.mes_simulation_library import MESSimulationLibrary


templates_folder = pathlib.Path(__file__).parent.joinpath("templates").absolute()

templates = Jinja2Templates(directory=templates_folder)


@experiment_admin_router.get("", tags=["experiment admin"])
async def admin_dashboard(request: Request):    
    # TODO replace password check
    return templates.TemplateResponse("admin_base.html", {"request": request})
