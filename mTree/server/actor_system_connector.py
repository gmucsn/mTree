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
from mTree.microeconomic_system.outconnect import OutConnect
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.container import Container
from mTree.microeconomic_system.simulation_container import SimulationContainer
from thespian.actors import *
from mTree.components import registry


class Hello(Actor):
    def receiveMessage(self, message, sender):
        self.send(sender, 'Hello, World!')


class ActorSystemConnector():

    class __ActorSystemConnector:
        def __init__(self):
            self.actor_system = None
        


            self.component_registry = registry.Registry()
            self.container = None
            self.component_registry.register_server(self)
            #self.multi_simulation = multi_simulation
            self.container = None
            self.configuration = None
            
            # if self.multi_simulation is not True:
            #     self.configuration = self.load_mtree_config(config_file)
            # else:
            #     self.configuration = self.load_multiple_mtree_config(config_file)
            # print("Current Configuration: ", json.dumps(self.configuration, indent=4, sort_keys=True))

        def __str__(self):
            return repr(self)

    instance = None
    
    def __init__(self):
        if not ActorSystemConnector.instance:
            ActorSystemConnector.instance = ActorSystemConnector.__ActorSystemConnector()
        else:
            return ActorSystemConnector.instance

    def send_message(self):
        # if self.instance.container is None:
        #     self.instance.container = SimulationContainer()
        # self.instance.container.create_dispatcher()
        
        # actor_system = ActorSystem()
        dispatcher = ActorSystem("multiprocTCPBase").createActor(Dispatcher, globalName = "Dispatcher")

        outconnect = ActorSystem("multiprocTCPBase").createActor(OutConnect, globalName = "OutConnect")

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
       