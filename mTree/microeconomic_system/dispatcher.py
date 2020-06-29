from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
#from socketIO_client import SocketIO, LoggingNamespace

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
        print("Starting to dispatch simulation(s)")


    def run_simulation(self, configuration, run_number=None):
        component_registry = registry.Registry()

        print("ABOUT TO REGISTER AGENTS AND GET COMPONENTS")

        environment = component_registry.get_component_class(configuration["environment"])
        if "institution" in configuration.keys():
            institution = component_registry.get_component_class(configuration["institution"])
        elif "institutions" in configuration.keys():
            institutions = []
            for institution_d in configuration["institutions"]:
                institution_class = component_registry.get_component_class(institution_d["institution"])
                institutions.append(institution_class)

        agents = []
        for agent_d in configuration["agents"]:
            agent_class = component_registry.get_component_class(agent_d["agent_name"])
            agent_count = agent_d["number"]
            agents.append((agent_class, agent_count))

        environment = self.createActor(environment)

        if "properties" in configuration.keys():
            message = Message()
            message.set_directive("simulation_properties")
            payload = {"properties": configuration["properties"]}
            payload["simulation_id"] = configuration["id"]
            if run_number is not None:
                payload["run_number"] = run_number
            message.set_payload(payload)
            self.send(environment, message)

        # setup environment log actor
        message = Message()
        message.set_directive("initialize_log_actor")
        payload = {}
        message.set_payload(payload)
        self.send(environment, message)


        if 'institutions' not in locals():
            message = Message()
            message.set_directive("setup_institution")
            message.set_payload({"institution_class": institution})
            self.send(environment, message)
        else:
            for institution in institutions:
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
        self.send(environment, start_message)


    def begin_simulations(self):
        print("s")
        for simulation in self.configurations_pending:
            if "number_of_runs" in simulation.keys():
                for run_number in range(0, simulation["number_of_runs"]):
                    self.run_simulation(simulation, run_number)
            else:
                self.run_simulation(simulation)



    def receiveMessage(self, message, sender):
        logging.info("MESSAGE RCVD: %s DIRECTIVE: %s SENDER: %s", self, message, sender)


        if isinstance(message, PoisonMessage):
            logging.exception("Posioning HAPPENED: %s -- %s -- %s", self, message, "sssss")
        else:
            if message.get_directive() == "simulation_configurations":
                self.configurations_pending = message.get_payload()
                self.begin_simulations()

