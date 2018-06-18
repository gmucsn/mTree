from thespian.actors import *
from datetime import timedelta

import logging

from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *

@directive_enabled_class
class Environment(Actor):
    def __init__(self):
        self.institutions = []
        self.agents = []

    def close_environment(self):
        #asys.shutdown()
        pass

    def receiveMessage(self, message, sender):
        logging.info('Hello got: %s', message)
        directive_handler = self._enabled_directives.get(message.get_directive())
        directive_handler(self, message)

    def setup_agent(self, message):
        print("got a message")
        print(message)

    @directive_decorator("setup_agents")
    def setup_agents(self, message:Message):
        # ensure that the actor system and institution are running...
        #message = MessageSpace.create_agent(agent_class)
        num_agents = message.get_payload()["num_agents"]
        agent_class = message.get_payload()["agent_class"]
        for i in range(num_agents):
            new_agent = self.createActor(agent_class)
            self.agents.append(new_agent)

    @directive_decorator("setup_institution")
    def create_institution(self, message:Message):
        institution_class = message.get_payload()["institution_class"]

        new_institution = self.createActor(institution_class)
        self.institutions.append(new_institution)

    def list_agents(self):
        message = MessageSpace.list_agents()
        #return asys.ask(self.institutions, message, timedelta(seconds=1.5))

    def get_agents_wealth(self):
        message = MessageSpace.get_wealths()
        print("Message: {}".format(message))
        #return asys.ask(self.institutions, message, timedelta(seconds=1.5))