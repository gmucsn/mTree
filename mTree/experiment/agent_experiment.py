import os
import sys
import datetime
import logging
from logging import FileHandler
import yaml
from uuid import *
import mTree.base.response as response
from mTree.base.user import User
from mTree.base.recorder import Recorder


class AgentExperiment:
    def __init__(self, debug=False):
        self.debug = debug
        if self.debug: print("Initialized")
        self.willow_response = None
        self.experiment_running = False  # TODO: This needs to have various possible states
        self.experiment_state = None

        self.sessions = {}  # TODO(@messiest) Think of how this can be used with multiple sessions
        self.session = None

        self.subjects = {}  # subjects is now the experiment level object for users...

        # Below needs to be moved to the mTree level...
        self.users = []
        self.user_state = {}  #
        self.user_objects = {}
        self.inactive_users = {}
        self.sid_dict = {}  # {sid: user_id}
        self.socketio = None
        self.emitter = None
        self.app = None
        self.db = None
        self.scheduler = None
        self.static_file_location = None
        self.static_content_location = None

        # for mechanical turk purposes
        self.task_preview = None


        path = os.path.realpath(sys.modules[self.__module__].__file__)
        self.template_location = os.path.join(os.path.dirname(path), 'html/')

        self.recorder = Recorder

        # self.recorder("STARTING EXPERIMENT", self.__class__.__name__)
        self.initializer()

    def initializer(self):
        pass

    def attach_emitter(self, emitter):
        self.emitter = emitter

    def attach_socketio(self, socketio):
        self.socketio = socketio

    def attach_app(self, app):
        self.app = app

    def attach_db(self, db):
        self.db = db

    def attach_scheduler(self, scheduler):
        self.scheduler = scheduler

    def response(self, debug=False):
        if debug: print("Attempting Reponse")
        return response.Response(self.emitter,
                                 self.app,
                                 self.db,
                                 "/subject",
                                 self.template_location)

    def set_static_file_location(self, location):
        self.static_file_location = location

    def provide_static_file(self, filename):
        return

    def set_static_content_location(self, location):
        self.static_content_location = location

    def get_static_content_location(self):
        return self.static_content_location

    def set_task_preview(self, preview_file):
        self.task_preview = preview_file

    def get_task_preview(self):
        return self.task_preview

    def load_config(self,filename):
        temp_store = yaml.load(open(filename))
        self.update(temp_store)

    def create_user(self, sid): # initiates new users
        # first must create a uuid for the user
        """Method to create a new user

        :param sid:
        :param WillowResponse:
        :return:
        """
        user_id = str(uuid1())

        self.users.append(user_id)
        self.user_state[user_id] = {}
        self.user_state[user_id]["running"] = False
        self.user_state[user_id]["current"] = "Start Screen"
        self.user_state[user_id]["join_time"] = datetime.datetime.now()  # adds the user's start time to the data
        self.user_state[user_id]["sid"] = sid
        self.user_state[user_id]["total_earnings"] = None

        # creating a new user object to handle users throughout the system...
        new_user = User(sid, self)
        new_user.set_user_id(user_id)



        #####
        self.response().set_user_id(user_id)
        # new_user.response().set_user_id(user_id)
        msg_data = {}
        msg_data["action"] = "add_user"
        msg_data["data"] = {}
        msg_data["data"]["user_id"] = user_id
        msg_data["data"]["current"] = str(self.user_state[user_id]["current"])
        msg_data["data"]["join_time"] = str(self.user_state[user_id]["join_time"])
        msg_data["data"]["earnings"] = str(0)

        self.user_objects[user_id] = new_user
        self.sid_dict[sid] = user_id

        # TODO What other things do we need for the user_state variables?
        #self.response.update_admin_status(msg_data)
        return user_id

    def add_user_property(self, user_id, property, value):
        self.user_state[user_id][property] = value
        self.user_objects[user_id].set_user_data(property, value)

    def check_experiment_state_to_run(self, user_id):
        if self.experiment_state == "running":
            self.start_user(user_id)

    def start_user(self, user_id):
        pass

    def remove_user(self, sid):
        user = self.sid_dict[sid]
        del self.users[self.users.index(user)]

    def event_handler(self, event):
        if self.debug: print("\n" + str(event) + "\n")
        if event["controllerAction"] != "":
            self.user_objects[event['user_id']].controller.action(event["controllerAction"], event)

    def get_template_location(self):
        return self.template_location

    def record(self, *args):
        output = ",".join(str(arg) for arg in args)
        self.recorder(self.__class__.__name__, output)
