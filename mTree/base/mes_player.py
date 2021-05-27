class MesPlayer:
    def __init__(self, subject, institution, player_type=None):
        self.controller = None                     # controller used in the institution
        self.subject = subject                     # subject object for the user
        self.experiment = self.subject.experiment  #
        self.recorder = self.experiment.recorder   #
        self.user = self.subject.user              # idk if this will work...
        self.id = self.user.user_id                # idk if this will work...
        self.institution = institution             # the institution the player is associated with
        self.points = 0.                           # points earned in the institution.
        self.player_type = player_type             # player type for the associated institution

        self.initializer()

    def initializer(self):
        pass

    def set_controller(self, controller):
        self.controller = controller
        self.user.attach_controller(self.controller)

    def set_player_type(self, player_type):
        self.player_type = player_type

    def set_institution(self, institution):
        self.institution = institution
        self.assigned = True

    def screen_setup(self):
        self.controller.screen_setup()

    def add_pay(self, label, amount):  # adds pay to the subject object
        self.subject.add_pay(label, amount)

    def close(self):  # closing the player object
        self.controller.response.delete_content(self.id, self.institution.name)
        self.user.detach_controller()  # does this handle clean up?
        self.subject.assigned = False
        pass

    def record(self, *args):
        output = ",".join(str(arg) for arg in args)
        self.recorder(self.__class__.__name__, output)
