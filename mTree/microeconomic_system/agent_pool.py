from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *

import logging
import json


@directive_enabled_class
class AgentPool(Actor):
    def mTree_logger(self):
        return logging.getLogger("mTree")

    def experiment_log(self, log_message):
        self.mTree_logger().log(25, log_message)


    def __str__(self):
        return "<AgentPool: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        print("AgentPool started")
        self.agents = []


    def receiveMessage(self, message, sender):
        self.mTree_logger().info('%s got: %s', self, message)
        directive_handler = self._enabled_directives.get(message.get_directive())
        directive_handler(self, message)

    @directive_decorator("add_agent")
    def add_agents(self, message: Message):
        # ensure that the actor system and institution are running...
        # message = MessageSpace.create_agent(agent_class)
        num_agents = message.get_payload()["num_agents"]
        agent_class = message.get_payload()["agent_class"]
        for i in range(num_agents):
            new_agent = self.createActor(agent_class)
            self.agents.append(new_agent)

    @directive_decorator("request_available_agent")
    def request_available_agent(self, message: Message):
        # ensure that the actor system and institution are running...
        # message = MessageSpace.create_agent(agent_class)
        num_agents = message.get_payload()["num_agents"]
        agent_class = message.get_payload()["agent_class"]
        for i in range(num_agents):
            new_agent = self.createActor(agent_class)
            self.agents.append(new_agent)