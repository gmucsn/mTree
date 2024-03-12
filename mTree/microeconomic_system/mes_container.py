from thespian.actors import *
from thespian.initmsgs import initializing_messages


from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.log_message import LogMessage
from mTree.microeconomic_system.sequence_event import SequenceEvent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
from mTree.microeconomic_system.address_book import AddressBook
from mTree.microeconomic_system.mes_exceptions import *
from mTree.microeconomic_system.admin_message import AdminMessage
from mTree.microeconomic_system.initialization_messages import *
#from socketIO_client import SocketIO, LoggingNamespace

import time
import os

import traceback
import logging
import json
from datetime import datetime, timedelta
import time
import sys
import inspect

import setproctitle


@initializing_messages([('_mes_container_configuration', MESConfigurationPayload)],
                            initdone='prepare_mes_container')
class MESContainer(Actor):
    
        


    def prepare_mes_container(self):
        setproctitle.setproctitle("mTree - MESContainer")
        self.simulation_configuration = self._mes_container_configuration.mes_configuration_payload["simulation_configuration"]
        self.mes_directory = self.simulation_configuration["mes_directory"]
        self.global_properties = self._mes_container_configuration.mes_configuration_payload["properties"]
        self.dispatcher = self._mes_container_configuration.mes_configuration_payload["dispatcher"]
        self.simulation_id = self._mes_container_configuration.mes_configuration_payload["simulation_id"]
        self.simulation_run_id = self._mes_container_configuration.mes_configuration_payload["simulation_run_id"]
        self.source_hash = self.simulation_configuration["source_hash"]
        self.run_number = None

        self.debug = self.simulation_configuration["debug"]
        self.log_level = self.simulation_configuration["log_level"]

        if "run_number" in self._mes_container_configuration.mes_configuration_payload.keys():
            self.run_number = self._mes_container_configuration.mes_configuration_payload["run_number"]

        self.run_code = self._mes_container_configuration.mes_configuration_payload["run_code"]
        self.status = self._mes_container_configuration.mes_configuration_payload["status"]

        self.data_logging = None
        if "data_logging" in self._mes_container_configuration.mes_configuration_payload.keys():
            self.data_logging = self._mes_container_configuration.mes_configuration_payload["data_logging"]
        
        if "subjects" in self._mes_container_configuration.mes_configuration_payload.keys():
            self.subjects = self._mes_container_configuration.mes_configuration_payload["subjects"]
        
        logging.info("CONTAINER PREP")
        logging.info(self._mes_container_configuration.mes_configuration_payload)
        

        self.configuration_object = self._mes_container_configuration.mes_configuration_payload["configuration_object"]

        self.logger_setup()

  
        # logging.info("Logger for run should be avialable...")
        # # properties to track contained components
        
        # This list will be used principally for maintaining which mes components
        self.mes_component_list = []

        self.master_address_book = AddressBook(self)        
        self.environment = None
        self.institutions = []
        self.agents = []

        self.construct_environment()
        self.construct_institutions()
        self.construct_agents()
        
        self.distribute_address_book()


        self.start_environment()



    def start_environment(self):
        start_message = Message()
        start_message.set_sender("experimenter")
        start_message.set_directive("start_environment")
        self.send(self.environment, start_message)


    def distribute_address_book(self):

        
        self.send(self.environment, AddressBookPayload(address_book_payload=self.master_address_book._export_data()))
        
        for agent in self.agents:
            self.send(agent, AddressBookPayload(address_book_payload=self.master_address_book._export_data()))

        for institution in self.institutions:
            self.send(institution, AddressBookPayload(address_book_payload=self.master_address_book._export_data()))



    def construct_environment(self):
        ####
        # Create the environment for the new MES
        ####
        source_hash = self.simulation_configuration["source_hash"]
        environment_configuration = self.simulation_configuration["environment"]
        environment_class = None
        if isinstance(environment_configuration, str):
            environment_class = environment_configuration
        elif isinstance(environment_configuration, dict):
            environment_class = environment_configuration["environment_class"]
        logging.info("SHOULD BE CREATING AN ENVIRONMENT...")
        logging.info(str(environment_configuration))
        logging.info(environment_class)
        environment = self.createActor(environment_class, sourceHash=source_hash)
        # environment created
        self.environment = environment

        self.mes_component_list.append(self.environment)

        ####
        # Initializing Environment
        ####

        # Initialization Message 1
        self.send(environment, str(environment_class))


        startup_payload = {}
        startup_payload["simulation_configuration"] = self.simulation_configuration
        startup_payload["properties"] = self.simulation_configuration["properties"]
        ### ADD LOCAL PROPERTIES
        startup_payload["container"] = self.myAddress
        startup_payload["address_type"] = "environment"
        startup_payload["simulation_id"] = self.simulation_id
        startup_payload["simulation_run_id"] = self.simulation_run_id
        # Fix here....
        startup_payload["short_name"] = str(environment_class)
        startup_payload["run_code"] = self.run_code
        startup_payload["status"] = self.status

        # payload["run_code"] = configuration_obect.run_code
        # payload["run_code"] = configuration_obect.run_code
        if self.data_logging is not None:
            startup_payload["data_logging"] = self.data_logging
        
        
        if self.run_number is not None:
            startup_payload["run_number"] = self.run_number
        
        startup_payload["log_actor"] = self.log_actor
        # Initialization Message 2
        self.send(environment, StartupPayload(startup_payload=startup_payload))

        # prep address book entry for the environment

        
        environment_info = {}
        environment_info["address_type"] = "environment"
        environment_info["address"] = self.environment
        environment_info["component_class"] = environment_class
        environment_info["component_number"] = 1
        # Fix here....
        environment_info["short_name"] = str(environment_class)

        self.master_address_book.add_address(environment_info["short_name"], environment_info)

    def construct_institutions(self):

        ####
        # Setup Institution(s) for the MES    
        # This preps configuration, but won't intitiate instantiation
        ####

        institutions = []
        institution_requests = []
        if "institution" in self.simulation_configuration.keys():
            # institution_request = ComponentRequest()
            # institution_request.source_hash=source_hash
            # institution_request.number=agent_d["number"]
            # institution_request.source_class=agent_d["agent_name"]
            institution_request = {}
            institution_request["institution_class"] = self.simulation_configuration["institution"]
            institutions = [institution_request]
        elif "institutions" in self.simulation_configuration.keys():
            institutions = self.simulation_configuration["institutions"]
            # if len(configuration["institutions"]) == 1:
            #     institutions = [configuration["institutions"]]
            # else:
            #     pass
            #     # for institution_d in configuration["institutions"]:
                    # institution_class = institution_d
                    # institutions.append(institution_class)

        #####

        for index, institution_configuration in enumerate(institutions):
            order = index + 1
            if "number" in institution_configuration.keys():

                num_institutions = institution_configuration["number"]
                for i in range(num_institutions):
                    self.create_institution(institution_configuration, i + 1)
            else:

                
                self.create_institution(institution_configuration)


    def create_institution(self, institution_configuration, number=None):
        # FIX short name configuration instruction

        # FIX the configuration objects....
        if "institution_class" in institution_configuration.keys():
            institution_class = institution_configuration["institution_class"]
        else:
            institution_class = institution_configuration["institution_name"]
        institution_number = number

        new_institution = self.createActor(institution_class, sourceHash=self.source_hash)
        
        self.mes_component_list.append(new_institution)

        ###
        # Insitutiton Initialization Message 1
        ###
        institution_short_name = institution_class
        if "short_name" in institution_configuration.keys():
            institution_short_name = institution_configuration["short_name"]

        if number is not None:
            institution_short_name = institution_class + " " + str(institution_number)

        self.send(new_institution, institution_short_name)
        
        startup_payload = {}
        startup_payload["address_type"] = "institution"
        startup_payload["address"] = new_institution
        startup_payload["component_class"] = institution_class
        startup_payload["component_number"] = 1
        startup_payload["short_name"] = institution_short_name
        # global and then local properties
        startup_payload["container"] = self.myAddress
        startup_payload["properties"] = self.global_properties
        startup_payload["simulation_configuration"] = self.simulation_configuration


        if "properties" in institution_configuration.keys():
            startup_payload["local_properties"] = institution_configuration["properties"]


        startup_payload["environment"] = self.myAddress
        startup_payload["simulation_id"] = self.simulation_id
        startup_payload["simulation_run_id"] = self.simulation_run_id
        startup_payload["log_actor"] = self.log_actor
        if "run_number" in dir(self):
            startup_payload["run_number"] = self.run_number
        
        ###
        # Insitutiton Initialization Message 2
        ###
        self.send(new_institution, StartupPayload(startup_payload=startup_payload))
        
        institution_info = {}
        institution_info["address_type"] = "institution"
        institution_info["address"] = new_institution
        institution_info["component_class"] = institution_class
        institution_info["component_number"] = 1
        institution_info["short_name"] = institution_short_name
        self.master_address_book.add_address(institution_info["short_name"], institution_info)

        self.institutions.append(new_institution)


    def construct_agents(self):
        ####
        # Setup Agent(s) for the MES    
        # This preps configuration, but won't intitiate instantiation
        ####

        agents = []
        agent_requests = []
        for agent_d in self.simulation_configuration["agents"]:
            agent_type = agent_d["agent_name"]


            if "number" in agent_d.keys():
                agent_count = agent_d["number"]
            else:
                # if "min_subjects" in agent_d.keys():
                #     if len(self.subjects) >= agent_d["min_subjects"]:
                # TODO should be sensitive to min subject requirements
                agent_count = len(self.subjects)
                

            # agents.append((agent_type, agent_count))
            # for i in range(0, agent_count):
            #     agents.append((agent_type, 1))

            
            # agent_count = agent_d["number"]

            # message.set_payload({"agent_class": agent[0], "num_agents": agent[1], "source_hash": source_hash})
            
            # agent_request = ComponentRequest()
            # agent_request.source_hash=source_hash
            # agent_request.number=agent_d["number"]
            # agent_request.source_class=agent_d["agent_name"]
            # agent_requests.append(agent_request)
            
            agent_configuration = {"agent_class": agent_type, "number": agent_count}
            if "short_name" in agent_d.keys():
                agent_configuration["short_name"] = agent_d["short_name"]
            if "properties" in agent_d.keys():
                agent_configuration["properties"] = agent_d["properties"]

            agents.append(agent_configuration)
            # for i in range(0, agent_count):
            #     agents.append((agent_type, 1))

        for agent_configuration in agents:

            self.create_agent(agent_configuration)
        #     message = Message()
        #     message.set_directive("setup_agents")
        #     message.set_payload({"agent_class": agent[0], "num_agents": agent[1], "source_hash": source_hash})
        #     self.send(environment, message)

    def create_agent(self, agent_configuration):
        # FIX
        if "subjects" in dir(self):
            self.subject_map = {}
        
        agent_class = agent_configuration["agent_class"]
        short_name_base = agent_class
        if "short_name" in agent_configuration.keys():
            short_name_base = agent_configuration["short_name"]


        for i in range(agent_configuration["number"]):
            agent_number = i + 1
            new_agent = self.createActor(agent_class, sourceHash=self.source_hash)
            

            self.mes_component_list.append(new_agent)
            ###
            # Agent Initialization Message #1
            ###


            agent_short_name = short_name_base + " " + str(agent_number)
            self.send(new_agent, agent_short_name)

            ###            
            # Agent Initialization Message #2
            ###
            startup_payload = {}
            startup_payload["address_type"] = "agent"
            startup_payload["address"] = new_agent
            startup_payload["component_class"] = agent_class
            startup_payload["component_number"] = agent_number
            startup_payload["short_name"] = agent_short_name
            startup_payload["properties"] = self.global_properties
            startup_payload["simulation_configuration"] = self.simulation_configuration


            if "properties" in agent_configuration.keys():
                startup_payload["local_properties"] = agent_configuration["properties"]

            startup_payload["container"] = self.myAddress
            startup_payload["environment"] = self.environment
            startup_payload["simulation_id"] = self.simulation_id
            startup_payload["simulation_run_id"] = self.simulation_run_id
            startup_payload["log_actor"] = self.log_actor
            if "run_number" in dir(self):
                startup_payload["run_number"] = self.run_number
            
            if "subjects" in dir(self):
                startup_payload["subject_id"] = self.subjects[i]["subject_id"]
                self.subject_map[self.subjects[i]["subject_id"]] = new_agent
 
            
            ###
            # Agent Initialization Message #2
            ###
            
            self.send(new_agent, StartupPayload(startup_payload=startup_payload))

            ###
            
            # self.agent_addresses.append(new_agent)
            self.agents.append(new_agent)
            
            agent_info = {}
            agent_info["address_type"] = "agent"
            agent_info["address"] = new_agent
            agent_info["component_class"] = agent_class
            agent_info["component_number"] = agent_number
            agent_info["short_name"] = agent_short_name

            self.master_address_book.add_address(agent_info["short_name"], agent_info)


    def complete_container_shutdown(self, message):
        # logging.info("Got anotehr child exit...")
        # logging.info(message)
        # logging.info(self.mes_component_list)
        if message.childAddress in self.mes_component_list:
            extract_index = self.mes_component_list.index(message.childAddress)
            self.mes_component_list.pop(extract_index)
        if len(self.mes_component_list) == 0:
            logging.info("Message to close logger: ")
            self.configuration_object.mark_finished()

            message = Message()
            message.set_directive("update_mes_run_information")
            message.set_sender(self.myAddress)
            payload = self.configuration_object
            message.set_payload(payload)
            self.send(self.dispatcher, message)



            payload = {}
            payload["status"] = self.configuration_object.status
            payload["start_time"] = str(self.configuration_object.start_time)
            payload["end_time"] = str(self.configuration_object.end_time)
            try:
                payload["total_time"] = str(self.configuration_object.end_time - self.configuration_object.start_time)
            except:
                payload["total_time"] = ""
            new_message = Message()
            new_message.set_sender(self.myAddress)
            new_message.set_directive("update_mes_status")
            # payload = message.get_payload()
            new_message.set_payload(payload)
            self.send(self.log_actor, new_message)
            
            self.send(self.myAddress, ActorExitRequest(recursive=True))
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
        
        
    def shutdown_mes(self, environment_address):
        # starting shut down process
        for mes_component in self.mes_component_list:
            self.send(mes_component, ActorExitRequest())        




    def excepted_mes_shutdown(self, environment_address, exception_payload):
        logging.info("Message to close logger: " + str(exception_payload))
        logging.info("MES CONTAINER SHOULD BE EXCEPTING OUT NOW")
        message = Message()
        message.set_directive("update_mes_status")
        message.set_sender(self.myAddress)
        payload = {}

        # message = Message()
        # message.set_directive("update_mes_status")
        # message.set_sender(self.myAddress)
        # payload = {}
        # payload["status"] = run.status
        # payload["start_time"] = str(run.start_time)
        # payload["end_time"] = str(run.end_time)
        # payload["total_time"] = str(run.end_time - run.start_time)
        # payload["exception_payload"] = exception_payload
        # message.set_payload(payload)
        # self.send(run.mes_base_address, message)
        
        


        payload["exception_payload"] = exception_payload
        message.set_payload(payload)
        # self.send(self.dispatcher, message)

        self.configuration_object.mark_excepted()
        payload = {}
        # payload["status"] = self.configuration_object.status
        # payload["start_time"] = str(self.configuration_object.start_time)
        # payload["end_time"] = str(self.configuration_object.end_time)
        # payload["total_time"] = str(self.configuration_object.end_time - self.configuration_object.start_time)
        


        message = Message()
        message.set_directive("update_mes_run_information")
        message.set_sender(self.myAddress)
        payload = self.configuration_object
        message.set_payload(payload)
        self.send(self.dispatcher, message)

        
        payload = None
        payload = {}
        # payload = message.get_payload()
        payload["exception_payload"] = exception_payload
        payload["configuration_object"] = self.configuration_object
        

        
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("finalize_mes_status")
        new_message.set_payload(payload)

        logging.info("Message to close logger: " + str(payload))
        self.send(self.log_actor, new_message)
        
        self.send(self.myAddress, ActorExitRequest())


        # for run in self.simulation_runs:
        #     if run.mes_base_address == environment_address:
        #         run.mark_excepted()

        #         message = Message()
        #         message.set_directive("update_mes_status")
        #         message.set_sender(self.myAddress)
        #         payload = {}
        #         payload["status"] = run.status
        #         payload["start_time"] = str(run.start_time)
        #         payload["end_time"] = str(run.end_time)
        #         payload["total_time"] = str(run.end_time - run.start_time)
        #         payload["exception_payload"] = exception_payload
        #         message.set_payload(payload)
        #         self.send(run.mes_base_address, message)
        #         self.send(environment_address, ActorExitRequest())

    def logger_setup(self):
        # NOTE: Important to keep a direct reference to the log actor else it will scan the source authority first
        self.log_actor = self.createActor(LogActor)
        
        log_basis = {}
        log_basis["message_type"] = "setup"

        log_configuration = {}
        log_configuration["simulation_run_id"] = self.simulation_run_id
        log_configuration["simulation_id"] = self.simulation_id
        log_configuration["run_number"] = self.run_number
        log_configuration["run_code"] = self.run_code
        log_configuration["status"] = self.status
        log_configuration["mes_directory"] = self.mes_directory
        log_configuration["data_logging"] = self.data_logging
        log_configuration["simulation_configuration"] = self.simulation_configuration
        self.send(self.log_actor, LogActorConfigurationPayload(log_actor_configuration_payload=log_configuration)) 


    def agent_action_forward(self, sender, message:Message):        
        subject_id = message.get_payload()["subject_id"]
        subject_agent_map = self.subject_map[subject_id]
        new_message = Message()
        new_message.set_directive(message.get_payload()["action"])
        new_message.set_sender(self.myAddress)
        new_message.set_payload(message.get_payload())
        self.send(subject_agent_map, new_message)


    def receiveMessage(self, message, sender):
        if not isinstance(message, ActorSystemMessage):
            if isinstance(message, Message):
                logging.info("Got a message to container...")
                logging.info(str(sender) + " -- " + str(message))
                if message.get_directive() == "excepted_mes":
                    logging.info("RECEVIED AN EXCEPTION REQUEST:" + str(message.get_payload()))
                    self.excepted_mes_shutdown(sender, message.get_payload())
                elif message.get_directive() == "shutdown_mes":
                    self.shutdown_mes(sender)
                elif message.get_directive() == "agent_action_forward":
                    self.agent_action_forward(sender, message)


        elif isinstance(message, ChildActorExited):
            self.complete_container_shutdown(message)
            

                
        


    # ##### Important things here
    # def prep_mes(self):
    #     ####
    #     # Setup Institution(s) for the MES    
    #     # This preps configuration, but won't intitiate instantiation
    #     ####

    #     institutions = []
    #     institution_requests = []
    #     if "institution" in configuration.keys():
    #         institution_request = ComponentRequest()
    #         institution_request.source_hash=source_hash
    #         institution_request.number=agent_d["number"]
    #         institution_request.source_class=agent_d["agent_name"]
            
    #         institutions = [configuration["institution"]]
    #     elif "institutions" in configuration.keys():
    #         institutions = configuration["institutions"]
    #         # if len(configuration["institutions"]) == 1:
    #         #     institutions = [configuration["institutions"]]
    #         # else:
    #         #     pass
    #         #     # for institution_d in configuration["institutions"]:
    #                 # institution_class = institution_d
    #                 # institutions.append(institution_class)

    #     ####
    #     # Setup Agent(s) for the MES    
    #     # This preps configuration, but won't intitiate instantiation
    #     ####
        
    #     agents = []
    #     agent_requests = []
    #     for agent_d in configuration["agents"]:
    #         agent_type = agent_d["agent_name"]
    #         agent_count = agent_d["number"]

    #         agent_count = agent_d["number"]
    #         agent_count = agent_d["number"]
            


    #         # message.set_payload({"agent_class": agent[0], "num_agents": agent[1], "source_hash": source_hash})
            
    #         agent_request = ComponentRequest()
    #         agent_request.source_hash=source_hash
    #         agent_request.number=agent_d["number"]
    #         agent_request.source_class=agent_d["agent_name"]
    #         agent_requests.append(agent_request)
            
    #         agents.append((agent_type, agent_count))
    #         # for i in range(0, agent_count):
    #         #     agents.append((agent_type, 1))


    #     #### PROBABLY DEPRECATED AS INCLUDED IN ENVIRONMENT STARTUP        
    #     # if "properties" in configuration.keys():
    #     #     message = Message()
    #     #     message.set_directive("simulation_properties")
    #     #     message.set_sender(self.myAddress)
    #     #     payload = {"properties": configuration["properties"],  "dispatcher":self.myAddress}
    #     #     payload["simulation_id"] = configuration["id"]
    #     #     payload["simulation_run_id"] = configuration["simulation_run_id"]
            
    #     #     if run_number is not None:
    #     #         payload["run_number"] = run_number
    #     #     message.set_payload(payload)
            
    #     #     self.send(environment, message)

        

    #     # if 'institutions' not in locals():
    #     #     message = Message()
    #     #     message.set_directive("setup_institution")
    #     #     message.set_payload({"order": 2, "institution_class": institution, "source_hash": source_hash})
    #     #     self.send(environment, message)
    #     # else:
        
    #     for index, setup_inst in enumerate(institutions):
    #         order = index + 1
    #         message = Message()
    #         message.set_directive("setup_institution")
    #         if isinstance(setup_inst, dict):
    #             message.set_payload({"order": order, "institution_class": setup_inst["institution"], "source_hash": source_hash})    
    #         else:
    #             message.set_payload({"order": order, "institution_class": institutions, "source_hash": source_hash})
    #         self.send(environment, message)

    #     # if hasattr(self, 'agent_memory_prepared'):
    #     #     for agent in zip(agents, self.agent_memory):
    #     #         message = Message()
    #     #         message.set_directive("setup_agents")
    #     #         message.set_payload({"agent_class": agent[0][0], "num_agents": agent[0][1], "agent_memory": agent[1], "source_hash": source_hash})
    #     #         self.send(environment, message)
    #     # else:
        
        
    #     # TODO replace with agent requests
    #     for agent in agents:
    #         message = Message()
    #         message.set_directive("setup_agents")
    #         message.set_payload({"agent_class": agent[0], "num_agents": agent[1], "source_hash": source_hash})
    #         self.send(environment, message)

    #     # for agent_request in agent_requests:
    #     #     message = Message()
    #     #     message.set_directive("setup_agent_requests")
    #     #     message.set_payload(agent_request)
    #     #     self.send(environment, message)

    #     start_message = Message()
    #     start_message.set_sender("experimenter")
    #     start_message.set_directive("distribute_address_book")
    #     self.send(environment, start_message)
        

    #     start_message = Message()
    #     start_message.set_sender("experimenter")
    #     start_message.set_directive("start_environment")
    #     self.send(environment, start_message)
    #     logging.info('Simulation environment should have started')
