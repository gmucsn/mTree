from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *

from socketIO_client import SocketIO, LoggingNamespace

import logging
import json


@directive_enabled_class
class Agent(Actor):
    environment = None

    def mTree_logger(self):
        return logging.getLogger("mTree")

    def experiment_log(self, log_message):
        self.mTree_logger().log(25, log_message)


    def __str__(self):
        return "<Agent: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        #socketIO = SocketIO('127.0.0.1', 5000, LoggingNamespace)
        print("Agent started")

    @directive_decorator("register_subject_connection")
    def register_subject_connection(self, message: Message):
        self.subject_id = "TEST!" #message.get_payload()["subject_id"]

    def receiveMessage(self, message, sender):
        #print("AGENT GOT MESSAGE: " + message)
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        logging.info("AGENT: MESSAGE RECEIVED")
        directive_handler = self._enabled_directives.get(message.get_directive())
        directive_handler(self, message)
