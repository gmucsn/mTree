from thespian.actors import *
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
import uuid
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *

import logging
import json



class Institution(Actor):
    def mTree_logger(self):
        return logging.getLogger("mTree")

    def experiment_log(self, *log_message):
        self.mTree_logger().log(25, log_message)



    def __str__(self):
        return "<Institution: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        self.agents = []
        self.agent_ids = []

    def receiveMessage(self, message, sender):
        self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        directive_handler = self._enabled_directives.get(message.get_directive())
        directive_handler(self, message)


    def add_agent(self, agent_class):
        agent_id = str(uuid.uuid1())

#        agent = asys.createActor(agent_class, globalName = agent_id)
        agent = self.createActor(agent_class)  # creates agent as child of institution
        self.agents.append(agent)
        self.agent_ids.append(agent_id)

