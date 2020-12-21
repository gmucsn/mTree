from flask import Flask, render_template, render_template_string, session, request, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect,  Namespace
from mTree.components import registry
from mTree.server.subject_pool import SubjectPool
from mTree.server.configuration_scanner import ConfigurationScanner
from mTree.runner.server_runner import ServerRunner
from mTree.server.component_registrar import ComponentRegistrar
from mTree.server.simulation_controller import SimulationController


import json

class AdminNamespace(Namespace):
    def __init__(self, namespace=None):
        self.admin_sid = None
        self.component_registry = registry.Registry()
        self.subject_pool = SubjectPool()
        self.configuration_scanner = ConfigurationScanner()
        super(Namespace, self).__init__(namespace)


    def on_connect(self):
        print("ADMIN Connected")
        print(request)
        print(request.namespace)
        print(request.sid)
        self.admin_sid = request.sid
        emit('chat', {'data': 'Connected'})

    def on_disconnect(self):
        print("DISCONNECTED AN ADMIN")
        print("\t", request.sid)

    def on_message(self, data):
        print("ADMIN MESSAGE RECEIVED")
        emit('chat', {'data': 'message also connected'})

    def on_get_components(self, data):
        agents = self.component_registry.agent_list()
        institutions = self.component_registry.institution_list()
        environments = self.component_registry.environment_list()
        response = {"message":"component_list", "data": {"agents": agents, "institutions": institutions, "environments": environments}}
        emit('response', response )

    def on_get_subject_pool(self, data):
        response = {"message":"subject_pool_data", "data": self.subject_pool.get_json()}
        emit('response', response )

    def on_get_configurations(self, data):
        response = {"message":"configuration_data", "data": self.configuration_scanner.get_configurations()}
        emit('response', response )
    
    

    def on_run_simulation_configuration(self, data):
        print("SIMULATION RUNNING>>>>")
        sim_controller = SimulationController()
        sim_controller.process_configuration("/Users/Shared/repos/mTree_examples/mes_example_1/config/mes_example_2.json")
        
        #server_runner.launch_multi_simulations()
        response = {"message":"simulation_running"}
        emit('response', response )
    