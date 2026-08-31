import json
from pathlib import Path

import yaml
from fastapi import WebSocket
from pydantic import BaseModel, Field

from mTree.simulation.configuration import Configuration
from mTree.simulation.human_subject_experiment_message import (
    HumanSubjectExperimentMessage,
)
from mTree.simulation.human_subject_experiment_startup import (
    HumanSubjectExperimentStartup,
)
from mTree.system.actor_system_connector import ActorSystemConnector
from mTree.system.actor_system_controller import ActorSystemController
from mTree.system.actors.websocket_actor import Start_Websocket, WebsocketActor

subject_connection_update = """<turbo-stream action="replace" target="messages">
  <template>
    <!-- The contents of this template will be added after the
    the element with ID "current_step". -->
    <li>New item</li>
  </template>
</turbo-stream>"""


class MtreeExperimentConfigFile(BaseModel):
    admin_password: str = Field(min_length=1)
    subject_ids: list[str] = Field(min_length=1)


class ConnectionManager:
    _instance = None
    _initialized = False
    _experiment_configuration = None
    _simulation_configuration = None
    _yaml_content = None
    _experiment_configuration_yaml: Configuration = None
    _subject_list = []
    _admin_password = "password"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.actor_system_ws_connection: WebSocket = None
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

    def start_websocket_actor(self):
        """
        This method is used to inject a method into the actor system to force the websocket actor to connect
        """
        start_msg = "subscribe"
        ws_addr = "ws://127.0.0.1:8000/admin/actor_system_ws"
        wsc = ActorSystemController.retrieve_connection().createActor(
            WebsocketActor, globalName="websocket_actor"
        )
        startmsg = Start_Websocket(ws_addr, start_msg, wsc)

        ActorSystemController.retrieve_connection().tell(wsc, startmsg)

    def load_mtree_experiment_config(self):
        experiment_directory = Path.cwd()

        with open(experiment_directory / "mtree_experiment_config.yaml") as f:
            self._yaml_content = f.read()
        self._experiment_configuration_yaml = yaml.safe_load(self._yaml_content)
        self._experiment_configuration = MtreeExperimentConfigFile.model_validate(
            self._experiment_configuration_yaml
        )

        self._simulation_configuration = Configuration.load_from_file(
            experiment_directory / "config" / "basic_human_subject_auction.yaml"
        )

        self._subject_list = self._experiment_configuration.subject_ids
        self._admin_password = self._experiment_configuration.admin_password

    async def subject_connect(
        self, websocket: WebSocket, connection_type: str, subject_id: str
    ):
        """
        Method to register websocket connections for subjects
        """
        await websocket.accept()
        if connection_type == "ws":
            self._instance.ws_active_connections.append(websocket)
        elif connection_type == "ts":
            self._instance.ts_active_connections.append(websocket)
        if subject_id not in self._instance.connection_map.keys():
            self._instance.connection_map[subject_id] = {}
        self._instance.connection_map[subject_id][connection_type] = websocket
        await self.update_subject_connection_status(subject_id, "Connected")

    async def subject_disconnect(
        self, websocket: WebSocket, connection_type: str, subject_id: str
    ):
        """
        Method to deregister websocket connections for subjects
        """
        if connection_type == "ws":
            self._instance.ws_active_connections.remove(websocket)
        elif connection_type == "ts":
            self._instance.ts_active_connections.remove(websocket)

        del self._instance.connection_map[subject_id][connection_type]
        await self.update_subject_connection_status(subject_id, "Disconnected")

    async def actor_system_connect(self, websocket: WebSocket):
        """
        A method used to register the websocket connection used for the actor system
        """
        await websocket.accept()
        self._instance.actor_system_ws_connection = websocket
        # await self._instance.actor_system_ws_connection.send_json({"test": "test"})

    async def actor_system_disconnect(self, websocket: WebSocket):
        """
        A method used to deregister the actor system's websocket connection
        """
        self._instance.actor_system_ws_connection = None

    async def admin_connect(self, websocket: WebSocket, connection_type):
        await websocket.accept()
        self.start_websocket_actor()
        if connection_type == "ws":
            self._instance.ws_active_connections.append(websocket)
            self._instance.ts_active_connections.append(websocket)
        elif connection_type == "ts":
            self._instance.ts_active_connections.append(websocket)
        if "admin" not in self._instance.connection_map.keys():
            self._instance.connection_map["admin"] = {}
        self._instance.connection_map["admin"][connection_type] = websocket

    async def update_subject_connection_status(
        self, subject_id: str, status_message: str
    ):
        """
        Send a message to the admin user indicating a subject's connections status

        Args:
            subject_id str identifier of the subject

        """
        subject_connection_status = f"""<turbo-stream action="replace" target="connection-status-{subject_id}">
            <template>
                <td id="connection-status-{subject_id}">{status_message}</td>
            </template>
            </turbo-stream>"""
        await self._instance.connection_map["admin"]["ws"].send_text(
            subject_connection_status
        )

    async def send_admin_ws_message(self, message: str):
        """
        Send a message to the admin user over the websocket

        Args:
            message str string to send to the admin user

        """
        if "ws" in self._instance.connection_map["admin"].keys():
            await self._instance.connection_map["admin"]["ws"].send_text(message)

    async def send_websocket_actor_message(self, message: str):
        """
        Send a message to the websocket actor

        Args:
            message str string to send to the websocket actor

        """
        if self._instance.actor_system_ws_connection is not None:
            await self._instance.actor_system_ws_connection.send_text(message)

    def disconnect(self, websocket: WebSocket):
        try:
            self._instance.active_connections.remove(websocket)
        except:
            pass

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self._instance.active_connections:
            await connection.send_text(message)

    async def route_actor_system_origin_message(self, message: str):
        """
        Send a message to the websocket actor

        Args:
            message str string to send to the websocket actor

        """

        final_message = json.loads(message)
        if "message_kind" in final_message.keys():
            if final_message["message_kind"] == "hotwire_message":
                hotwire_message = {"message": final_message["content"]}
                await self._instance.connection_map[final_message["destination"]][
                    "ws"
                ].send_text(json.dumps(hotwire_message))
        else:
            await self._instance.connection_map[final_message["destination"]][
                "ws"
            ].send_text(json.dumps(final_message))
        # if self._instance.actor_system_ws_connection is not None:
        #     await self._instance.actor_system_ws_connection.send_text(message)

    async def route_actor_system_destination_message(self, message_content: str):
        """
        Send a message to the websocket actor inside the actor system

        Args:
            message str string to send to the websocket actor

        """
        if self._instance.actor_system_ws_connection is not None:
            message = json.loads(message_content)
            match message["action"]:
                case "start_experiment":
                    # Load the current MES into the system
                    source_hash = ActorSystemConnector.load_base_mes(
                        self._instance._simulation_configuration.mes_directory
                    )
                    self._instance._simulation_configuration.source_hash = source_hash
                    startup = HumanSubjectExperimentStartup(
                        configuration=self._instance._simulation_configuration,
                        subject_ids=self._instance.connection_map.keys(),
                        source_hash=source_hash,
                    )
                    final_message = HumanSubjectExperimentMessage(
                        action="start_experiment",
                        source="admin",
                        destination="admin",
                        payload=startup,
                    )
                    await self._instance.actor_system_ws_connection.send_text(
                        final_message.model_dump_json()
                    )

    async def route_actor_system_destination_message_from_subject(
        self, subject_id: str, message_content: str
    ):
        """
        Send a message to the websocket actor inside the actor system destined for a subject

        Args:
            subject_id str the subject id to send the message to
            message str string to send to the websocket actor

        """
        if self._instance.actor_system_ws_connection is not None:
            message = json.loads(message_content)
            final_message = HumanSubjectExperimentMessage(
                action="send_to_agent",
                source=f"{subject_id}",
                destination=f"{subject_id}",
                payload=message,
            )
            await self._instance.actor_system_ws_connection.send_text(
                final_message.model_dump_json()
            )
