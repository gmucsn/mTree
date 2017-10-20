from thespian.actors import *
from datetime import timedelta

from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message

class Environment(Actor):
    def __init__(self):
        self.institutions = []
        self.agents = []

    def add_institution(self, institution_class):
        #institution = asys.createActor(institution_class)
        #self.institutions = institution
        pass

    def close_environment(self):
        #asys.shutdown()
        pass

    def create_agents(self, agent_class, number=1):
        # ensure that the actor system and institution are running...
        message = MessageSpace.create_agent(agent_class)
        for i in range(number):
            pass
            #asys.tell(self.institutions, message)

    def list_agents(self):
        message = MessageSpace.list_agents()
        #return asys.ask(self.institutions, message, timedelta(seconds=1.5))

    def get_agents_wealth(self):
        message = MessageSpace.get_wealths()
        print("Message: {}".format(message))
        #return asys.ask(self.institutions, message, timedelta(seconds=1.5))