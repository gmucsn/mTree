class Subject:
    def __init__(self, user, experiment):
        self.user = user  # User() object
        self.user_id = self.user.user_id  # I think this is the right way to do this...
        self.pay = 0.  # total dollar amount the subject has earned in the experiment
        self.experiment = experiment  # the experiment the subject is attached to
        self.recorder = self.experiment.recorder
        self.session = None  # TODO(@messiest) Find a way to associate a subject with a session...
        self.assigned = False  # whether the subject is currently assigned to an institution
        self.subjects = {}
        self.earnings = {}


        self.initializer()  # for child object setup

    def initializer(self):
        pass

    def set_experiment(self, experiment):
        self.experiment = experiment

    def add_pay(self, label, amount):
        self.pay += amount
        self.pay = round(self.pay, 2)
        if label not in self.earnings.keys():
            self.earnings[label] = 0.
        self.earnings[label] += amount
        self.earnings[label] = round(self.earnings[label], 2)
        self.user.add_pay(label, amount)

    def set_session(self, session):
        self.session = session

    def get_pay(self, debug=False):
        if debug: print("Subject {} Pay: {}".format(self.id, self.pay))
        return self.pay

    def record(self, *args):
        output = ",".join(str(arg) for arg in args)
        self.recorder(self.__class__.__name__, output)
