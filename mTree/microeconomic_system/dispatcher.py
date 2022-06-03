from email.mime import base
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
# from mTree.microeconomic_system.web_socket_router_actor import WebSocketRouterActor

#from socketIO_client import SocketIO, LoggingNamespace

import logging
import json
import hashlib
import random
from datetime import datetime


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

@initializing_messages([('starting', str)], initdone='init_done')
class Dispatcher(Actor):
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
        self.simulation_runs = []
        self.configurations_pending = []
        self.configurations_finished = []
        self.agent_memory = {}

        logging.info("Dispatcher initialized and sending message to system status actor")
        system_status_actor = self.createActor(Actor, globalName = "SystemStatusActor")
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
        logging.info('SENT TO WWEBSOCKET FOR FURTHER PROCESSING')
        logging.info(message)
                
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
            message.set_sender(self.myAddress)
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
            

    def shutdown_mes(self, environment_address):
        for run in self.simulation_runs:
            if run.mes_base_address == environment_address:
                run.mark_finished()
        
                message = Message()
                message.set_directive("update_mes_status")
                message.set_sender(self.myAddress)
                payload = {}
                payload["status"] = run.status
                payload["start_time"] = str(run.start_time)
                payload["end_time"] = str(run.end_time)
                payload["total_time"] = str(run.end_time - run.start_time)        
                message.set_payload(payload)
                self.send(environment_address, message)
            
        self.send(environment_address, ActorExitRequest())
    
    def kill_run_by_id(self, message):
        for run in self.simulation_runs:
            logging.info("DISOPATCHEWR IKILL REUEST " + str(message.get_payload()))
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
        logging.info("Dispatcher recieved message: " + str(message))
        if not isinstance(message, ActorSystemMessage):
            if isinstance(message, AdminMessage):
                logging.info('DISPATCHER RECEIVED ADMIN MESSAGE')
                logging.info(message)
                if message.get_request() == "system_status":
                    logging.info('System status message received')
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
                
                self.send(self.environment, new_message)


            else:        
                if message.get_directive() == "simulation_configurations":
                    logging.info('Preparing to run a new set of simulation configurations')
                    self.configurations_pending = message.get_payload()
                    self.prepare_simulation_run(message.get_payload())
                    logging.info('Prepared the simulation')
                    self.begin_simulations()
                    logging.info('Simulations started')
                
                elif message.get_directive() == "human_subject_configuration":
                    logging.info('Human Subject Configuration Starting!')
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

        

    def run_human_subject_experiment(self, configuration, run_number=None, configuration_obect=None):
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
            agent_count = agent_d["number"]
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