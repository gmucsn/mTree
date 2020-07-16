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
        self.log_actor = None
        self.dispatcher = None
        self.run_number = None
        self.agents = []
        self.agent_ids = []
        self.mtree_properties = {}

    def receiveMessage(self, message, sender):
        #print("INST GOT MESSAGE: " + message)
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        if not isinstance(message, ActorSystemMessage):
            try:
                directive_handler = self._enabled_directives.get(message.get_directive())
                directive_handler(self, message)
            except Exception as e:
                logging.exception("EXCEPTION HAPPENED: %s -- %s -- %s", self, message, e)
                #self.actorSystemShutdown()
        
    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None

    def log_experiment_data(self, data):
        self.send(self.log_actor, data)

    @directive_decorator("simulation_properties")
    def simulation_properties(self, message: Message):
        if "mtree_properties" not in dir(self):
            self.mtree_properties = {}

        if "properties" in message.get_payload().keys():
            self.mtree_properties = message.get_payload()["properties"]
        self.simulation_id = message.get_payload()["simulation_id"]
        if "run_number" in message.get_payload().keys():
            self.run_number = message.get_payload()["run_number"]
        self.log_actor = message.get_payload()["log_actor"]
        self.dispatcher = message.get_payload()["dispatcher"]
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

