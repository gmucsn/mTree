import numpy
import types
import uuid
import datetime

from mTree.new_objects.user import User
from mTree.new_objects.user_state import UserState
from mTree.new_objects.treatments import Treatment, Treatments


class Experiment:
    treatments = []  # list to store different experiment treatments

    def __init__(self, name, debug=False):
        if debug: print("Initialized")
        self.name = name
        self.experiment_running = False  # TODO: This needs to have various possible states
        self.experiment_state = None
        self.treatment_assignment = None

        self.treatments = {}
        self.users = {}  # TODO(@messiest) change users to subjects IN the environment
        self.user_state = None

        self.experiment_running = False  # TODO: This needs to have various possible states

        self.willow_response = None

        self.users = []
        self.user_state = {}  #
        self.sid_dict = {}  # {sid: user_id}
        self.socketio = None
        self.emitter = None
        self.app = None
        self.db = None
        self.scheduler = None

        self.logger = open("{}.csv".format(self.name), 'a')  # need to come up with stable naming
        self.logger.flush()

    def add_treatments(self, treatments):
        for treatment in treatments:
            self.treatments[treatment.name] = treatment

    def set_assignment_method(self, method="balanced_treatments"):
        methods = [method for method in dir(Experiment) if isinstance(getattr(Experiment, method), types.FunctionType)]
        if method in methods:
            self.treatment_assignment = self.__getattribute__(method)
        else:
            print("Provided object is not a treatment assignment.")

    def balanced_treatments(self):
        if Experiment.treatments:  # treatment list not empty
            treatment = Experiment.treatments.pop()
        else:  # treatment list is empty
            Experiment.treatments = list(self.treatments.keys())
            numpy.random.shuffle(Experiment.treatments)
            treatment = Experiment.treatments.pop()
        return treatment

    def random_treatment(self):
        if not Experiment.treatments:  # populate treatment list
            Experiment.treatments = list(self.treatments.keys())
            treatment = numpy.random.choice(Experiment.treatments)
        else:
            Experiment.treatments = list(self.treatments.keys())
            treatment = numpy.random.choice(Experiment.treatments)
        return treatment

    def create_user(self, sid, debug=False):
        user_id = str(uuid.uuid1())

        if debug: print(user_id)
        # self.user_state[user_id]["running"] = False
        # self.users.append(user_id)
        # self.user_state[user_id] = {}
        self.current = "start_screen"
        self.join_time = datetime.datetime.now()  # adds the user's start time to the data
        self.sid = sid
        # self.response = response.Response().set_user_id(user_id)

    def remove_user(self, sid): # TODO(@messiest) remove print statements after completion

        # print("\nBefore: %s" % str(self.users))

        user = self.sid_dict[sid]

        # print("User being deleted: %s" % user)

        del self.users[self.users.index(user)]

        # print("After: %s\n" % str(self.users))

