import sys, getopt
import json
import importlib
import inspect
import os
import glob

import importlib.util
import sys
import time

from mTree.microeconomic_system.dispatcher import Dispatcher
from mTree.microeconomic_system.live_dispatcher import LiveDispatcher
from mTree.microeconomic_system.outconnect import OutConnect
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.container import Container
from mTree.microeconomic_system.simulation_container import SimulationContainer
from thespian.actors import *
from mTree.components import registry
import os
import glob
from zipfile import ZipFile

import datetime


class Hello(Actor):
    def receiveMessage(self, message, sender):
        self.send(sender, 'Hello, World!')

class SimpleSourceAuthority(Actor):
    def receiveMessage(self, msg, sender):
        if msg is True:
            self.registerSourceAuthority()
        if isinstance(msg, ValidateSource):
            self.send(sender,
                      ValidatedSource(msg.sourceHash,
                                      msg.sourceData,
                                      # Thespian pre 3.2.0 has no sourceInfo
                                      getattr(msg, 'sourceInfo', None)))


capabilities = dict([('Admin Port', 19000)])


class ActorSystemConnector():

    # class __ActorSystemConnector:
    #     def __init__(self):
    #         self.actor_system = None
    #         self.component_registry = registry.Registry()
    #         self.container = None
    #         self.component_registry.register_server(self)
    #         #self.multi_simulation = multi_simulation
    #         self.container = None
    #         self.configuration = None
            
    #         # if self.multi_simulation is not True:
    #         #     self.configuration = self.load_mtree_config(config_file)
    #         # else:
    #         #     self.configuration = self.load_multiple_mtree_config(config_file)
    #         # print("Current Configuration: ", json.dumps(self.configuration, indent=4, sort_keys=True))

    #     def __str__(self):
    #         return repr(self)

    __instance = None
    
    def __init__(self):
        if ActorSystemConnector.__instance is None:
            self.actor_system = None
            self.component_registry = registry.Registry()
            self.container = None
            self.component_registry.register_server(self)
            #self.multi_simulation = multi_simulation
            self.container = None
            self.configuration = None
            ActorSystemConnector.__instance = self

    # def __new__(self):
    #     if not ActorSystemConnector.instance:
    #         ActorSystemConnector.instance = ActorSystemConnector.__ActorSystemConnector()
    #     return self

    def load_base_mes(self, mes_base_dir):
        script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "microeconomic_system")
        #script_dir = os.path.join(mes_base_dir, "mes")
        # script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "microeconomic_system")
        
        # #plugins_directory_path = os.path.join(os.getcwd(), 'mes')
        #print("\t plugin path: ", plugins_directory_path)
        plugin_file_paths = glob.glob(os.path.join(script_dir, "*.py"))
        base_components = []
        for plugin_file_path in plugin_file_paths:
            plugin_file_name = os.path.basename(plugin_file_path)
            module_name = os.path.splitext(plugin_file_name)[0]
            if module_name.startswith("__"):
                continue
            base_components.append([plugin_file_path, plugin_file_name])

        #base_components = []
        script_dir = os.path.join(mes_base_dir, "mes")
        plugin_file_paths = glob.glob(os.path.join(script_dir, "*.py"))
        
        for plugin_file_path in plugin_file_paths:
            plugin_file_name = os.path.basename(plugin_file_path)
            module_name = os.path.splitext(plugin_file_name)[0]
            if module_name.startswith("__"):
                continue
            base_components.append([plugin_file_path, plugin_file_name])


        with ZipFile('temp_components.zip', 'w') as zipObj2:
            for component in base_components:
                zipObj2.write(component[0],arcname=component[1])

        capabilities = dict([('Admin Port', 19000)])

        asys = ActorSystem('multiprocTCPBase', capabilities)
        source_hash = asys.loadActorSource('temp_components.zip')
        #asys.createActor(Dispatcher,sourceHash=source_hash, globalName="dispatcher")
        os.remove("temp_components.zip")
        return source_hash


    def run_simulation(self, mes_base_dir, run_configuration):
        #sa = ActorSystem("multiprocTCPBase", capabilities).createActor(SimpleSourceAuthority)
        #ActorSystem("multiprocTCPBase").tell(sa, True)
        
        
        source_hash = self.load_base_mes(mes_base_dir)
        # if self.instance.container is None:
        #     self.instance.container = SimulationContainer()
        # self.instance.container.create_dispatcher()
       
        #return
        # actor_system = ActorSystem()
        capabilities = dict([('Admin Port', 19000)])

        dispatcher = ActorSystem("multiprocTCPBase", capabilities).createActor(Dispatcher, globalName = "Dispatcher")

        #outconnect = ActorSystem("multiprocTCPBase").createActor(OutConnect, globalName = "OutConnect")

        configuration_message = Message()
        configuration_message.set_directive("simulation_configurations")
        # configuration = [{"mtree_type": "mes_simulation_description",
        #     "name":"Basic CVA Run",
        #     "id": "1",
        #     "environment": "CVAEnvironment",
        #     "institution": "CVAInstitution",
        #     "number_of_runs": 1,
        #     "agents": [{"agent_name": "CVASimpleAgent", "number": 5}],
        #     "properties": {
        #         "agent_endowment": 10
        #         }
        #     }]
        run_configuration["source_hash"] = source_hash


        nowtime = datetime.datetime.now().timestamp()
        simulation_run_id = str(nowtime).split(".")[0]

        run_configuration["simulation_run_id"] = simulation_run_id
        run_configuration["mes_directory"] = mes_base_dir
        configuration_message.set_payload(run_configuration)
        ActorSystem().tell(dispatcher, configuration_message)


    def send_message(self):
        # if self.instance.container is None:
        #     self.instance.container = SimulationContainer()
        # self.instance.container.create_dispatcher()
        capabilities = dict([('Admin Port', 19000)])

        actor_system = ActorSystem("multiprocTCPBase", capabilities)

        sa = actor_system.createActor(SimpleSourceAuthority)
        actor_system.tell(sa, True)
        dispatcher = ActorSystem("multiprocTCPBase", capabilities).createActor(Dispatcher, globalName = "Dispatcher")

        outconnect = ActorSystem("multiprocTCPBase", capabilities).createActor(OutConnect, globalName = "OutConnect")

        configuration_message = Message()
        configuration_message.set_directive("simulation_configurations")
        configuration = [{"mtree_type": "mes_simulation_description",
            "name":"Basic CVA Run",
            "id": "1",
            "environment": "CVAEnvironment",
            "institution": "CVAInstitution",
            "number_of_runs": 1,
            "agents": [{"agent_name": "CVASimpleAgent", "number": 5}],
            "properties": {
                "agent_endowment": 10
                }
            }]
        configuration_message.set_payload(configuration)
        ActorSystem().tell(dispatcher, configuration_message)
       