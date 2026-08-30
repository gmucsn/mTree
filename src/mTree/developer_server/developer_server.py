
# from flask_sqlalchemy import SQLAlchemy

import socketio
import uvicorn
from fastapi import FastAPI

from mTree.developer_server.admin_router import admin_router
from mTree.developer_server.developer_router import developer_router
from mTree.developer_server.socketio_router import sio
from mTree.developer_server.subject_router import subject_router
from mTree.developer_server.system_router import base_router

# from mTree.development.development_endpoints import development_area
# from mTree.development.mtree_configuration import MTreeConfiguration
# from mTree.development.subject_directory import SubjectDirectory
# from mTree.microeconomic_system.admin_message import AdminMessage
# from mTree.server.actor_system_connector import ActorSystemConnector
# from mTree.simulation.mes_simulation_library import MESSimulationLibrary
# from mTree.subject_interface.subject_endpoints import subject_area


class DeveloperServer(object):
    """
    A class used to manage the processes related to the FastAPI webservices
    """

    app = None

    def __init__(self):
        self.app = FastAPI()
        # self.sio=socketio.AsyncServer(cors_allowed_origins='*',async_mode='asgi')
        # #wrap with ASGI application
        # self.socket_app = socketio.ASGIApp(sio)
        # self.app.mount("/comm_socket", self.socket_app)
        self.app.include_router(base_router)
        self.app.include_router(subject_router, prefix="/subject")
        self.app.include_router(admin_router, prefix="/admin")
        self.app.include_router(developer_router, prefix="/developer")
        self.socket_app = socketio.ASGIApp(sio, self.app)

    def run_server(self):
        config = uvicorn.Config(
            self.socket_app, host="0.0.0.0", port=8000, reload=True, use_colors=False
        )
        server = uvicorn.Server(config)
        server.run()
        # uvicorn.run("main:server.app", host="0.0.0.0", port=8000, reload=True, use_colors=False)
