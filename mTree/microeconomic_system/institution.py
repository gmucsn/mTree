from thespian.actors import *
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
import uuid



#asys = ActorSystem()


class Institution(Actor):
    def __init__(self):
        self.agents = []
        self.agent_ids = []

    def add_agent(self, agent_class):
        agent_id = str(uuid.uuid1())

#        agent = asys.createActor(agent_class, globalName = agent_id)
        agent = self.createActor(agent_class)  # creates agent as child of institution
        self.agents.append(agent)
        self.agent_ids.append(agent_id)

    def receiveMessage(self, message, sender):
        if isinstance(message, Message):
            if message.recipients == "Institution":
                if message.directive == "create_agent":
                    self.add_agent(message.content)

                elif message.directive == "list_agents":
                    self.send(sender, self.agents)  # explicit call back to sender

            elif message.recipients == "Agents":
                if message.directive == "get_wealth":
                    #wealths = [asys.ask(agent, message) for agent in self.agents]
                    self.send(sender, wealths)  # self.send(address, message)
