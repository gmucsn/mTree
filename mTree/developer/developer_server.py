import hashlib
import importlib
import logging
# from flask_sqlalchemy import SQLAlchemy
import os
import pkgutil
import sys
import uuid
from inspect import getframeinfo, stack
from logging import Handler
from logging.handlers import RotatingFileHandler

import eventlet
import flask
import jinja2
from apscheduler import events
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    send_from_directory,
    session,
)
from flask_apscheduler import APScheduler
from flask_basicauth import BasicAuth
from flask_socketio import SocketIO, close_room, disconnect, emit, join_room, leave_room, rooms
from jinja2 import Environment, FileSystemLoader
from mTree.base.response import Response
from mTree.components import registry
from mTree.components.registry import Registry
# from mTree.development.development_endpoints import development_area
# from mTree.development.mtree_configuration import MTreeConfiguration
# from mTree.development.subject_directory import SubjectDirectory
# from mTree.microeconomic_system.admin_message import AdminMessage
# from mTree.server.actor_system_connector import ActorSystemConnector
# from mTree.simulation.mes_simulation_library import MESSimulationLibrary
# from mTree.subject_interface.subject_endpoints import subject_area

from fastapi import FastAPI
import socketio
import uvicorn
from mTree.developer.system_router import base_router
from mTree.developer.socketio_router import sio


class DeveloperServer(object):
    app = None

    def __init__(self):
        self.app = FastAPI()
        # self.sio=socketio.AsyncServer(cors_allowed_origins='*',async_mode='asgi')
        # #wrap with ASGI application
        # self.socket_app = socketio.ASGIApp(sio)
        # self.app.mount("/comm_socket", self.socket_app)
        self.app.include_router(base_router)
        self.socket_app = socketio.ASGIApp(sio, self.app)

    def run_server(self):
        config = uvicorn.Config(self.socket_app, host="0.0.0.0", port=8000, reload=True, use_colors=False)
        server = uvicorn.Server(config)
        server.run()
        # uvicorn.run("main:server.app", host="0.0.0.0", port=8000, reload=True, use_colors=False) 

    