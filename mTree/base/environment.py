class Environment:
    def __init__(self, period):
        self.period = period
        self.recorder = self.period.recorder
        self.experiment = self.period.session.experiment  # the experiment in which the environment is initiated
        self.subjects = self.period.subjects

        #  self.recorder("ENVIRONMENT", self.__class__.__name__)
        self.institutions = []

        # TODO(@messiest) Fix below to reflect design changes
        users = self.experiment.user_objects  # dictionary of user objects
        self.users = users                    # list of user ids

        ################################################################
        # Match-making variables
        self.match_making = self.get_subjects()  # list of user ids waiting to be matched
        self.pairings = {}  # dictionary of paired user objects
        self.pairing_ids = {}  # dictionary of paired user ids
        # self.subject_pairing()  # match all the subjects
        ################################################################

        self.running_institutions = []

        self.initializer()

    def initializer(self):
        pass

    def set_institutions(self, *institutions):  # add institutions to the period
        for institution in institutions:
            if type(institution) is tuple:
                for i in range(institution[1]):
                    self.institutions.append(institution[0])
            else:
                self.institutions.append(institution)

    def run_institution(self):
        pass


    def get_subjects(self):
        """
        Returns a list of all subject objects
        :return:
        """
        return list(self.subjects.values())

    def get_subject(self):
        """
        Returns one subject object not currently assigned to an institution
        :return:
        """
        for subject in self.subjects.keys():
            if self.subjects[subject].assigned:
                continue
            else:
                self.subjects[subject].assigned = True
                return self.subjects[subject]

    def subject_pairing(self):
        pass

    def run(self):
        if not self.institutions:
            self.period.end_period()
            return
        else:
            self.run_institution()

    def record(self, *args):
        output = ",".join(str(arg) for arg in args)
        self.recorder(self.__class__.__name__, output)
