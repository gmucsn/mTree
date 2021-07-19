from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.log_message import LogMessage
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
from mTree.microeconomic_system.address_book import AddressBook
#from socketIO_client import SocketIO, LoggingNamespace
import traceback
import logging
import json
from datetime import datetime, timedelta
import time
import sys


@directive_enabled_class
class Agent(Actor):
    def __init__(self):
        self.address_book = AddressBook(self)
        #socketIO = SocketIO('127.0.0.1', 5000, LoggingNamespace)
        self.log_actor = None
        self.mtree_properties = {}
        self.agent_memory = {}
        self.outlets = {}

    environment = None

    def get_simulation_property(self, name):
        if name not in self.mtree_properties.keys():
            raise Exception("Simulation property: " + str(name) + " not available")
        return self.mtree_properties[name]

    def log_message(self, logline):
        log_message = LogMessage(message_type="log", content=logline)
        self.send(self.log_actor, log_message)

    def log_data(self, logline):
        log_message = LogMessage(message_type="data", content=logline)
        self.send(self.log_actor, log_message)
        
    def __str__(self):
        return "<Agent: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()


        
    def __setattr__(self, key, value):
        """
        magic function that passes change to the root object
        :param key:
        :param value:
        :return:
        """
        super().__setattr__(key, value)
        if hasattr(self, 'outlets'):
            if key in self.outlets:
                print("LETTING: " + str(self.user) + " -- " + str(self.outlets[key]) + " -- " + str(value))

                self.response.let_user(self.user_id, self.outlets[key], value)
                

    @directive_decorator("register_subject_connection")
    def register_subject_connection(self, message: Message):
        self.subject_id = "TEST!" #message.get_payload()["subject_id"]

    @directive_decorator("store_agent_memory")
    def store_agent_memory(self, message: Message):
        self.subject_id = "TEST!" #message.get_payload()["subject_id"]
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("store_agent_memory")
        new_message.set_payload({"agent_memory": self.agent_memory})
        self.send(self.dispatcher, new_message)

    @directive_decorator("simulation_properties")
    def simulation_properties(self, message: Message):
        self.address_book = AddressBook(self)
        
        self.log_actor = message.get_payload()["log_actor"]
        if "mtree_properties" not in dir(self):
            self.mtree_properties = {}
        # if "agent_memory" not in dir(self):
        #     self.agent_memory = {}
        

        if "properties" in message.get_payload().keys():
            self.mtree_properties = message.get_payload()["properties"]

        if "agent_information" in message.get_payload().keys():
            self.short_name = message.get_payload()["agent_information"]["short_name"]
            self.agent_information = message.get_payload()["agent_information"]

        #self.log_actor = message.get_payload()["log_actor"]
        #self.dispatcher = message.get_payload()["dispatcher"]
        #self.dispatcher = self.createActor("Dispatcher", globalName="dispatcher")
        
        # if "agent_memory" in message.get_payload().keys():
        #     print("setting my memory to... ", message.get_payload()["agent_memory"])
        #     self.agent_memory = message.get_payload()["agent_memory"]
        # else:
        #     self.agent_memory = {}

    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None

    def register_outlet(self, _property, target):  # _property used due to builtin use of property
        self.outlets[_property] = target


    def receiveMessage(self, message, sender):
        #print("AGENT GOT MESSAGE: ", message) # + message)
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        if not isinstance(message, ActorSystemMessage):
            try:
                directive_handler = self._enabled_directives.get(message.get_directive())
                directive_handler(self, message)
            except Exception as e:
                self.log_message("MES AGENT CRASHING - EXCEPTION FOLLOWS")
                self.log_message("\tSource Message: " + str(message))
                error_type, error, tb = sys.exc_info()
                filename, lineno, func_name, line = traceback.extract_tb(tb)[-1]
                self.log_message("\tError Type: " + str(error_type))
                self.log_message("\tError: " + str(error))
                self.log_message("\tFilename: " + str(filename))
                self.log_message("\tLine Number: " + str(lineno))
                self.log_message("\tFunction Name: " + str(func_name))
                self.log_message("\tLine: " + str(line))
                
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
            
