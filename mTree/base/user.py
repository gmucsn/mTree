import datetime
from mTree.base.response import Response


class User:
    def __init__(self, sid, experiment):
        self.user_id = None
        self.running = False
        self.current = "Start Screen"
        self.join_time = datetime.datetime.now()  # adds the user's start time to the data
        self.sid = sid
        self.user_data = {}
        # self.total_earnings = 0.  # which one do we use?
        self.pay = 0.  # the monetary payoff for the User()
        self.earnings = {}  # hash of earnings from all tasks.
        self.controller = None
        self.experiment = experiment

        self.mturk_assignment_id = None
        try:
            self.mturk_assignment_id = self.user_data["assignment_id"]

        except KeyError:
            print("Not an mTurk Subject")

        self.recorder = self.experiment.recorder
        self.response = Response(self.experiment.socketio.emit,
                                 self.experiment.app,
                                 self.experiment.db,
                                 "/subject",
                                 self.experiment.template_location)

        self.initializer()

    def initializer(self):
        pass

    def set_asssignment_id(self, id):
        self.mturk_assignment_id = id
        self.mturk_set_submit()

    def mturk_set_submit(self):
        html_snippet = "<form action='https://workersandbox.mturk.com/mturk/externalSubmit' assignmentId='{}'><button type='input' class='btn btn-primary' id='submit_to_amazon' data-controller-action='submit_to_amazon'>Submit Work to Amazon</button></form>".format(self.mturk_assignment_id)
        self.response.let_user(self.user_id, "mturk_submit", html_snippet)

    def attach_controller(self, controller):
        self.response.hide_user(self.user_id, "welcome_screen")
        self.response.hide_user(self.user_id, "end_experiment_screen")
        self.controller = controller
        self.controller.screen_setup()  # default screen setup

    def detach_controller(self):
        self.controller = None

    def add_pay(self, label, amount):
        self.pay += amount
        self.pay = round(self.pay, 2)
        if label not in self.earnings.keys():
            self.earnings[label] = 0.
        self.earnings[label] += amount
        self.earnings[label] = round(self.earnings[label], 2)

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_pay(self):
        return self.pay

    def get_id(self):
        return self.user_id

    def record(self, *args):
        output = ",".join(str(arg) for arg in args)
        self.recorder(self.__class__.__name__, output)

    def close_user(self):
        self.response.let_user(self.user_id, "total_subject_earnings", "%.2f" % self.pay)
        self.response.show_user(self.user_id, "end_experiment_screen")
        self.response.hide_user(self.user_id, "earnings_breakdown")

        if self.earnings:
            self.response.show_user(self.user_id, "earnings_breakdown")
            html_snippet = "<tr><td><p>{}</p></td><td><p>${:.2f}</p></td></tr>"  # row for table
            html_block = "".join([html_snippet.format(key, self.earnings[key]) for key in self.earnings.keys()])
            self.response.let_user(self.user_id, "task_breakdown", html_block)
        if not self.pay:  # No pay either
            print("HERE")
            self.response.hide_user(self.user_id, "earnings_result")
            self.response.hide_user(self.user_id, "earnings_breakdown")
        if self.mturk_assignment_id:
            self.mturk_set_submit()

    def set_user_data(self, field, value):
        self.user_data[field] = value

    def display_welcome_screen(self):
        self.response.show_user(self.user_id, "welcome_screen")  # welcome screen in subject_base.html
        self.response.hide_user(self.user_id, "end_experiment_screen")  # closing screen in subject_base.html
