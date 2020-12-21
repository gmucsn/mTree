class Session:  # TODO(@messiest) There needs to be a way to set the number of players here...
    def __init__(self, experiment, name=None):
        self.experiment = experiment  # experiment the session is being run from
        self.recorder = self.experiment.recorder
        self.name = name
        self.periods = []
        self.subjects = {}
        self.exchange_rate = 1.0
        self.total_periods = 0
        self.current_period = 0

        # self.recorder("SESSION", self.__class__.__name__)
        self.initializer()

    def initializer(self):
        pass

    def set_name(self, name):
        self.name = name

    def add_subjects(self, *subjects, debug=False):
        for subject in subjects:
            self.subjects[subject.user_id] = subject
            subject.set_session(self)
        if debug:
            print("SESSION: {}, SUBJECTS: {}".format(self, self.subjects))

    def close(self):
        for subject in self.subjects.values():
            subject.user.close_user()

    def set_periods(self, *periods):
        for period in periods:
            if type(period) is tuple:
                for i in range(period[1]):
                    self.periods.append(period[0](self))
            else:
                self.periods.append(period(self))
        self.total_periods = len([type(x) for x in self.periods])
        # self.total_periods = len(set([type(x) for x in self.periods]))

    def run_period(self):
        print("running the period...")
        print(self.periods)
        if self.periods:  # periods still remain
            period = self.periods.pop(0)  # retrieve first period
            self.current_period = self.total_periods - len(self.periods)  # gives the difference between total and current
            print("about to start")
            period.start()
        elif not self.periods:
            self.end_session()
        print("period returned...")

    def run(self):
        pass

    def end_session(self, debug=False):
        if debug: print("SESSION ENDED")
        for subject in self.subjects.values():
            subject.user.close_user()
        pass

    def record(self, *args):
        output = ",".join(str(arg) for arg in args)
        self.recorder(self.__class__.__name__, output)
