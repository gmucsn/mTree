from thespian.actors import *
from datetime import timedelta

import logging

from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor



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
        self.log_actor = None
        self.simulation_id = None
        self.run_number = None
        self.institutions = []
        self.agents = []
        self.agent_addresses = []
        self.mtree_properties = {}

    def close_environment(self):
        #asys.shutdown()
        pass

    def end_round(self):
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("end_round")
        payload = {}
        payload["agents"] = self.agent_addresses
        new_message.set_payload(payload)
        self.send(self.dispatcher, new_message)
        
    def receiveMessage(self, message, sender):
        #print("ENV GOT MESSAGE: " + message)
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        if isinstance(message, PoisonMessage):
            #logging.exception("Poison HAPPENED: %s -- %s", self, message)
            pass
        elif isinstance(message, ActorExitRequest):
            #logging.exception("ActorExitRequest: %s -- %s", self, message)
            pass
        elif isinstance(message, ChildActorExited):
            #logging.exception("ChildActorExited: %s -- %s", self, message)
            pass
        else:
            try:
                directive_handler = self._enabled_directives.get(message.get_directive())
                directive_handler(self, message)
            except Exception as e:
                logging.exception("EXCEPTION HAPPENED: %s -- %s -- %s", self, message, e)
                self.actorSystemShutdown()

    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None


    @directive_decorator("initialize_log_actor")
    def initialize_log_actor(self, message:Message):
        self.log_actor = self.createActor(LogActor)
        log_basis = {}
        log_basis["message_type"] = "setup"
        log_basis["simulation_id"] = self.simulation_id
        if hasattr(self, 'run_number'):
            log_basis["run_number"] = self.run_number
        self.send(self.log_actor, log_basis)        




    def log_experiment_data(self, data):
        self.send(self.log_actor, data)

    @directive_decorator("simulation_properties")
    def simulation_properties(self, message: Message):
        self.dispatcher = message.get_payload()["dispatcher"]
        self.log_actor = message.get_payload()["log_actor"]
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
            self.agent_addresses = []
        # ensure that the actor system and institution are running...
        #message = MessageSpace.create_agent(agent_class)
        num_agents = message.get_payload()["num_agents"]
        agent_class = message.get_payload()["agent_class"]
        memory = False
        agent_memory = None
        if "agent_memory" in message.get_payload().keys():
            memory = True
            agent_memory = message.get_payload()["agent_memory"]

        for i in range(num_agents):
            new_agent = self.createActor(agent_class)
            self.agent_addresses.append(new_agent)
            self.agents.append([new_agent, agent_class, agent_class.__name__])
            new_message = Message()
            new_message.set_sender(self.myAddress)
            new_message.set_directive("simulation_properties")
            payload = {}
            #if "mtree_properties" not in dir(self):
            payload["log_actor"] = self.log_actor
            payload["dispatcher"] = self.dispatcher
            payload["properties"] = self.mtree_properties
            if memory:
                payload["agent_memory"] = agent_memory
            new_message.set_payload(payload)
            self.send(new_agent, new_message)

    @directive_decorator("setup_institution")
    def create_institution(self, message:Message):
        print("GETTING INSTITUTION ReADY")
        if "institutions" not in dir(self):
            self.institutions = []

        institution_class = message.get_payload()["institution_class"]
        new_institution = self.createActor(institution_class)
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("simulation_properties")
        payload = {}
        #if "mtree_properties" not in dir(self):
        payload["log_actor"] = self.log_actor
        payload["dispatcher"] = self.dispatcher
        payload["environment"] = self.myAddress
        payload["properties"] = self.mtree_properties
        payload["simulation_id"] = self.simulation_id
        if "run_number" in dir(self):
            payload["run_number"] = self.run_number


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