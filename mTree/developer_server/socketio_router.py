import socketio
import os

from mTree.components import registry
# from mTree.server.component_registrar import ComponentRegistrar
from mTree.server.configuration_scanner import ConfigurationScanner
from mTree.server.simulation_controller import SimulationController
from mTree.server.subject_pool import SubjectPool
from mTree.development.subject_directory import SubjectDirectory
from mTree.components.registry import Registry
from mTree.system.mes_simulation_library import MESSimulationLibrary
from mTree.system.actor_system_connector import ActorSystemConnector


sio=socketio.AsyncServer(cors_allowed_origins='*',async_mode='asgi')
SubjectPool().register_flask_outlet(sio)

@sio.on("connect")
async def connect(sid, env):
    print("New Client Connected to This id :"+" "+str(sid))

@sio.on("disconnect")
async def disconnect(sid):
    print("Client Disconnected: "+" "+str(sid))



class SubjectNamespace(socketio.AsyncNamespace):
    def __init__(self, namespace=None):
        self.subject_pool = SubjectPool()
        super(socketio.AsyncNamespace, self).__init__(namespace)


    async def on_connect(self, sid, environ):
        self.subject_pool.attempt_add(sid)
        await self.emit('hello', {})

    def on_disconnect(self, sid, reason):
        self.subject_pool.attempt_remove(sid)
        pass

    async def get_subject_pool(self):
        pass
        # return self.subject_pool

    # @self.socketio.on("json", namespace="/subject")
    async def on_json(self, sid, json):
        command = json["command"]
        payload = json["payload"]
        print("the command is ", command)
        print("the payload is ", payload)
        if command == "register_subject_id":
            subject_directory = SubjectDirectory()
            subject_directory.update_subjects(payload["subject_id"], sid)
            # await self.join_room(payload["subject_id"])
            # await self.join_room("all_subjects")
            await self.enter_room(sid, payload["subject_id"])
            await self.enter_room(sid, "all_subjects")
            
            await self.emit(
                "subject_message",
                {"response": "Another Subject Connected "},
                to="all_subjects",
            )
            await self.emit(
                "subject_message",
                {
                    "response": "subject_connection",
                    "payload": {"subjects": subject_directory.get_subjects()},
                },
                namespace="/developer",
                to="admin",
            )
        elif command == "agent_action":
            if "control_action" in payload.keys():
                if payload["control_action"] == "register":
                    await self.emit(
                        "subject_message",
                        {
                            "response": "subject_ui_details",
                            "payload": payload,
                        },
                        namespace="/developer",
                        to="admin",
                    )

            # TODO for 
            # actor_system = ActorSystemConnector()
            # actor_system.send_agent_action(json)


class AdminNamespace(socketio.AsyncNamespace):
    def __init__(self, namespace=None):
        self.admin_sid = None
        self.component_registry = registry.Registry()
        self.subject_pool = SubjectPool()
        
        self.configuration_scanner = ConfigurationScanner()
        super(socketio.AsyncNamespace, self).__init__(namespace)
        # self.subject_pool.register_flask_outlet(self)
        

    async def on_connect(self, sid, environ):
        # self.subject_pool.attempt_add(request.sid)
        print("ADMIN Connected")
        self.admin_sid = sid
        await self.emit("log_message", {"data": "Received by server."})
        await self.emit("chat", {"data": "Connected"})

    def on_disconnect(self, sid, reason):
        # self.subject_pool.attempt_remove(request.sid)
        pass

    async def on_get_components(self, sid, reason):
        agents = self.component_registry.agent_list()
        institutions = self.component_registry.institution_list()
        environments = self.component_registry.environment_list()
        response = {
            "message": "component_list",
            "data": {
                "agents": agents,
                "institutions": institutions,
                "environments": environments,
            },
        }
        await self.emit("response", response)

    async def on_get_subject_pool(self, sid, reason):
        response = {
            "message": "subject_pool_data",
            "data": self.subject_pool.get_json(),
        }
        await self.emit("response", response)

    async def on_get_configurations(self, sid, reason):
        response = {
            "message": "configuration_data",
            "data": self.configuration_scanner.get_configurations(),
        }
        await self.emit("response", response)

    async def on_run_simulation_configuration(self, sid, reason):
        print("SIMULATION RUNNING>>>>")
        sim_controller = SimulationController()
        sim_controller.process_configuration(
            "/Users/Shared/repos/mTree_examples/mes_example_1/config/mes_example_2.json"
        )

        # server_runner.launch_multi_simulations()
        response = {"message": "simulation_running"}
        await self.emit("response", response)



class DeveloperNamespace(socketio.AsyncNamespace):
    # def __init__(self, namespace=None):
    #     self.subject_pool = SubjectPool()
    #     super(socketio.AsyncNamespace, self).__init__(namespace)


    async def on_connect(self, sid, environ):
        await self.emit("subject_message", {"response": "connected"})
        # namespace="/developer",
        await self.emit("log_message", {"data": "Received by server."})
        

    def on_disconnect(self, sid, reason):
        # self.subject_pool.attempt_remove(sid)
        pass

    async def get_subject_pool(self):
        pass
        # return self.subject_pool

    async def on_json(self, sid, json):
        print("Admin message received: ", json)
        command = json["command"]
        payload = json["payload"]

        if command == "developer_execute_ui_method":
                await self.emit(
                    "execute_method",
                    payload,
                    namespace="/subject",
                    to="all_subjects",
                )
        if command == "developer_display_ui":
                ui_file = os.path.join(os.getcwd(), "ui", "seller_interface.html")
                ui_content = None
                with open(ui_file, "r") as t_file:
                    ui_content = t_file.read()
                
                await self.emit(
                    "display_ui",
                    {"ui_content": ui_content},
                    namespace="/subject",
                    
                    to="all_subjects",
                )
        if command == "register_admin":
            await self.enter_room(sid, "admin")
        if command == "start_subject_experiment":
            subject_directory = SubjectDirectory()
            if not subject_directory.experiment_status():
                await self.emit(
                    "experiment_status_message",
                    {"response": "status", "payload": {"status": "Started"}},
                )
                subject_directory.start_experiment()
                configuration = payload["configuration"]
                # run_code_gen = str(uuid.uuid4())
                # run_code = run_code_gen[0:6]

                # await self.emit(
                #     "display_ui",
                #     {"ui_file": "seller_interface.html"},
                # )
                
                ui_file = os.path.join(os.getcwd(), "ui", "seller_interface.html")
                ui_content = None
                with open(ui_file, "r") as t_file:
                    ui_content = t_file.read()
                
                await self.emit(
                    "display_ui",
                    {"ui_content": ui_content},
                    namespace="/subject",
                    
                    to="all_subjects",
                )
                # self.send_to_subject("display_ui", {"ui_file": "seller_interface.html"})

                # component_registry = Registry()
                # working_dir = os.path.join(os.getcwd())
                # simulation_library = MESSimulationLibrary()
                # simulation_library.list_human_subject_files_directory(working_dir)
                # simulation = simulation_library.get_simulation_by_filename(
                #     configuration
                # )
                # actor_system = ActorSystemConnector()
                # working_dir = os.path.join(os.getcwd())
                # actor_system.run_human_subject_experiment(
                #     working_dir,
                #     configuration,
                #     simulation["description"].to_hash(),
                #     subject_directory.get_subjects(),
                # )

#         @self.socketio.on("disconnect")
#         def test_disconnect():
#             print("Client disconnected!!!!")

#         @self.socketio.on("run_test_configuration", namespace="/developer")
#         def run_test_configuration(message):
#             actor_system = ActorSystemConnector()
#             actor_system.send_message()
#             # return self.component_registry.message(message)

#         @self.socketio.on("message", namespace="/developer")
#         def message_handler(message):
#             self.socketio.send(message, namespace="/developer", broadcast=True)

#         # @self.socketio.on('admin_mes_message', namespace='/developer')
#         # def admin_mes_message(message):
#         #     self.actor_system.send_message()
#         #     self.socketio.send(message, namespace='/developer', broadcast=True)

#         @self.socketio.on("admin_mes_message", namespace="/developer")
#         def admin_mes_message(message):

#             admin_message = AdminMessage(request=message["request"])
#             if "payload" in message.keys():
#                 admin_message.set_payload(message["payload"])

#             actor_system = ActorSystemConnector()
#             actor_system.send_message(admin_message)

#         @self.socketio.on("admin_mes_response", namespace="/developer")
#         def admin_mes_response(message):
#             print("WebServer handling an MES admin response")
#             self.socketio.emit(
#                 "mes_response", message, namespace="/developer", broadcast=True
#             )

#         @self.socketio.on("system_status", namespace="/developer")
#         def system_status(message):
#             print("Retrieved system status")
#             print(message)
#             self.socketio.send(message, namespace="/developer", broadcast=True)

#             # return self.component_registry.message(message)

#         @self.socketio.on("get_system_status", namespace="/developer")
#         def get_system_status(message):
#             print("Shoud start to run a sim")
#             print(message)
#             actor_system = ActorSystemConnector()
#             actor_system.send_message(message)
#             self.socketio.emit(
#                 {"data": "echo back"}, namespace="/developer", broadcast=True
#             )




sio.register_namespace(SubjectNamespace('/subject'))
sio.register_namespace(AdminNamespace('/admin'))
sio.register_namespace(DeveloperNamespace('/developer'))