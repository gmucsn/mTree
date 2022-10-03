import sys, getopt
import json
import inspect
import os
import glob
from zipfile import ZipFile
import datetime
import importlib
import importlib.util
import time

from thespian.actors import *

from mTree.microeconomic_system.dispatcher import Dispatcher
from mTree.microeconomic_system.message import Message
# from mTree.microeconomic_system.live_dispatcher import LiveDispatcher
# from mTree.microeconomic_system.outconnect import OutConnect
from mTree.microeconomic_system.admin_message import AdminMessage
from mTree.microeconomic_system.container import Container
from mTree.microeconomic_system.simulation_container import SimulationContainer
from mTree.components import registry
from mTree.server.log_config import logcfg


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
            # self.capabilities = dict([('Admin Port', 19000)])
            # self.actor_system = ActorSystem('multiprocTCPBase', capabilities=self.capabilities, logDefs=logcfg)
            # self.capabilities = dict([('Admin Port', 19000)])
            self.actor_system = ActorSystem('multiprocTCPBase') #, logDefs=logcfg)

            ActorSystemConnector.__instance = self
            self.dispatchers = []
            self.source_hashes = []

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
            # Here is where we collect all files to include in the thespian submitted artifact
            #print("--> ", plugin_file_path)


        with ZipFile('temp_components.zip', 'w') as zipObj2:
            for component in base_components:
                zipObj2.write(component[0],arcname=component[1])

        self.capabilities = dict([('Admin Port', 19000)])

        source_hash = None
        try:
            asys = ActorSystemConnector.__instance.actor_system #ActorSystem('multiprocTCPBase', self.capabilities)
            source_hash = asys.loadActorSource('temp_components.zip')
            #asys.createActor(Dispatcher,sourceHash=source_hash, globalName="dispatcher")
            os.remove("temp_components.zip")
        except:
            pass
        return source_hash

    def run_simulation(self, mes_base_dir, configuration_filename, run_configuration):
        #sa = ActorSystem("multiprocTCPBase", capabilities).createActor(SimpleSourceAuthority)
        #ActorSystem("multiprocTCPBase").tell(sa, True)
        
        # print("!&@#*" * 25)
        # print(json.dumps(run_configuration))

        source_hash = self.load_base_mes(mes_base_dir)
        print(source_hash)
        # if self.instance.container is None:
        #     self.instance.container = SimulationContainer()
        # self.instance.container.create_dispatcher()
       
        #return
        # actor_system = ActorSystem()
        self.capabilities = dict([('Admin Port', 19000)])

        # Kill old dispatchers....

        # for dispatcher in self.__instance.dispatchers:
        #     ActorSystem().tell(dispatcher, ActorExitRequest())

        dispatcher = ActorSystemConnector.__instance.actor_system.createActor(Actor, globalName = "Dispatcher") # ActorSystem("multiprocTCPBase", self.capabilities).createActor(Dispatcher, globalName = "Dispatcher")
        # ActorSystemConnector.__instance.actor_system.tell(dispatcher, "START DISPATCHER")
        self.__instance.dispatchers.append(dispatcher)
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

        # simulation_run_id is set here
        # we use a human readable date format
        
        config_base_name = os.path.basename(configuration_filename).split('.')[0]
        nowtime = datetime.datetime.now().timestamp()
        # Simulation Run ID Generator - TODO consolidate with subject ID generation
        nowtime_filename = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        simulation_run_id = config_base_name + "-" + nowtime_filename #str(nowtime).split(".")[0]
        run_configuration["simulation_run_id"] = simulation_run_id
        run_configuration["mes_directory"] = mes_base_dir
        configuration_message.set_payload(run_configuration)
        ActorSystemConnector.__instance.actor_system.tell(dispatcher, configuration_message) #createActor(Dispatcher, globalName = "Dispatcher")
        print("dispatcher request -> " + str(configuration_message))
        # ActorSystem("multiprocTCPBase", self.capabilities).tell(dispatcher, configuration_message)

    def get_status(self):
        if len(self.__instance.dispatchers) == 0:
            return []
        else:
            dispatcher = ActorSystemConnector.__instance.actor_system.createActor(Dispatcher, globalName = "Dispatcher")# ActorSystem("multiprocTCPBase", self.capabilities).createActor(Dispatcher, globalName = "Dispatcher")
            configuration_message = Message()
            configuration_message.set_directive("check_status")
            response = ActorSystemConnector.__instance.actor_system.ask(dispatcher, configuration_message) #.createActor(Dispatcher, globalName = "Dispatcher")
            # ActorSystem("multiprocTCPBase", self.capabilitie).ask(dispatcher, configuration_message)
            return response

    def kill_run_by_id(self, run_id):
        dispatcher = ActorSystemConnector.__instance.actor_system.createActor(Dispatcher, globalName = "Dispatcher") #ActorSystem("multiprocTCPBase", self.capabilities).createActor(Dispatcher, globalName = "Dispatcher")
        configuration_message = Message()
        configuration_message.set_directive("kill_run_by_id")
        payload = {}
        payload["run_id"] = run_id
        configuration_message.set_payload(payload)
        ActorSystemConnector.__instance.actor_system.tell(dispatcher, configuration_message)
        # ActorSystem("multiprocTCPBase", self.capabilitie).tell(dispatcher, configuration_message)

    def send_message(self, message):
        '''
            This method allows injections of messages into the Actor System by routing through the Dispatcher.
        '''
        dispatcher = ActorSystemConnector.__instance.actor_system.createActor(Dispatcher, globalName = "Dispatcher")#ActorSystem("multiprocTCPBase", self.capabilities).createActor(Dispatcher, globalName = "Dispatcher")
        ActorSystemConnector.__instance.actor_system.tell(dispatcher, message)
        #ActorSystem("multiprocTCPBase", self.capabilitie).tell(dispatcher, message)

    def send_agent_action(self, message):
        '''
            This method allows injections of messages into the Actor System by routing through the Dispatcher.
        '''
        dispatcher = ActorSystemConnector.__instance.actor_system.createActor(Dispatcher, globalName = "Dispatcher")#ActorSystem("multiprocTCPBase", self.capabilities).createActor(Dispatcher, globalName = "Dispatcher")
        ActorSystemConnector.__instance.actor_system.tell(dispatcher, message)

    # 2022 purge
    # def send_message(self):
    #     # if self.instance.container is None:
    #     #     self.instance.container = SimulationContainer()
    #     # self.instance.container.create_dispatcher()
    #     capabilities = dict([('Admin Port', 19000)])

    #     actor_system = ActorSystem("multiprocTCPBase", capabilities)

    #     sa = actor_system.createActor(SimpleSourceAuthority)
    #     actor_system.tell(sa, True)
    #     dispatcher = ActorSystem("multiprocTCPBase", capabilities).createActor(Dispatcher, globalName = "Dispatcher")

    #     outconnect = ActorSystem("multiprocTCPBase", capabilities).createActor(OutConnect, globalName = "OutConnect")

    #     configuration_message = Message()
    #     configuration_message.set_directive("simulation_configurations")
    #     configuration = [{"mtree_type": "mes_simulation_description",
    #         "name":"Basic CVA Run",
    #         "id": "1",
    #         "environment": "CVAEnvironment",
    #         "institution": "CVAInstitution",
    #         "number_of_runs": 1,
    #         "agents": [{"agent_name": "CVASimpleAgent", "number": 5}],
    #         "properties": {
    #             "agent_endowment": 10
    #             }
    #         }]
    #     configuration_message.set_payload(configuration)
    #     ActorSystem().tell(dispatcher, configuration_message)
    
    
    def run_human_subject_experiment(self, mes_base_dir, configuration_filename, run_configuration, subjects):
        source_hash = self.load_base_mes(mes_base_dir)
        self.capabilities = dict([('Admin Port', 19000)])

        dispatcher = ActorSystemConnector.__instance.actor_system.createActor(Actor, globalName = "Dispatcher") # ActorSystem("multiprocTCPBase", self.capabilities).createActor(Dispatcher, globalName = "Dispatcher")
        
        self.__instance.dispatchers.append(dispatcher)

        configuration_message = Message()
        configuration_message.set_directive("human_subject_configuration") #"simulation_configurations")
        run_configuration["source_hash"] = source_hash
        config_base_name = os.path.basename(configuration_filename).split('.')[0]
        nowtime = datetime.datetime.now().timestamp()
        # Simulation Run ID setup
        nowtime_filename = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        simulation_run_id = config_base_name + "-" + nowtime_filename #str(nowtime).split(".")[0]
        run_configuration["simulation_run_id"] = simulation_run_id
        run_configuration["mes_directory"] = mes_base_dir
        run_configuration["subjects"] = subjects
        run_configuration["properties"] = run_configuration["properties"]
        configuration_message.set_payload(run_configuration)
        print("RUN CONFIG --> ", run_configuration)

        ActorSystemConnector.__instance.actor_system.tell(dispatcher, configuration_message) #createActor(Dispatcher, globalName = "Dispatcher")
 