import os
from pathlib import Path
from typing import List

import yaml
from fastapi import APIRouter, FastAPI, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field, ValidationError, field_validator

subject_connection_update = """<turbo-stream action="replace" target="messages">
  <template>
    <!-- The contents of this template will be added after the
    the element with ID "current_step". -->
    <li>New item</li>
  </template>
</turbo-stream>"""


class MtreeExperimentConfigFile(BaseModel):
    admin_password: str = Field(min_length=1)
    subject_ids: List[str] = Field(min_length=1)


class ConnectionManager:
    _instance = None
    _initialized = False
    _subject_list = []
    _admin_password = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.ws_active_connections: list[WebSocket] = []
            cls._instance.ts_active_connections: list[WebSocket] = []
            cls._instance.connection_map = {}
            cls._instance.load_mtree_experiment_config()
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self._initialized:
            self._initialized = True
        else:
            print("Instance already initialized.")

    def load_mtree_experiment_config(self):
        experiment_directory = Path.cwd()
        with open(experiment_directory / "mtree_experiment_config.yaml", "r") as f:
            yaml_content = yaml.safe_load(f)
        experiment_configuration = MtreeExperimentConfigFile.model_validate(
            yaml_content
        )
        self._subject_list = experiment_configuration.subject_ids
        self._admin_password = experiment_configuration.admin_password

    async def subject_connect(
        self, websocket: WebSocket, connection_type: str, subject_id: str
    ):
        await websocket.accept()
        if connection_type == "ws":
            self._instance.ws_active_connections.append(websocket)
        elif connection_type == "ts":
            self._instance.ts_active_connections.append(websocket)
        if subject_id not in self._instance.connection_map.keys():
            self._instance.connection_map[subject_id] = {}
        self._instance.connection_map[subject_id][connection_type] = websocket
        await self.update_subject_connection_status(subject_id)

    async def admin_connect(self, websocket: WebSocket, connection_type):
        await websocket.accept()
        if connection_type == "ws":
            self._instance.ws_active_connections.append(websocket)
        elif connection_type == "ts":
            self._instance.ts_active_connections.append(websocket)
        if "admin" not in self._instance.connection_map.keys():
            self._instance.connection_map["admin"] = {}
        self._instance.connection_map["admin"][connection_type] = websocket

    async def update_subject_connection_status(self, subject_id):
        subject_connection_status = f"""<turbo-stream action="replace" target="connection-status-{subject_id}">
            <template>
                Connected
            </template>
            </turbo-stream>"""
        print("SENDING TO ADMIN")
        await self._instance.connection_map["admin"]["ts"].send_text(
            subject_connection_status
        )

    def disconnect(self, websocket: WebSocket):
        self._instance.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self._instance.active_connections:
            await connection.send_text(message)
