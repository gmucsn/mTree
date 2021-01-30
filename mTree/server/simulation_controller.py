from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
from mTree.server.component_registrar import ComponentRegistrar

import logging
import json

capabilities = dict([('Admin Port', 1900)])


class SimulationController:
    class __SimulationController:
        def __init__(self):
            self.components = {}
            self.component_files = []
            self.component_registrar = ComponentRegistrar()
            
        

    instance = None
        
    def __init__(self):
        if not SimulationController.instance:
            SimulationController.instance = SimulationController.__SimulationController()
        
    def process_configuration(self, configuration):
        print("READING CONFIGURATION: ", configuration)
        configurations = self.load_mtree_config(configuration)
        self.run_simulation(configurations)
        
    def load_mtree_config(self, config_file):
        configurations = None
        with open(config_file) as json_file:
            configurations = json.load(json_file)
        return [configurations]

    def run_simulation(self, configurations, run_number=None):
        #self.component_registrar.instance.components[""]
        
        asys = ActorSystem('multiprocTCPBase', capabilities)
        source_hash = SimulationController.instance.component_registrar.get_source_hash()
        for configuration in configurations:
            configuration["source_hash"] = source_hash
            print(configuration)
            print(configuration["source_hash"])
            print("CREATING DISPATCHER FOR CONFIGURATION")
            
            configuration_message = Message()
            configuration_message.set_directive("simulation_configurations")
            configuration_message.set_payload(configuration)
            address = asys.createActor("live_dispatcher.LiveDispatcher", globalName="dispatcher")

            asys.tell(address, configuration_message)

