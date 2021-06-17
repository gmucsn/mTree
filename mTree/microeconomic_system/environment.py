from thespian.actors import *
from datetime import datetime, timedelta
  
import logging

from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.log_message import LogMessage
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
from mTree.microeconomic_system.address_book import AddressBook
import time

import traceback
import json
import os



@directive_enabled_class
class Environment(Actor):
    def __init__(self):
        self.address_book = AddressBook(self)
        self.log_actor = None
        self.simulation_id = None
        self.run_number = None
        self.institutions = []
        self.agents = []
        self.agent_addresses = []
        self.mtree_properties = {}

    def __str__(self):
        return "<Environment: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    

    def close_environment(self):
        #asys.shutdown()
        pass

    def get_simulation_property(self, name):
        if name not in self.mtree_properties.keys():
            raise Exception("Simulation property: " + str(name) + " not available")
        return self.mtree_properties[name]

    
    def end_round(self):
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("end_round")
        payload = {}
        payload["agents"] = self.agent_addresses
        new_message.set_payload(payload)
        self.dispatcher = self.createActor("Dispatcher", globalName="dispatcher")
        self.send(self.dispatcher, new_message)

        for agent in self.agent_addresses:
            new_message = Message()
            new_message.set_sender(self.myAddress)
            new_message.set_directive("store_agent_memory")
            self.send(agent, message)
            
        
    def receiveMessage(self, message, sender):
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        if not isinstance(message, ActorSystemMessage):
            try:
                directive_handler = self._enabled_directives.get(message.get_directive())
                directive_handler(self, message)
            except Exception as e:
                self.log_message("MES ENVIRONMENT CRASHING - EXCEPTION FOLLOWS")
                self.log_message(traceback.format_exc())
                self.actorSystemShutdown()
        elif isinstance(message, WakeupMessage):
            try:
                wakeup_message = message.payload
                directive_handler = self._enabled_directives.get(wakeup_message.get_directive())
                directive_handler(self, wakeup_message)
            except Exception as e:
                self.log_message("MES CRASHING - EXCEPTION FOLLOWS")
                self.log_message(traceback.format_exc())
                self.actorSystemShutdown()

    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None


    @directive_decorator("initialize_log_actor")
    def initialize_log_actor(self, message:Message):
        self.log_actor = self.createActor("log_actor.LogActor")
        log_basis = {}
        log_basis["message_type"] = "setup"
        log_basis["simulation_id"] = self.simulation_id
        if hasattr(self, 'run_number'):
            log_basis["run_number"] = self.run_number
        self.send(self.log_actor, log_basis)        

    @directive_decorator("logger_setup")
    def logger_setup(self, message:Message):
        self.log_actor = self.createActor("log_actor.LogActor") #, globalName="log_actor")
        
        log_basis = {}
        log_basis["message_type"] = "setup"

        log_basis["simulation_run_id"] = message.get_payload()["simulation_run_id"]
        log_basis["simulation_id"] = message.get_payload()["simulation_id"]
        log_basis["mes_directory"] = message.get_payload()["mes_directory"]
        log_basis["data_logging"] = message.get_payload()["data_logging"]
        self.send(self.log_actor, log_basis) 
        
    def log_message(self, logline):
        log_message = LogMessage(message_type="log", content=logline)
        self.send(self.log_actor, log_message)

    def log_data(self, logline):
        log_message = LogMessage(message_type="data", content=logline)
        self.send(self.log_actor, log_message)


    def record_data(self, data):
        #self.log_actor = self.createActor(LogActor, globalName="log_actor")
        self.send(self.log_actor, data)

    @directive_decorator("simulation_properties")
    def simulation_properties(self, message: Message):
        #self.dispatcher = self.createActor("Dispatcher", globalName="dispatcher")
        #self.log_actor = message.get_payload()["log_actor"]
        if "mtree_properties" not in dir(self):
            self.mtree_properties = {}

        self.mtree_properties = message.get_payload()["properties"]
        self.simulation_id = message.get_payload()["simulation_id"]
        self.simulation_run_id = message.get_payload()["simulation_run_id"]
        if "run_number" in message.get_payload().keys():
            self.run_number = message.get_payload()["run_number"]

    @directive_decorator("setup_agents")
    def setup_agents(self, message:Message):
        if "address_book" not in dir(self):
            self.address_book = AddressBook(self)        

        if "agents" not in dir(self):
            self.agents = []
            self.agent_addresses = []
        # ensure that the actor system and institution are running...
        #message = MessageSpace.create_agent(agent_class)
        num_agents = message.get_payload()["num_agents"]
        agent_class = message.get_payload()["agent_class"]
        
        # need to check source hash for simulation
        source_hash = message.get_payload()["source_hash"]
        
        # memory = False
        # agent_memory = None
        # if "agent_memory" in message.get_payload().keys():
        #     memory = True
        #     agent_memory = message.get_payload()["agent_memory"]
        for i in range(num_agents):
        
            new_agent = self.createActor(agent_class, sourceHash=source_hash)
            
            self.agent_addresses.append(new_agent)
            self.agents.append([new_agent, agent_class])
            agent_number = i + 1
            agent_info = {}
            agent_info["address_type"] = "agent"
            agent_info["address"] = new_agent
            agent_info["component_class"] = agent_class
            agent_info["component_number"] = agent_number
            agent_info["short_name"] = agent_class + " " + str(agent_number)

            self.address_book.add_address(agent_info["short_name"], agent_info)

            new_message = Message()
            #new_message.set_sender(self.myAddress)
            new_message.set_directive("simulation_properties")
            payload = {}
            #if "mtree_properties" not in dir(self):
            payload["log_actor"] = self.log_actor
            #payload["dispatcher"] = self.createActor("Dispatcher", globalName="dispatcher")
            payload["properties"] = self.mtree_properties
            # if memory:
            #     payload["agent_memory"] = agent_memory
            new_message.set_payload(payload)
            self.send(new_agent, new_message)

        

    @directive_decorator("setup_institution")
    def create_institution(self, message:Message):
        if "institutions" not in dir(self):
            self.institutions = []

        if "address_book" not in dir(self):
            self.address_book = AddressBook(self)
        

        institution_class = message.get_payload()["institution_class"]
        source_hash = message.get_payload()["source_hash"]
        
        new_institution = self.createActor(institution_class, sourceHash=source_hash)
        institution_info = {}
        institution_info["address_type"] = "institution"
        institution_info["address"] = new_institution
        institution_info["component_class"] = institution_class
        institution_info["component_number"] = 1
        institution_info["short_name"] = institution_class
        self.address_book.add_address(institution_info["short_name"], institution_info)


        new_message = Message()
        #new_message.set_sender(self.myAddress)
        new_message.set_directive("simulation_properties")
        payload = {}

        
        #if "mtree_properties" not in dir(self):
        #payload["dispatcher"] = self.createActor("Dispatcher", globalName="dispatcher")
        payload["environment"] = self.myAddress
        payload["properties"] = self.mtree_properties
        payload["simulation_id"] = self.simulation_id
        payload["simulation_run_id"] = self.simulation_run_id
        payload["log_actor"] = self.log_actor
        if "run_number" in dir(self):
            payload["run_number"] = self.run_number

        new_message.set_payload(payload)
        self.send(new_institution, new_message)

        self.institutions.append(new_institution)

    def list_agents(self):
        message = MessageSpace.list_agents()
        #return asys.ask(self.institutions, message, timedelta(seconds=1.5))

    def get_agents_wealth(self):
        message = MessageSpace.get_wealths()
        print("Message: {}".format(message))
        #return asys.ask(self.institutions, message, timedelta(seconds=1.5))