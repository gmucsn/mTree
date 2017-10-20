import mTree.base.response as willow
import uuid


class SequentialAgentController():
    def __init__(self, experiment, user=None, data=None):
        self.user = user
        if self.user is None:
            self.generate_agent_id()
        self.experiment = experiment
        self.initializer(data)

    def initializer(self, data):
        pass

    def __setattr__(self, key, value):
        # magic function, passes change to the root object
        super().__setattr__(key, value)

    def generate_agent_id(self):
        agent_id = uuid.uuid4()
        self.user = agent_id
