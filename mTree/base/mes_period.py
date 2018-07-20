from mTree.base.period import Period

class MesPeriod(Period):
    def __init__(self, session):  # environment/institutions set up in file
        self.session = session    # session the period is a part of
        self.recorder = self.session.recorder
        #self.environment = None   # environment attached to the period
        #self.institutions = []    # list of institutions for the period
        self.subjects = self.session.subjects
        # self.recorder("PERIOD", self.__class__.__name__)
        self.initializer()

    def initializer(self):
            print("initializing...")

    def set_environment(self, environment):
        self.environment = environment

    def start_period(self):
        print("starting to run the MES Period")
        #self.run_institutions()
        #institution = self.institutions.pop()
        #institution.start_institution()

    def end_period(self, debug=False):
        if debug: print("ENDING PERIOD")
        self.session.run_period()  # run the next period
        pass

    def run_institutions(self):
        if self.institutions:
            institution = self.institutions.pop(0)
            institution.start_institution()
        else:
            self.end_period()

    def start(self):
        """
        Needs to be overwritten in the experiment to run the period.
        :return:
        """
        print("WARNING: Run method was not defined.")
        pass

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

    def record(self, *args):
        output = ",".join(str(arg) for arg in args)
        self.recorder(self.__class__.__name__, output)
