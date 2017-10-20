import mTree.base.response as willow


class SequentialAgentController():
    def __init__(self, user, experiment, data=None):
        self.user = user
        self.example = None
        self.action_list = {}
        self.experiment = experiment
        self.initializer(data)

    def initializer(self):
        pass

    def __setattr__(self, key, value):
        # magic function, passes change to the root object
        super().__setattr__(key, value)
