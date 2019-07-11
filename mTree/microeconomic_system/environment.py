from thespian.actors import *
from datetime import timedelta

import logging

from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *

import json



@directive_enabled_class
class Environment(Actor):
    def mTree_logger(self):
        return logging.getLogger("mTree")

    def experiment_log(self, *log_message):
        self.mTree_logger().log(25, log_message)


    def __str__(self):
        return "<Environment: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        self.institutions = []
        self.agents = []
        self.mtree_properties = {}

    def close_environment(self):
        #asys.shutdown()
        pass

    def receiveMessage(self, message, sender):
        #print("ENV GOT MESSAGE: " + message)
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        logging.info("MESSAGE RCVD: %s DIRECTIVE: %s SENDER: %s", self, message, sender)
        try:
            directive_handler = self._enabled_directives.get(message.get_directive())
            print("DIRECTIVE HANDLING")
            print(message)
            directive_handler(self, message)
        except Exception as e:
            logging.exception("EXCEPTION HAPPENED: %s -- %s -- %s", self, message, e)
            self.actorSystemShutdown()

    def setup_agent(self, message):
        print("got a message")
        print(message)

    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None

    @directive_decorator("simulation_properties")
    def simulation_properties(self, message: Message):
        print("RECEIVED PROPERTIES")
        if "mtree_properties" not in dir(self):
            self.mtree_properties = {}


        self.mtree_properties = message.get_payload()["properties"]
        self.simulation_id = message.get_payload()["simulation_id"]
        if "run_number" in message.get_payload().keys():
            self.run_number = message.get_payload()["run_number"]

    @directive_decorator("setup_agents")
    def setup_agents(self, message:Message):
        if "agents" not in dir(self):
            self.agents = []
        # ensure that the actor system and institution are running...
        #message = MessageSpace.create_agent(agent_class)
        num_agents = message.get_payload()["num_agents"]
        agent_class = message.get_payload()["agent_class"]

        for i in range(num_agents):
            new_agent = self.createActor(agent_class)
            self.agents.append([new_agent, agent_class, agent_class.__name__])
            new_message = Message()
            new_message.set_sender(self.myAddress)
            new_message.set_directive("simulation_properties")
            payload = {"properties": self.mtree_properties}
            new_message.set_payload(payload)
            self.send(new_agent, new_message)

    @directive_decorator("setup_institution")
    def create_institution(self, message:Message):
        if "institutions" not in dir(self):
            self.institutions = []

        institution_class = message.get_payload()["institution_class"]
        new_institution = self.createActor(institution_class)
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("simulation_properties")
        payload = {"properties": self.mtree_properties}
        new_message.set_payload(payload)
        self.send(new_institution, new_message)

        self.institutions.append(new_institution)

    def list_agents(self):
        message = MessageSpace.list_agents()
        #return asys.ask(self.institutions, message, timedelta(seconds=1.5))

    def get_agents_wealth(self):
        message = MessageSpace.get_wealths()
        print("Message: {}".format(message))
        #return asys.ask(self.institutions, message, timedelta(seconds=1.5))