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
import sys

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

    def get_simulation_property(self, name):
        if name not in self.mtree_properties.keys():
            raise Exception("Simulation property: " + str(name) + " not available")
        return self.mtree_properties[name]


    def __str__(self):
        return "<Institution: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    
    def reminder(self, seconds_to_reminder, message, addresses=None):
        if addresses is None:
            if type(seconds_to_reminder) is timedelta:
                self.wakeupAfter( seconds_to_reminder, payload=message)    
            else:
                # TODO if not seconds then reject
                self.wakeupAfter( timedelta(seconds=seconds_to_reminder), payload=message)

        else:
            new_message = Message()
            new_message.set_directive("external_reminder")
            new_message.set_sender(self.myAddress)
            payload = {}
            payload["reminder_message"] = message
            payload["seconds_to_reminder"] = seconds_to_reminder
            new_message.set_payload(payload)

            for agent in addresses:
                self.send(agent, new_message)                

    @directive_decorator("external_reminder")
    def external_reminder(self, message:Message):
        reminder_message = message.get_payload()["reminder_message"]
        seconds_to_reminder = message.get_payload()["seconds_to_reminder"]
        self.reminder(seconds_to_reminder, reminder_message)

    def receiveMessage(self, message, sender):
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        if not isinstance(message, ActorSystemMessage):
            try:
                directive_handler = self._enabled_directives.get(message.get_directive())
                directive_handler(self, message)
            except Exception as e:
                error_type, error, tb = sys.exc_info()
                error_message = "MES INSITUTION CRASHING - EXCEPTION FOLLOWS \n"
                error_message += "\tSource Message: " + str(message) + "\n"
                error_message += "\tError Type: " + str(error_type) + "\n"
                error_message += "\tError: " + str(error) + "\n"
                
                traces = traceback.extract_tb(tb)
                trace_output = "\tTrace Output: \n"
                for trace_line in traceback.format_list(traces):
                    trace_output += "\t" + trace_line + "\n"
                error_message += "\n"
                error_message += trace_output
                self.log_message(error_message)
                
                # self.log_message("MES AGENT CRASHING - EXCEPTION FOLLOWS")
                # self.log_message("\tSource Message: " + str(message))
                # filename, lineno, func_name, line = traceback.extract_tb(tb)[-1]
                # self.log_message("\tError Type: " + str(error_type))
                # self.log_message("\tError: " + str(error))
                # self.log_message("\tFilename: " + str(filename))
                # self.log_message("\tLine Number: " + str(lineno))
                # self.log_message("\tFunction Name: " + str(func_name))
                # self.log_message("\tLine: " + str(line))
                
                
                #self.actorSystemShutdown()
        elif isinstance(message, WakeupMessage):
            try:
                wakeup_message = message.payload
                directive_handler = self._enabled_directives.get(wakeup_message.get_directive())
                directive_handler(self, wakeup_message)
            except Exception as e:
                self.log_message("MES CRASHING - EXCEPTION FOLLOWS")
                self.log_message("\tSource Message: " + str(message))
                
                self.log_message(traceback.format_exc())
                self.actorSystemShutdown()
        
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

        if "institution_info" in message.get_payload().keys():
            self.institution_info = message.get_payload()["institution_info"]
            self.short_name = message.get_payload()["institution_info"]["short_name"]
            
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

