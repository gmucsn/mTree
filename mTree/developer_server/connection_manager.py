import os
from pathlib import Path
from typing import List

import yaml
from fastapi import APIRouter, FastAPI, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field, ValidationError, field_validator


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
            cls._instance.active_connections: list[WebSocket] = []
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
