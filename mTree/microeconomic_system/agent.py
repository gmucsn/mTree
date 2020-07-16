from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *

#from socketIO_client import SocketIO, LoggingNamespace

import logging
import json

EXPERIMENT = 25


@directive_enabled_class
class Agent(Actor):
    environment = None

    #def mTree_logger(self):
    #    return logging.getLogger("mTree")

    def experiment_log(self, log_message):
        self.mTree_logger().log(25, log_message)


    def __str__(self):
        return "<Agent: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        #socketIO = SocketIO('127.0.0.1', 5000, LoggingNamespace)
        self.log_actor = None
        self.mtree_properties = {}
        self.agent_memory = {}

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


    def log_experiment_data(self, data):
        self.send(self.log_actor, data)

    @directive_decorator("simulation_properties")
    def simulation_properties(self, message: Message):
        if "mtree_properties" not in dir(self):
            self.mtree_properties = {}
        if "agent_memory" not in dir(self):
            self.agent_memory = {}
        

        if "properties" in message.get_payload().keys():
            self.mtree_properties = message.get_payload()["properties"]
        self.log_actor = message.get_payload()["log_actor"]
        self.dispatcher = message.get_payload()["dispatcher"]
        if "agent_memory" in message.get_payload().keys():
            print("setting my memory to... ", message.get_payload()["agent_memory"])
            self.agent_memory = message.get_payload()["agent_memory"]
        else:
            self.agent_memory = {}

    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None

    def receiveMessage(self, message, sender):
        #print("AGENT GOT MESSAGE: ", message) # + message)
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        if not isinstance(message, ActorSystemMessage):
            try:
                directive_handler = self._enabled_directives.get(message.get_directive())
                directive_handler(self, message)
            except Exception as e:
                logging.exception("EXCEPTION HAPPENED: %s -- %s -- %s", self, message, e)
                #self.actorSystemShutdown()
                
            
