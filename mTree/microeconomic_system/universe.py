from thespian.actors import *
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
import sys
from datetime import timedelta

class Universe:
    def __init__(self, actor_system):
        self.environments = None
        self.actor_system = actor_system

    def add_environment(self, environment_class):
        environment = self.actor_system.createActor(environment_class)
        self.environments = environment

    def add_institution(self, institution_class):
        #message = msg.create_institution(institution_class)
        #self.actor_system.tell(self.environments, message)
        pass

    def create_agents(self, agent):
        #message = msg.create_agent(agent)
        #self.actor_system.tell(self.environments, message)
        pass

    def start_institutions(self):
        print("THISISIS")
        #message = msg.start_institution(AuctionInstitution)
        #self.actor_system.tell(self.environments, message)


    def register_good(self, value):
        print("registering good")
        #message = msg.register_good(value)
        #self.actor_system.tell(self.environments, message)

