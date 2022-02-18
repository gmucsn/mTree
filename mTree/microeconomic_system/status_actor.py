from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
from mTree.microeconomic_system.outconnect import OutConnect

#from socketIO_client import SocketIO, LoggingNamespace

import logging
import json


class StatusActor(Actor):
    def __str__(self):
        return "<StatusActor: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        #socketIO = SocketIO('127.0.0.1', 5000, LoggingNamespace)
        self.configurations_pending = []
        self.configurations_finished = []
        self.agent_memory = {}
        

    def run_simulation(self, configuration, run_number=None):
        #self.component_registrar.instance.components[""]
        
        # test_environment = self.createActor("mTree.microeconomic_system.environment.Environment")
        # message = Message()
        # message.set_directive("simulation_properties")
        # payload = {"properties": configuration["properties"],  "dispatcher":self.myAddress}
        # payload["simulation_id"] = configuration["id"]
        # payload["run_number"] = 1
        # message.set_payload(payload)
        
        #self.send(test_environment, message)
        ####
        # get the source hash for the newly loaded MES components
        ####
        source_hash = configuration["source_hash"]
        
        
        # print("WHAT IS MY SOURCE HASH????????? ", str(source_hash))
        # test_environment = self.createActor("t_environment.TEnvironment",sourceHash=source_hash)
        
        #return

        ####
        # Create the environment for the new MES
        ####
        source_hash = configuration["source_hash"]
        environment_class = configuration["environment"]
        environment = self.createActor(environment_class,sourceHash=source_hash)
        # environment created
        self.environment = environment

        ####
        # Setup logger for the MES
        ####
        message = Message()
        message.set_directive("logger_setup")
        payload = {}
        payload["simulation_id"] = configuration["id"]
        payload["simulation_run_id"] = configuration["simulation_run_id"]
        payload["mes_directory"] = configuration["mes_directory"]
        payload["simulation_configuration"] = configuration
        if "data_logging" in configuration.keys():
            payload["data_logging"] = configuration["data_logging"]
        message.set_payload(payload)
        self.send(environment, message)
        
        
        ####
        # Setup Institution(s) for the MES    
        # This preps configuration, but won't intitiate instantiation
        ####

        institutions = []
        if "institution" in configuration.keys():
            institutions = [configuration["institution"]]
        elif "institutions" in configuration.keys():
            institutions = configuration["institutions"]
            # if len(configuration["institutions"]) == 1:
            #     institutions = [configuration["institutions"]]
            # else:
            #     pass
            #     # for institution_d in configuration["institutions"]:
                    # institution_class = institution_d
                    # institutions.append(institution_class)
            
        ####
        # Setup Agent(s) for the MES    
        # This preps configuration, but won't intitiate instantiation
        ####
        
        agents = []
        for agent_d in configuration["agents"]:
            agent_type = agent_d["agent_name"]
            agent_count = agent_d["number"]
            agents.append((agent_type, agent_count))
            # for i in range(0, agent_count):
            #     agents.append((agent_type, 1))

        

        
        if "properties" in configuration.keys():
            message = Message()
            message.set_directive("simulation_properties")
            payload = {"properties": configuration["properties"],  "dispatcher":self.myAddress}
            payload["simulation_id"] = configuration["id"]
            payload["simulation_run_id"] = configuration["simulation_run_id"]
            
            if run_number is not None:
                payload["run_number"] = run_number
            message.set_payload(payload)
            
            self.send(environment, message)

        

        # if 'institutions' not in locals():
        #     message = Message()
        #     message.set_directive("setup_institution")
        #     message.set_payload({"order": 2, "institution_class": institution, "source_hash": source_hash})
        #     self.send(environment, message)
        # else:
        
        for index, setup_inst in enumerate(institutions):
            order = index + 1
            message = Message()
            message.set_directive("setup_institution")
            if isinstance(setup_inst, dict):
                message.set_payload({"order": order, "institution_class": setup_inst["institution"], "source_hash": source_hash})    
            else:
                message.set_payload({"order": order, "institution_class": institutions, "source_hash": source_hash})
            self.send(environment, message)

        # if hasattr(self, 'agent_memory_prepared'):
        #     for agent in zip(agents, self.agent_memory):
        #         message = Message()
        #         message.set_directive("setup_agents")
        #         message.set_payload({"agent_class": agent[0][0], "num_agents": agent[0][1], "agent_memory": agent[1], "source_hash": source_hash})
        #         self.send(environment, message)
        # else:
        for agent in agents:
            message = Message()
            message.set_directive("setup_agents")
            message.set_payload({"agent_class": agent[0], "num_agents": agent[1], "source_hash": source_hash})
            self.send(environment, message)

        

        start_message = Message()
        start_message.set_sender("experimenter")
        start_message.set_directive("start_environment")
        self.send(environment, start_message)
        

    # TODO examine this to verify that the component registry is the problem in live launch...
    # def memory_run_simulation(self, configuration, run_number=None):
    #     component_registry = registry.Registry()


    #     environment = component_registry.get_component_class(configuration["environment"])
    #     if "institution" in configuration.keys():
    #         institution = component_registry.get_component_class(configuration["institution"])
    #     elif "institutions" in configuration.keys():
    #         institutions = []
    #         for institution_d in configuration["institutions"]:
    #             institution_class = component_registry.get_component_class(institution_d["institution"])
    #             institutions.append(institution_class)

    #     agents = []
    #     for agent_d in configuration["agents"]:
    #         agent_class = component_registry.get_component_class(agent_d["agent_name"])
    #         agent_count = agent_d["number"]
    #         agents.append((agent_class, agent_count))

    #     environment = self.createActor(environment)
    #     print("$" * 25)
    #     print("CONFIGURATION CHECK")
    #     print(configuration)
    #     print("^" * 25)
    #     if "properties" in configuration.keys():
    #         message = Message()
    #         message.set_directive("simulation_properties")
    #         payload = {"properties": configuration["properties"]}
    #         payload["simulation_id"] = configuration["id"]
    #         payload["log_actor"] = self.log_actor
    #         if run_number is not None:
    #             payload["run_number"] = run_number
    #         message.set_payload(payload)
    #         print("SENDING SIMULATION CONFIGURATION INFORMATION")
    #         self.send(environment, message)

    #     # setup environment log actor
    #     # message = Message()
    #     # message.set_directive("initialize_log_actor")
    #     # payload = {}
    #     # message.set_payload(payload)
    #     # self.send(environment, message)


    #     if 'institutions' not in locals():
    #         message = Message()
    #         message.set_directive("setup_institution")
    #         message.set_payload({"institution_class": institution})
    #         self.send(environment, message)
    #     else:
    #         for institution in institutions:
    #             message = Message()
    #             message.set_directive("setup_institution")
    #             message.set_payload({"properties": configuration["properties"], "institution_class": institution})
    #             self.send(environment, message)

    #     for agent in agents:
    #         message = Message()
    #         message.set_directive("setup_agents")
    #         message.set_payload({"properties": configuration["properties"], "agent_class": agent[0], "num_agents": agent[1]})
    #         self.send(environment, message)


    #     start_message = Message()
    #     start_message.set_sender("experimenter")
    #     start_message.set_directive("start_environment")
    #     self.send(environment, start_message)


    # def run_simulation(self, configuration, run_number=None):
    #     component_registry = registry.Registry()
    #     with open("/Users/Shared/repos/mTree_auction_examples/sample_output", "a") as file_object:
    #         file_object.write("SHOULD BE RUNNING SIMULATION" + "\n")
                

    #     try:
    #         environment = component_registry.get_component_class(configuration["environment"])
    #     except Exception as e:
    #         environment = configuration["environment"]

    #     environment = self.createActor(environment)

    #     self.environment = environment

    #     try:
    #         if "institution" in configuration.keys():
    #             institution = component_registry.get_component_class(configuration["institution"])
    #         elif "institutions" in configuration.keys():
    #             institutions = []
    #             for institution_d in configuration["institutions"]:
    #                 institution_class = component_registry.get_component_class(institution_d["institution"])
    #                 institutions.append(institution_class)
    #     except Exception as e:
    #         if "institution" in configuration.keys():
    #             institution = configuration["institution"]
    #         elif "institutions" in configuration.keys():
    #             institutions = []
    #             for institution_d in configuration["institutions"]:
    #                 institution_class = institution_d["institution"]
    #                 institutions.append(institution_class)

    #     agents = []
    #     for agent_d in configuration["agents"]:
    #         try:
    #             agent_class = component_registry.get_component_class(agent_d["agent_name"])
    #         except Exception as e:
    #             agent_class = agent_d["agent_name"]
    #         agent_count = agent_d["number"]
    #         for i in range(0, agent_count):
    #             agents.append((agent_class, 1))


    #     print("$" * 25)
    #     print("CONFIGURATION CHECK")
    #     print(configuration)
    #     print("^" * 25)

    #     if "properties" in configuration.keys():
    #         message = Message()
    #         message.set_directive("simulation_properties")
    #         payload = {"properties": configuration["properties"]} #, "dispatcher":self.myAddress}
    #         payload["simulation_id"] = configuration["id"]
    #         #payload["log_actor"] = self.log_actor
            
    #         if run_number is not None:
    #             payload["run_number"] = run_number
    #         message.set_payload(payload)
    #         print("Environment: Simulation Properties Loading")
    #         print(payload)
    #         print("^!" * 25 )
    #         self.send(environment, message)

    #     # setup environment log actor
    #     # message = Message()
    #     # message.set_directive("initialize_log_actor")
    #     # payload = {}
    #     # message.set_payload(payload)
    #     # self.send(environment, message)


    #     if 'institutions' not in locals():
    #         message = Message()
    #         message.set_directive("setup_institution")
    #         message.set_payload({"institution_class": institution})
    #         self.send(environment, message)
    #     else:
    #         for institution in institutions:
    #             message = Message()
    #             message.set_directive("setup_institution")
    #             message.set_payload({"institution_class": institution})
    #             self.send(environment, message)

    #     if hasattr(self, 'agent_memory_prepared'):
    #         for agent in zip(agents, self.agent_memory):
    #             message = Message()
    #             message.set_directive("setup_agents")
    #             message.set_payload({"agent_class": agent[0][0], "num_agents": agent[0][1],
    #             "agent_memory": agent[1]})
    #             self.send(environment, message)
    #     else:
    #         for agent in agents:
    #             message = Message()
    #             message.set_directive("setup_agents")
    #             message.set_payload({"agent_class": agent[0], "num_agents": agent[1]})
    #             self.send(environment, message)

    #     start_message = Message()
    #     start_message.set_sender("experimenter")
    #     start_message.set_directive("start_environment")
    #     self.send(environment, start_message)

    # # def begin_simulations(self):
    # #     for simulation in self.configurations_pending:
    # #         print("SIUMAUTLALJKF ")
    # #         print(simulation)
    # #         if "number_of_runs" in simulation.keys():
    # #             for run_number in range(0, simulation["number_of_runs"]):
    # #                 self.run_simulation(simulation, run_number)
    # #         else:
    # #             self.run_simulation(simulation)

    def begin_simulations(self):
        # move log construction to attach to environment...
        # try:
        #     self.log_actor = self.createActor(LogActor, globalName="log_actor")
        # except Exception as e:
        #     self.log_actor = self.createActor("LogActor", globalName="log_actor")
        
        # log_basis = {}
        # log_basis["message_type"] = "setup"
        # print("CONFIGURATIONS PENDING")
        # print(self.configurations_pending)
        target_configuration = None
        try:
            target_configuration = self.configurations_pending[0]
        except Exception as e:
            target_configuration = self.configurations_pending
        
        # log_basis["simulation_id"] = target_configuration["id"]
        # log_basis["mes_directory"] = target_configuration["mes_directory"]
        # self.send(self.log_actor, log_basis)        



        if "number_of_runs" in target_configuration.keys():
            self.runs_remaining = target_configuration["number_of_runs"]
            self.current_run = 0
            self.run_simulation(target_configuration, self.current_run)
        else:
            self.run_simulation(target_configuration)
        

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
        #outconnect = ActorSystem("multiprocTCPBase").createActor(OutConnect, globalName = "OutConnect")
        #self.send(outconnect, message)
        #logging.info("MESSAGE RCVD: %s DIRECTIVE: %s SENDER: %s", self, message, sender)
        # with open("/Users/Shared/repos/mTree_auction_examples/sample_output", "a") as file_object:
        #     file_object.write("SHOULD BE RUNNING SIMULATION" + str(message) +  "\n")
    
        if not isinstance(message, ActorSystemMessage):
            if message.get_directive() == "simulation_configurations":
                self.configurations_pending = message.get_payload()
                self.begin_simulations()
            elif message.get_directive() == "end_round":
                self.agent_memory = []
                self.agents_to_wait = len(message.get_payload()["agents"])
            elif message.get_directive() == "store_agent_memory":
                if self.agents_to_wait > 1:
                    self.agents_to_wait -= 1
                    self.agent_memory.append(message.get_payload()["agent_memory"])
                    self.send(sender, ActorExitRequest())
        
                else:
                    self.agent_memory.append(message.get_payload()["agent_memory"])
                    self.agents_to_wait -= 1
                    self.agent_memory_prepared = True
        
                    self.send(sender, ActorExitRequest())
        
                    self.end_round()
                    self.next_run()

