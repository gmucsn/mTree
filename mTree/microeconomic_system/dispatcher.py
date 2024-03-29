from email.mime import base
from importlib.util import source_hash
from mTree.microeconomic_system.initialization_messages import MESConfigurationPayload
from thespian.actors import *
from thespian.initmsgs import initializing_messages
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.admin_message import AdminMessage
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
from mTree.microeconomic_system.outconnect import OutConnect
from mTree.microeconomic_system.mes_container import MESContainer

# from mTree.microeconomic_system.web_socket_router_actor import WebSocketRouterActor

#from socketIO_client import SocketIO, LoggingNamespace

import logging
import json
import hashlib
import random
from datetime import datetime

from dataclasses import dataclass, field
from typing import Dict


# This class represents a request for an MES component
@dataclass
class ComponentRequest:
    short_name: str = None
    short_name_base: str = None
    source_class: str = None
    source_hash: str = None
    local_properties: dict = field(default_factory=dict) 
    global_properties: dict = field(default_factory=dict)
    number: int = 1
    

class SimulationRun:
    def __init__(self, configuration, run_number=None) -> None:
        
        self.configuration = configuration

        self.name = configuration["name"]
        self.id = configuration["id"]
        self.run_number = run_number
        
        hash_basis = str(self.name) + "-" + str(self.id) + "-" + str(self.run_number) + str(random.uniform(0,100))
        hash_object = hashlib.sha1(hash_basis.encode("utf-8"))
        self.run_code = hash_object.hexdigest()[0:6]

        self.status = "Registered"
        self.mes_base_address = None
        self.start_time = None
        self.end_time = None

    def set_mes_base_address(self, base_address):
        self.mes_base_address = base_address

    def mark_running(self):
        self.status = "Running"
        self.start_time = datetime.now()
    
    def mark_finished(self):
        self.status = "Finished"
        self.end_time = datetime.now()

    def mark_killed(self):
        self.status = "Killed"
        self.end_time = datetime.now()

        
    def mark_excepted(self):
        self.status = "Exception!"
        self.end_time = datetime.now()

    def to_data_row(self):
        total_time = "Not running"
        if self.start_time is not None:
            if self.end_time is not None:
                total_time = self.end_time - self.start_time
            else:
                total_time = datetime.now() - self.start_time
        return [self.run_code, self.name, self.run_number, self.status, str(total_time)]
    
    def __str__(self):
        output_string = f"<SimulationRunStatus run_code: {self.run_code} id: {self.id} run_number: {self.run_number} status: {self.status} start_time: {self.start_time} end_time: {self.start_time}  >"
        return output_string

    def __repr__(self):
        return self.__str__()


import setproctitle

@initializing_messages([('starting', str)], initdone='init_done')
class Dispatcher(Actor):
    # def __init__(self):
        

    def __str__(self):
        return "<Dispatcher: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()


    # def __init__(self):
    #     pass
    #     #socketIO = SocketIO('127.0.0.1', 5000, LoggingNamespace)
    #     # self.simulation_runs = []
    #     # self.configurations_pending = []
    #     # self.configurations_finished = []
    #     # self.agent_memory = {}
        
    def init_done(self):
        setproctitle.setproctitle("mTree - Dispatcher")
        self.simulation_runs = []
        self.configurations_pending = []
        self.configurations_finished = []
        self.agent_memory = {}

        system_status_actor = self.createActor(Actor, globalName = "SystemStatusActor")
        self.send(system_status_actor, "START")
        message = AdminMessage(request="register_dispatcher")
        self.send(system_status_actor, message)
                    
        


    def get_status(self, sender):
        output = []
        for run in self.simulation_runs:
            output.append(run.to_data_row())
        self.send(sender, output)

    def return_admin_status(self):
        web_socket_router_actor = self.createActor(Actor, globalName = "WebSocketRouterActor")

        output = []
        for run in self.simulation_runs:
            output.append(run.to_data_row())
        payload = {"status": output}
        message = AdminMessage(response="system_status", payload=payload)
        
        # message.set_directive("system_status")
        # message.set_sender(self.myAddress)
        # 
        # message.set_payload(payload)
                
        self.send(web_socket_router_actor, message)


    def request_system_status(self):
        '''
            This provides system simulation status suitable for emission via websockets
        '''
        web_socket_router_actor = self.createActor(Actor, globalName = "WebSocketRouterActor")

        output = []
        for run in self.simulation_runs:
            output.append(run.to_data_row())
        message = Message()
        message.set_directive("system_status")
        message.set_sender(self.myAddress)
        payload = {"status": output}
        message.set_payload(payload)
            
        self.send(web_socket_router_actor, message)

    def run_simulation(self, configuration, run_number=None, configuration_obect=None):
        
        ####
        # get the source hash for the newly loaded MES components
        ####
        source_hash = configuration["source_hash"]
        
        
        ####
        # get debug and log level information for sharing across all components
        ####
        debug = configuration["debug"]
        log_level = configuration["log_level"]
        
        
        ####
        # Startup the MES Container that will contain this simulation
        ####

        source_hash = configuration["source_hash"]
        mes_container = self.createActor(MESContainer)
        

        ####
        # Create the environment for the new MES
        ####
        source_hash = configuration["source_hash"]
        environment_class = configuration["environment"]
        # environment = self.createActor(environment_class,sourceHash=source_hash)
        # # environment created
        # self.environment = environment

        ####
        # Initializing Environment
        ####

        # Initialization Message 1
        # self.send(environment, str(environment_class))
        startup_payload = {}
        startup_payload["simulation_configuration"] = configuration
        startup_payload["properties"] = configuration["properties"]
        startup_payload["dispatcher"] = self.myAddress
        startup_payload["simulation_id"] = configuration["id"]
        startup_payload["simulation_run_id"] = configuration["simulation_run_id"]
        startup_payload["short_name"] = str(environment_class)
        startup_payload["run_code"] = configuration_obect.run_code
        startup_payload["status"] = configuration_obect.status
        startup_payload["configuration_object"] = configuration_obect

        startup_payload["debug"] = debug
        startup_payload["log_level"] = log_level

        # payload["run_code"] = configuration_obect.run_code
        # payload["run_code"] = configuration_obect.run_code
        if "data_logging" in configuration.keys():
            startup_payload["data_logging"] = configuration["data_logging"]
        
        
        if run_number is not None:
            startup_payload["run_number"] = run_number
        
        # Initialization Message 2
        # self.send(environment, startup_payload)

        # Initialization Message for Container
        self.send(mes_container, MESConfigurationPayload(mes_configuration_payload=startup_payload))


        # if "properties" in configuration.keys():
        #     message = Message()
        #     message.set_directive("simulation_properties")
        #     message.set_sender(self.myAddress)
        #     payload = {"properties": configuration["properties"],  "dispatcher":self.myAddress}
        #     payload["simulation_id"] = configuration["id"]
        #     payload["simulation_run_id"] = configuration["simulation_run_id"]
            
        #     if run_number is not None:
        #         payload["run_number"] = run_number
        #     message.set_payload(payload)
            
        #     self.send(environment, message)

      
        ### CHANGE THIS TO THE CONTAINER
        if configuration_obect is not None:
            configuration_obect.set_mes_base_address(mes_container)

        return

        ####
        # Setup logger for the MES
        #   This will setup the folders necessary for the simulation files to be written to
        ####
        message = Message()
        message.set_directive("logger_setup")
        payload = {}
        logging.info("SHOULD HAVE AN ENVIRONMENT CLASS: " + str(environment_class))
        payload["short_name"] = str(environment_class)
        payload["simulation_id"] = configuration["id"]
        payload["simulation_run_id"] = configuration["simulation_run_id"]
        payload["simulation_run_number"] = run_number
        payload["mes_directory"] = configuration["mes_directory"]
        payload["simulation_configuration"] = configuration
        payload["run_code"] = configuration_obect.run_code
        payload["status"] = configuration_obect.status

        # payload["run_code"] = configuration_obect.run_code
        # payload["run_code"] = configuration_obect.run_code
        if "data_logging" in configuration.keys():
            payload["data_logging"] = configuration["data_logging"]
        message.set_payload(payload)


        self.send(environment, message)
        
        logging.info('Environment logger created')

        ####
        # Setup Institution(s) for the MES    
        # This preps configuration, but won't intitiate instantiation
        ####

        # FIX
        institutions = []
        institution_requests = []
        if "institution" in configuration.keys():
            institution_request = ComponentRequest()
            institution_request.source_hash=source_hash
            institution_request.number=agent_d["number"]
            institution_request.source_class=agent_d["agent_name"]
            
            institutions = [{"institution_class": configuration["institution"]}]
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
        agent_requests = []
        for agent_d in configuration["agents"]:
            agent_type = agent_d["agent_name"]
            agent_count = agent_d["number"]
            # message.set_payload({"agent_class": agent[0], "num_agents": agent[1], "source_hash": source_hash})
            
            agent_request = ComponentRequest()
            agent_request.source_hash=source_hash
            agent_request.number=agent_d["number"]
            agent_request.source_class=agent_d["agent_name"]
            agent_requests.append(agent_request)
            
            agents.append((agent_type, agent_count))
            # for i in range(0, agent_count):
            #     agents.append((agent_type, 1))


        #### PROBABLY DEPRECATED AS INCLUDED IN ENVIRONMENT STARTUP        
        # if "properties" in configuration.keys():
        #     message = Message()
        #     message.set_directive("simulation_properties")
        #     message.set_sender(self.myAddress)
        #     payload = {"properties": configuration["properties"],  "dispatcher":self.myAddress}
        #     payload["simulation_id"] = configuration["id"]
        #     payload["simulation_run_id"] = configuration["simulation_run_id"]
            
        #     if run_number is not None:
        #         payload["run_number"] = run_number
        #     message.set_payload(payload)
            
        #     self.send(environment, message)

        

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
        
        
        # TODO replace with agent requests
        for agent in agents:
            message = Message()
            message.set_directive("setup_agents")
            message.set_payload({"agent_class": agent[0], "num_agents": agent[1], "source_hash": source_hash})
            self.send(environment, message)

        # for agent_request in agent_requests:
        #     message = Message()
        #     message.set_directive("setup_agent_requests")
        #     message.set_payload(agent_request)
        #     self.send(environment, message)

        start_message = Message()
        start_message.set_sender("experimenter")
        start_message.set_directive("distribute_address_book")
        self.send(environment, start_message)
        

        start_message = Message()
        start_message.set_sender("experimenter")
        start_message.set_directive("start_environment")
        self.send(environment, start_message)
        logging.info('Simulation environment should have started')


    def prepare_simulation_run(self, configuration):
        if "number_of_runs" in configuration.keys():
            total_runs = configuration["number_of_runs"]
            for run_number in range(1, total_runs+1):
                new_simulation_run = SimulationRun(configuration, run_number)
                self.simulation_runs.append(new_simulation_run)
        else:
            new_simulation_run = SimulationRun(configuration, 1)
            self.simulation_runs.append(new_simulation_run)

    def begin_simulations(self):
        MAX_CONCURRENT = 5
        
        for simulation_configuration in self.simulation_runs:
            if simulation_configuration.status == "Registered":    
                simulation_configuration.mark_running()
                self.run_simulation(simulation_configuration.configuration, simulation_configuration.run_number, configuration_obect=simulation_configuration)

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
            

    def update_mes_status(self, sender, message):
             
        for run in self.simulation_runs:
            if run.mes_base_address == sender:
                run.mark_finished()

    def update_mes_run_information(self, sender, message):
            
        for run_index, run in enumerate(self.simulation_runs):
            if run.mes_base_address == sender:
                self.simulation_runs[run_index] = message
                break
        
        
    def shutdown_mes(self, environment_address):
        pass
        # for run in self.simulation_runs:
        #     if run.mes_base_address == environment_address:
        #         run.mark_finished()
        
        #         message = Message()
        #         message.set_directive("update_mes_status")
        #         message.set_sender(self.myAddress)
        #         payload = {}
        #         payload["status"] = run.status
        #         payload["start_time"] = str(run.start_time)
        #         payload["end_time"] = str(run.end_time)
        #         payload["total_time"] = str(run.end_time - run.start_time)        
        #         message.set_payload(payload)
        #         self.send(environment_address, message)
            
        # self.send(environment_address, ActorExitRequest())
    
    def kill_run_by_id(self, message):
        for run in self.simulation_runs:
            if run.run_code == message.get_payload()["run_id"]:
                run.mark_killed()

                message = Message()
                message.set_directive("update_mes_status")
                message.set_sender(self.myAddress)
                payload = {}
                payload["status"] = run.status
                payload["start_time"] = str(run.start_time)
                payload["end_time"] = str(run.end_time)
                payload["total_time"] = str(run.end_time - run.start_time)

                message.set_payload(payload)
                self.send(run.mes_base_address, message)

                self.send(run.mes_base_address, ActorExitRequest())


    

                
    def excepted_mes_shutdown(self, environment_address, exception_payload):
        for run in self.simulation_runs:
            if run.mes_base_address == environment_address:
                run.mark_excepted()

                message = Message()
                message.set_directive("update_mes_status")
                message.set_sender(self.myAddress)
                payload = {}
                payload["status"] = run.status
                payload["start_time"] = str(run.start_time)
                payload["end_time"] = str(run.end_time)
                payload["total_time"] = str(run.end_time - run.start_time)
                payload["exception_payload"] = exception_payload
                message.set_payload(payload)
                self.send(run.mes_base_address, message)
                self.send(environment_address, ActorExitRequest())


    def receiveMessage(self, message, sender):
        #outconnect = ActorSystem("multiprocTCPBase").createActor(OutConnect, globalName = "OutConnect")
        #self.send(outconnect, message)
        #logging.info("MESSAGE RCVD: %s DIRECTIVE: %s SENDER: %s", self, message, sender)
        # with open("/Users/Shared/repos/mTree_auction_examples/sample_output", "a") as file_object:
        #     file_object.write("SHOULD BE RUNNING SIMULATION" + str(message) +  "\n")
        if not isinstance(message, ActorSystemMessage):
            if isinstance(message, AdminMessage):
                if message.get_request() == "system_status":
                    self.return_admin_status()
                elif message.get_request() == "kill_run_by_id":
                    self.kill_run_by_id(message)
            elif isinstance(message, dict):
                # agent action processing...
                new_message = Message()
                new_message.set_directive("agent_action_forward")
                new_message.set_sender(self.myAddress)
                payload = message
                new_message.set_payload(payload["payload"])
                
                # TODO targeting the only known human subject container...
                self.send(self.human_subject_container, new_message)


            else:        
                if message.get_directive() == "simulation_configurations":
                    self.configurations_pending = message.get_payload()
                    self.prepare_simulation_run(message.get_payload())
                    self.begin_simulations()
                    
                elif message.get_directive() == "human_subject_configuration":
                    self.run_human_subject_experiment(message.get_payload())


                elif message.get_directive() == "check_status":
                    self.get_status(sender)
                elif message.get_directive  () == "kill_run_by_id":
                    self.kill_run_by_id(message)
                    
                elif message.get_directive() == "end_round":
                    self.agent_memory = []
                    self.agents_to_wait = len(message.get_payload()["agents"])
                elif message.get_directive() == "shutdown_mes":
                    self.shutdown_mes(sender)
                elif message.get_directive() == "excepted_mes":
                    self.excepted_mes_shutdown(sender, message.get_payload())
                elif message.get_directive() == "update_mes_status":
                    self.update_mes_status(sender, message.get_payload())
                elif message.get_directive() == "update_mes_run_information":
                    self.update_mes_run_information(sender, message.get_payload())

                elif message.get_directive() == "request_system_status":
                    self.request_system_status()

                elif message.get_directive() == "register_dispatcher":
                    pass
                    # system_status_actor = self.createActor(Actor, globalName = "SystemStatusActor")
                    # message = AdminMessage(request="register_dispatcher")
                    # self.send(system_status_actor, message)
                    
                elif message.get_directive() == "register_websocket_router":
                    # registering the dispatcher at the system status actor to prevent starting another
                    
                    self.websocket_router = sender
                    self.send(self.websocket_router, "SLAMBACK")
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

        




    def old_run_human_subject_experiment(self, configuration, run_number=None, configuration_obect=None):
        # self.(simulation_configuration.configuration, simulation_configuration.run_number, configuration_obect=simulation_configuration)
        
        ####
        # get the source hash for the newly loaded MES components
        ####
        source_hash = configuration["source_hash"]
        
        ####
        # Create the environment for the new MES
        ####
        logging.info('Creating a simulation environment')
        source_hash = configuration["source_hash"]
        environment_class = configuration["environment"]
        environment = self.createActor(environment_class,sourceHash=source_hash)
        # environment created
        self.environment = environment

        ####
        # Initializing Environment
        ####
        self.send(environment, str(environment_class))


        logging.info('Simulation environment created')

        if configuration_obect is not None:
            configuration_obect.set_mes_base_address(environment)


        ####
        # Setup logger for the MES
        #   This will setup the folders necessary for the simulation files to be written to
        ####
        message = Message()
        message.set_directive("logger_setup")
        payload = {}
        payload["short_name"] = str(environment_class)
        payload["simulation_id"] = configuration["id"]
        payload["simulation_run_id"] = configuration["simulation_run_id"]
        payload["simulation_run_number"] = run_number
        payload["mes_directory"] = configuration["mes_directory"]
        payload["simulation_configuration"] = configuration
        payload["run_code"] = "a1" #configuration_obect.run_code
        payload["status"] = "running" #configuration_obect.status
        payload["subjects"] = configuration["subjects"]
        # payload["run_code"] = configuration_obect.run_code
        # payload["run_code"] = configuration_obect.run_code
        if "data_logging" in configuration.keys():
            payload["data_logging"] = configuration["data_logging"]
        payload["human_subjects"] = True
        message.set_payload(payload)
        self.send(environment, message)
        
        logging.info('Environment logger created')

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
            if "number" in agent_d.keys():
                agent_count = agent_d["number"]
            else:
                if "min_subjects" in agent_d.keys():
                    if len(configuration["subjects"] >= agent_d["min_subjects"]):
                        agent_count = len(configuration["subjects"])
                

            agents.append((agent_type, agent_count))
            # for i in range(0, agent_count):
            #     agents.append((agent_type, 1))


        
        if "properties" in configuration.keys():
            message = Message()
            message.set_directive("simulation_properties")
            message.set_sender(self.myAddress)
            payload = {"properties": configuration["properties"],  "dispatcher":self.myAddress}
            payload["simulation_id"] = configuration["id"]
            payload["simulation_run_id"] = configuration["simulation_run_id"]
            payload["subjects"] = configuration["subjects"]
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
            logging.info("DISPATCHING INSTITUTIONS./..")
            logging.info(institutions)
            message.set_payload({"order": order, "institution_class": setup_inst["institution"], "source_hash": source_hash})    
            
            # if isinstance(setup_inst, dict):
            #     message.set_payload({"order": order, "institution_class": setup_inst["institution"], "source_hash": source_hash})    
            # else:
            #     message.set_payload({"order": order, "institution_class": institutions, "source_hash": source_hash})
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
        logging.info('Simulation environment should have started')





    def run_human_subject_experiment(self, configuration, run_number=None, configuration_obect=None):        
        ####
        # get the source hash for the newly loaded MES components
        ####
        source_hash = configuration["source_hash"]
        
        logging.info('Booting dispatched')
        logging.info(configuration)

        ####
        # get debug and log level information for sharing across all components
        ####
        debug = configuration["debug"]
        log_level = configuration["log_level"]
        
        
        ####
        # Startup the MES Container that will contain this simulation
        ####
        mes_container = self.createActor(MESContainer)
        # TODO this only lets us run one human subject experiment at a time... BEWARE
        self.human_subject_container = mes_container
      
        ####
        # Create the environment for the new MES
        ####
        environment_class = configuration["environment"]
        
        ####
        # Initializing Environment
        ####

        # Initialization Message 1
        # self.send(environment, str(environment_class))
        startup_payload = {}
        startup_payload["simulation_configuration"] = configuration
        startup_payload["properties"] = configuration["properties"]
        startup_payload["dispatcher"] = self.myAddress
        startup_payload["simulation_id"] = configuration["id"]
        startup_payload["simulation_run_id"] = configuration["simulation_run_id"]
        startup_payload["short_name"] = str(environment_class)
        startup_payload["run_code"] = configuration["run_code"]

        new_simulation_run = SimulationRun(configuration, 1)

        startup_payload["status"] = new_simulation_run.status
        startup_payload["configuration_object"] = new_simulation_run


        startup_payload["subjects"] = configuration["subjects"]
        # payload["run_code"] = configuration_obect.run_code
        # payload["run_code"] = configuration_obect.run_code
        if "data_logging" in configuration.keys():
            startup_payload["data_logging"] = configuration["data_logging"]
        startup_payload["human_subjects"] = True
        

        startup_payload["debug"] = debug
        startup_payload["log_level"] = log_level

        # payload["run_code"] = configuration_obect.run_code
        # payload["run_code"] = configuration_obect.run_code
        if "data_logging" in configuration.keys():
            startup_payload["data_logging"] = configuration["data_logging"]
        
        
        if run_number is not None:
            startup_payload["run_number"] = run_number
        
        # Initialization Message 2
        # self.send(environment, startup_payload)

        # Initialization Message for Container
        self.send(mes_container, MESConfigurationPayload(mes_configuration_payload=startup_payload))


        # if "properties" in configuration.keys():
        #     message = Message()
        #     message.set_directive("simulation_properties")
        #     message.set_sender(self.myAddress)
        #     payload = {"properties": configuration["properties"],  "dispatcher":self.myAddress}
        #     payload["simulation_id"] = configuration["id"]
        #     payload["simulation_run_id"] = configuration["simulation_run_id"]
            
        #     if run_number is not None:
        #         payload["run_number"] = run_number
        #     message.set_payload(payload)
            
        #     self.send(environment, message)

      
        ### CHANGE THIS TO THE CONTAINER
        if configuration_obect is not None:
            configuration_obect.set_mes_base_address(mes_container)




   