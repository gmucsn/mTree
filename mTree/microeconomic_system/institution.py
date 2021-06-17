from thespian.actors import *
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.log_message import LogMessage
from mTree.microeconomic_system.address_book import AddressBook

import uuid
from mTree.microeconomic_system.message_space import MessageSpace

from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
import logging
import json
import traceback
from datetime import datetime, timedelta
import time

class Institution(Actor):
    def __init__(self):
        self.address_book = AddressBook(self)
        self.log_actor = None
        self.dispatcher = None
        self.run_number = None
        self.agents = []
        self.agent_ids = []
        self.mtree_properties = {}



    def log_message(self, logline):
        log_message = LogMessage(message_type="log", content=logline)
        self.send(self.log_actor, log_message)

    def log_data(self, logline):
        log_message = LogMessage(message_type="data", content=logline)
        self.send(self.log_actor, log_message)

    def __str__(self):
        return "<Institution: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    
    def receiveMessage(self, message, sender):
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        if not isinstance(message, ActorSystemMessage):
            try:
                directive_handler = self._enabled_directives.get(message.get_directive())
                directive_handler(self, message)
            except Exception as e:
                self.log_message("MES INSTITUTION CRASHING - EXCEPTION FOLLOWS")
                self.log_message(traceback.format_exc())
                #self.actorSystemShutdown()
        
    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None

    def log_experiment_data(self, data):
        #self.log_actor = self.createActor(LogActor, globalName="log_actor")
        self.send(self.log_actor, data)

    @directive_decorator("address_book_update")
    def address_book_update(self, message: Message):
        addresses = message.get_payload()
        self.address_book.merge_addresses(addresses)
        

    @directive_decorator("simulation_properties")
    def simulation_properties(self, message: Message):
        if "address_book" not in dir(self):
            self.address_book = AddressBook(self)
        
        self.log_actor = message.get_payload()["log_actor"]
        if "mtree_properties" not in dir(self):
            self.mtree_properties = {}

        if "properties" in message.get_payload().keys():
            self.mtree_properties = message.get_payload()["properties"]
        self.simulation_id = message.get_payload()["simulation_id"]
        if "run_number" in message.get_payload().keys():
            self.run_number = message.get_payload()["run_number"]
        #self.log_actor = message.get_payload()["log_actor"]
        #self.dispatcher = message.get_payload()["dispatcher"]
        #self.dispatcher = self.createActor("Dispatcher", globalName="dispatcher")
        
        self.environment = message.get_payload()["environment"]

    def add_agent(self, agent_class):
        if "agents" not in dir(self):
            self.agents = []
            self.agent_ids = []

        agent_id = str(uuid.uuid1())

#        agent = asys.createActor(agent_class, globalName = agent_id)
        agent = self.createActor(agent_class)  # creates agent as child of institution
        self.agents.append(agent)
        self.agent_ids.append(agent_id)

