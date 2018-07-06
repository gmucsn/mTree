import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, render_template_string, session, request, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
import flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler import events
from flask_apscheduler import APScheduler
from flask_basicauth import BasicAuth


import logging
from logging.handlers import RotatingFileHandler
from inspect import getframeinfo, stack
import mTree.base.response as willow

import json
import jinja2
from jinja2 import Environment, FileSystemLoader

from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, FileSystemLoader
import os

from mTree.base.response import Response


class Server(object):
    app = None

    def __init__(self):
        #  print("initializing " * 20)
        self.async_mode = 'eventlet' # None
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        thread = None
        self.socketio = SocketIO(self.app, async_mode=self.async_mode)
        template_loader = jinja2.ChoiceLoader([self.app.jinja_loader,
                                               jinja2.PackageLoader('mTree', 'base/admin_templates'),
                                               jinja2.PackageLoader('mTree', 'base/user_templates')])
        self.app.jinja_loader = template_loader

        self.app.config['BASIC_AUTH_USERNAME'] = 'testing'
        self.app.config['BASIC_AUTH_PASSWORD'] = 'testing'

        self.basic_auth = BasicAuth(self.app)

        self.add_routes()
        self.scheduler = APScheduler()
        self.scheduler.init_app(self.app)
        self.scheduler.start()
        #self.scheduler.add_listener(self.my_listener, events.EVENT_ALL)



    def my_listener(self, event):
        print("APSCHEDULER EVENT " + str(event))

    def run_server(self):
        print("RUNNING " * 20)
        self.socketio.run(self.app, host='0.0.0.0', debug=True)

    def attach_experiment(self, experiment):
        self.experiment = experiment()
        self.experiment.attach_emitter(emit)
        self.experiment.attach_socketio(self.socketio)

        self.experiment.attach_app(self.app)
        self.experiment.attach_db(None)
        self.experiment.attach_scheduler(self.scheduler)

    def get_response(self, emit):
        return Response(emit, self.app, self.db)

    def add_scheduler(self, sched_function):
        self.scheduler.add_job(func=sched_function, trigger=IntervalTrigger(seconds=5),
                               id="print_test", name="print something", replace_existing=True)

    def add_routes(self):
        @self.app.route('/admin_dashboard')  # URL path for the admin screen
        @self.basic_auth.required
        def index():
            return render_template('admin_base.html')

        @self.app.route('/static_content/<string:path>')
        def static_hosting(path):
            static_content_location = self.experiment.get_static_content_location()
            return send_from_directory(static_content_location, path)

        @self.app.route('/subject')  # URL path for the subject screen
        def not_search():
            assignment_id = request.args.get('assignmentId')
            hit_id = request.args.get('hitId')
            turk_submit_to = request.args.get('turkSubmitTo')
            worker_id = request.args.get('workerId')

            if assignment_id == "ASSIGNMENT_ID_NOT_AVAILABLE":
                # display the preview screen... presumably
                context = {}
                template = Environment(loader=FileSystemLoader(self.experiment.get_template_location() or './')).get_template(
                    self.experiment.get_task_preview()).render(context)
                print("PREPARING FOR A PREVIEW...")
                return template
            else:
                return render_template('subject_base.html', async_mode=self.socketio.async_mode)

        @self.app.route('/<string:experiment_id>/<request_page>')  # TODO(@skunath) This is where it's failing. What's happening?
        def pageHandler(template):
            return render_template(template)

        @self.socketio.on('admin_control', namespace='/admin')
        def admin_control_message(message):
            #self.experiment.admin_event_handler(message)
            self.experiment.start_experiment()

        @self.socketio.on('user_configuration', namespace='/subject')
        def receive_user_configuration(message):
            # need to send user id information
            event = json.loads(message["data"])
            print(event)
            user_id = event["user_id"]
            assignment_id = event["assignmentId"]
            hit_id = event["hitId"]
            worker_id = event["workerId"]
            self.experiment.add_user_property(user_id, "assignment_id", assignment_id)
            self.experiment.add_user_property(user_id, "hit_id", hit_id)
            #self.experiment.add_user_property(user_id, "turk_submit_to", turk_submit_to)
            self.experiment.add_user_property(user_id, "worker_id", worker_id)
            # print("PUT OCCUR -- " + str(event))


        @self.socketio.on('put', namespace='/subject')
        def receive_put(message):
            # need to send user id information
            event = json.loads(message["data"])
            #print("PUT OCCUR -- " + str(event))
            self.experiment.event_handler(event)

        @self.socketio.on('join', namespace='/subject')
        def subjectJoin(message):
            print("\n\nSUBJECT JUST JOINED\n\n")

            join_room(message['room'])

        @self.socketio.on('connect', namespace='/subject')
        def subject_connect():
            # need to send user id information
            assignment_id = request.args.get('assignmentId')
            hit_id = request.args.get('hitId')
            turk_submit_to = request.args.get('turkSubmitTo')
            worker_id = request.args.get('workerId')

            user_id = self.experiment.create_user(request.sid)


            join_room(user_id)
            print("\nCONNECTED\nUser: {}\n\n".format(user_id))

            self.experiment.user_objects[user_id].display_welcome_screen()  # display the welcome screen to the connected user

            self.experiment.check_experiment_state_to_run(user_id)  # Auto start when subjects connect

        @self.socketio.on('disconnect', namespace='/subject')
        def subject_disconnect():
            print("CLIENT DISCONNECTED")
            self.experiment.remove_user(request.sid)  # TODO(@messiest) Think of a better way to remove users

if __name__ == '__main__':
    global c_experiment
    c_experiment = experiment.Experiment()
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler("foo.log")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
