from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *

from socketIO_client import SocketIO, LoggingNamespace

import logging
import json


class Dispatcher(Actor):
    def __str__(self):
        return "<Dispatcher: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        #socketIO = SocketIO('127.0.0.1', 5000, LoggingNamespace)
        self.configurations_pending = []
        self.configurations_finished = []
        print("Dispatcher started")


    def run_simulation(self, configuration):
        component_registry = registry.Registry()

        environment = component_registry.get_component_class(configuration["environment"])
        institution = component_registry.get_component_class(configuration["institution"])
        agents = []
        for agent_d in configuration["agents"]:
            agent_class = component_registry.get_component_class(agent_d["agent_name"])
            agent_count = agent_d["number"]
            agents.append((agent_class, agent_count))

        environment = self.createActor(environment)

        if "properties" in configuration.keys():
            message = Message()
            message.set_directive("simulation_properties")
            message.set_payload({"properties": configuration["properties"]})
            self.actor_system.tell(self.environment, message)


        message = Message()
        message.set_directive("setup_institution")
        message.set_payload({"institution_class": institution})
        self.send(environment, message)

        for agent in agents:
            message = Message()
            message.set_directive("setup_agents")
            message.set_payload({"agent_class": agent[0], "num_agents": agent[1]})
            self.send(environment, message)


        start_message = Message()
        start_message.set_sender("experimenter")
        start_message.set_directive("start_environment")
        print("start message sent to the environment...")
        self.send(environment, start_message)


    def begin_simulations(self):
        for simulation in self.configurations_pending:
            self.run_simulation(simulation)



    def receiveMessage(self, message, sender):
        logging.info("MESSAGE RCVD: %s DIRECTIVE: %s SENDER: %s", self, message, sender)


        if message.get_directive() == "simulation_configurations":
            self.configurations_pending = message.get_payload()
            self.begin_simulations()
            print("MESSAGE RECEIVED")
            print(message.get_payload())
