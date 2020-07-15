from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *

#from socketIO_client import SocketIO, LoggingNamespace

import logging
import json

EXPERIMENT_DATA = 27


class LogActor(Actor):
    def experiment_log(self, log_message):
        #self.mTree_logger().log(25, log_message)
        pass


    def __str__(self):
        return "<LogActor: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        #socketIO = SocketIO('127.0.0.1', 5000, LoggingNamespace)
        self.mtree_properties = {}
        self.simulation_id = None
        self.run_number = None
    
    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None

    def log_message(self, message):
        if self.simulation_id is not None:
            message["simulation_id"] = self.simulation_id
        if self.run_number is not None:
            message["run_number"] = self.run_number
            
        logging.log(EXPERIMENT_DATA, message)

    def receiveMessage(self, message, sender):
        #print("AGENT GOT MESSAGE: " + message)
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        if isinstance(message, PoisonMessage):
            logging.exception("Poison HAPPENED: %s -- %s", self, message)
        elif isinstance(message, ActorExitRequest):
            logging.exception("ActorExitRequest: %s -- %s", self, message)
        elif isinstance(message, ChildActorExited):
            logging.exception("ChildActorExited: %s -- %s", self, message)
        else:
            try:
                if "message_type" in message.keys():
                    self.simulation_id = message["simulation_id"]
                    if "run_number" in message.keys():
                        self.run_number = message["run_number"]
                else:
                    self.log_message(message)
                    
            except Exception as e:
                logging.exception("EXCEPTION HAPPENED: %s -- %s -- %s", self, message, e)
                self.actorSystemShutdown()
