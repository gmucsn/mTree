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
        self.agent_memory = {}
        


    def memory_run_simulation(self, configuration, run_number=None):
        component_registry = registry.Registry()


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
            payload["log_actor"] = self.log_actor
            if run_number is not None:
                payload["run_number"] = run_number
            message.set_payload(payload)
            self.send(environment, message)

        # setup environment log actor
        # message = Message()
        # message.set_directive("initialize_log_actor")
        # payload = {}
        # message.set_payload(payload)
        # self.send(environment, message)


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


    def run_simulation(self, configuration, run_number=None):
        component_registry = registry.Registry()
        

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
            for i in range(0, agent_count):
                agents.append((agent_class, 1))

        environment = self.createActor(environment)
        
        self.environment = environment
        
        if "properties" in configuration.keys():
            message = Message()
            message.set_directive("simulation_properties")
            payload = {"properties": configuration["properties"], "dispatcher":self.myAddress}
            payload["simulation_id"] = configuration["id"]
            payload["log_actor"] = self.log_actor
            
            if run_number is not None:
                payload["run_number"] = run_number
            message.set_payload(payload)
            self.send(environment, message)

        # setup environment log actor
        # message = Message()
        # message.set_directive("initialize_log_actor")
        # payload = {}
        # message.set_payload(payload)
        # self.send(environment, message)


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

        if hasattr(self, 'agent_memory_prepared'):
            for agent in zip(agents, self.agent_memory):
                message = Message()
                message.set_directive("setup_agents")
                message.set_payload({"agent_class": agent[0][0], "num_agents": agent[0][1],
                "agent_memory": agent[1]})
                self.send(environment, message)
        else:
            for agent in agents:
                message = Message()
                message.set_directive("setup_agents")
                message.set_payload({"agent_class": agent[0], "num_agents": agent[1]})
                self.send(environment, message)

        start_message = Message()
        start_message.set_sender("experimenter")
        start_message.set_directive("start_environment")
        self.send(environment, start_message)

    # def begin_simulations(self):
    #     for simulation in self.configurations_pending:
    #         print("SIUMAUTLALJKF ")
    #         print(simulation)
    #         if "number_of_runs" in simulation.keys():
    #             for run_number in range(0, simulation["number_of_runs"]):
    #                 self.run_simulation(simulation, run_number)
    #         else:
    #             self.run_simulation(simulation)

    def begin_simulations(self):
        self.log_actor = self.createActor(LogActor)
        log_basis = {}
        log_basis["message_type"] = "setup"
        log_basis["simulation_id"] = self.configurations_pending["id"]
        self.send(self.log_actor, log_basis)        



        if "number_of_runs" in self.configurations_pending.keys():
            self.runs_remaining = self.configurations_pending["number_of_runs"]
            self.current_run = 0
            self.run_simulation(self.configurations_pending, self.current_run)
        else:
            self.run_simulation(self.configurations_pending)


    def end_round(self):
        self.send(self.environment, ActorExitRequest())
        
        # self.log_actor = self.createActor(LogActor)
        # log_basis = {}
        # log_basis["message_type"] = "setup"
        # log_basis["simulation_id"] = self.configurations_pending["id"]
        # self.send(self.log_actor, log_basis)        



        # if "number_of_runs" in self.configurations_pending.keys():
        #     self.runs_remaining = self.configurations_pending["number_of_runs"]
        #     self.current_run = 0
        #     self.run_simulation(self.configurations_pending, self.current_run)
        # else:
        #     self.run_simulation(self.configurations_pending)


    def next_run(self):
        if self.runs_remaining > 0:
            self.runs_remaining -= 1
            self.current_run += 1
            self.run_simulation(self.configurations_pending, self.current_run)
        else:
            self.send(self.myAddress, ActorExitRequest())
            


    def receiveMessage(self, message, sender):
        #logging.info("MESSAGE RCVD: %s DIRECTIVE: %s SENDER: %s", self, message, sender)


        if isinstance(message, PoisonMessage):
            pass
            #logging.exception("Posioning HAPPENED: %s -- %s -- %s", self, message, "sssss")
        elif isinstance(message, ActorExitRequest):
            pass
            #logging.exception("ActorExitRequest: %s -- %s", self, message)
        elif isinstance(message, ChildActorExited):
            pass
            #logging.exception("ChildActorExited: %s -- %s", self, message)
        else:
            if message.get_directive() == "simulation_configurations":
                self.configurations_pending = message.get_payload()
                self.begin_simulations()
            elif message.get_directive() == "end_round":
                self.end_round()
                self.agent_memory = []
                self.agents_to_wait = len(message.get_payload()["agents"])
            elif message.get_directive() == "store_agent_memory":
                if self.agents_to_wait > 1:
                    self.agents_to_wait -= 1
                    self.agent_memory.append(message.get_payload()["agent_memory"])
                else:
                    self.agent_memory.append(message.get_payload()["agent_memory"])
                    self.agents_to_wait -= 1
                    self.agent_memory_prepared = True
                    
                    self.next_run()

