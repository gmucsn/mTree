class PlayerController:  # was originally the SubjectController()
    def __init__(self, player, data=None, title=None):  # TODO(@messiest) Rethink what's needed for init...
        self.player = player
        self.subject = self.player.subject
        self.user = self.player.user
        self.user_id = self.user.user_id
        self.experiment = self.player.experiment
        try:
            self.session = self.player.institution.environment.period.session  # TODO(@messiest) Do this in a less hacky way
        except:
            pass
        self.recorder = self.experiment.recorder
        self.outlets = {}
        self.action_list = {}
        self.example = None  # What is this for?
        self.response = self.user.response  # Response taken from the User() object

        self.register_outlet("subject_earnings", "subject_earnings")  # this should be moved to be a "user" screen
        self.register_outlet("page_title", "page_title")  # this should be moved to be a "user" screen
        self.register_outlet("page_number", "page_number")  # this should be moved to be a "user" screen
        self.register_outlet("total_pages", "total_pages")  # this should be moved to be a "user" screen
        # self.register_outlet("period_number", "period_number")  # this should be moved to be a "user" screen
        # self.register_outlet("total_periods", "total_periods")  # this should be moved to be a "user" screen

        self.page_title = title
        try:
            self.total_periods = self.session.total_periods
        except:
            self.total_periods = 1

        if data:
            print("Data: {}".format(data))
        # self.recorder("PLAYER CONTROLLER", self.__class__.__name__, self.user_id)
        # self.initializer(data)  # I don't believe this needs to be passed data...
        self.initializer()

    def initializer(self):
        pass

    def screen_setup(self):
        pass

    def __setattr__(self, key, value):
        """
        magic function that passes change to the root object
        :param key:
        :param value:
        :return:
        """
        super().__setattr__(key, value)
        if hasattr(self, 'outlets'):
            if key in self.outlets:
                # print("LETTING: " + str(self.user) + " -- " + str(self.outlets[key]) + " -- " + str(value))

                self.response.let_user(self.user_id, self.outlets[key], value)
                # TODO(@messiest) Figure out if this is needed...
                """if flask.has_app_context():
                    self.response.let_user(self.user, self.outlets[key], value)
                else:
                    with self.experiment.app.app_context():

                        self.response.let_user(self.user, self.outlets[key], value)
                """

    def register_action_handler(self, action_name, handler):
        self.action_list[action_name] = handler

    def register_outlet(self, _property, target):  # _property used due to builtin use of property
        self.outlets[_property] = target

    def action(self, name, data, debug=False):
        """
        Action routing to function
        :param name:
        :param data:
        :return:
        """
        if debug: print("Calling " + str(name) + " with data " + str(data))
        method_call = getattr(self, name)
        method_call(data)

    def remove(self):  # for removing the controller and its associated content
        self.user.detach_controller()  # does this do the clean up?
        pass

    def end(self):
        # self.response.show_user(self.user_id, "end_experiment_screen")
        self.user.close_user()

    def record(self, *args):
        output = ",".join(str(arg) for arg in args)
        self.recorder(self.__class__.__name__, output)

    def exit_experiment(self, data):  #TODO(@messiest) Why does this method not fire with the button press??
        print("Exit Experiment")
