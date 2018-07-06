from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *

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
        print("Agent started")


    def receiveMessage(self, message, sender):
        self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        directive_handler = self._enabled_directives.get(message.get_directive())
        directive_handler(self, message)
