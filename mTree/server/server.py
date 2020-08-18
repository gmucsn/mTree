import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, render_template_string, session, request, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect,  Namespace
import flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler import events
from flask_apscheduler import APScheduler
from flask_basicauth import BasicAuth


from mTree.components.admin_message import AdminMessage


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
from os import listdir
from os.path import isfile, join

from mTree.components import registry

from mTree.base.response import Response

from mTree.server.admin import admin_area

from mTree.server.subject import subject_area

from mTree.server.subject_pool import SubjectPool

from mTree.runner.server_runner import ServerRunner
from mTree.server.component_registrar import ComponentRegistrar
import signal
from blessed import Terminal
from mTree.server.admin_namespace import AdminNamespace
from mTree.server.subject_namespace import SubjectNamespace
from mTree.server.configuration_scanner import ConfigurationScanner


class MTreeController(object):
    app = None

    def __init__(self):
        print("doing stuff")
        #  print("initializing " * 20)


        self.async_mode = 'eventlet'  # None
        self.app = Server()
        #self.app.config['SECRET_KEY'] = 'secret!'

        #self.app.config['EXPLAIN_TEMPLATE_LOADING'] = True

        thread = None
        #self.socketio = SocketIO(self.app) #, async_mode=self.async_mode)
        self.component_registry = registry.Registry()
        self.component_registry.register_server(self)


        # template_loader = jinja2.ChoiceLoader([self.app.jinja_loader,
        #                                        jinja2.PackageLoader('mTree', 'base/admin_templates'),
        #                                        jinja2.PackageLoader('mTree', 'base/user_templates')])
        # self.app.jinja_loader = template_loader

        # self.app.config['BASIC_AUTH_USERNAME'] = '<PLACE USERNAME HERE>'
        # self.app.config['BASIC_AUTH_PASSWORD'] = '<PLACE PASSWORD HERE>'

        # self.basic_auth = BasicAuth(self.app)

        # self.add_routes()
        # self.scheduler = APScheduler()
        # self.scheduler.init_app(self.app)
        # self.scheduler.start()
        # self.scheduler.add_listener(self.my_listener, events.EVENT_ALL)
        #self.app.register_blueprint(admin_area, url_prefix='/admin')
        # self.app.register_blueprint(admin_area)
        # self.add_routes()

    def add_routes(self):
        @self.socketio.on('admin_control', namespace='/admin')
        def admin_control_message(message):
            print("Received Admin Message")
            return self.component_registry.message(message)
            # self.experiment.admin_event_handler(message)


    def run(self):
        print("SSSstarting server...")
        #self.list_rules()
        self.socketio.run(self.app, host='0.0.0.0', debug=True)

class NewServer(Flask):
    def __init__(self):
        Flask.__init__(self, __name__)
        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            jinja2.PrefixLoader({}, delimiter = ".")
        ])
        print("test start")
        #print(self.app)

    def create_global_jinja_loader(self):
        return self.jinja_loader

    def register_blueprint(self, bp):
        Flask.register_blueprint(self, bp)
        #self.jinja_loader.loaders[1].mapping[bp.name] = bp.jinja_loader

    def list_rules(self):
        print("rule list")
        print(self.url_map)





class Server(object):
    app = None

    def __init__(self):
        #  print("initializing " * 20)
        self.configuration_scanner = ConfigurationScanner()
        self.configuration_scanner.scan_configurations()

        self.async_mode = 'eventlet' # None
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        thread = None
        self.socketio = SocketIO(self.app, async_mode=self.async_mode, cors_allowed_origins="*")
        SubjectPool().register_flask_outlet(self.socketio)
        self.socketio.on_namespace(AdminNamespace('/admin'))
        self.socketio.on_namespace(SubjectNamespace('/subject'))        
        
        template_loader = jinja2.ChoiceLoader([self.app.jinja_loader,
                                               jinja2.PackageLoader('mTree', 'base/admin_templates'),
                                               jinja2.PackageLoader('mTree', 'base/user_templates')])
        self.app.jinja_loader = template_loader

        #self.app.config['BASIC_AUTH_USERNAME'] = '<PLACE USERNAME HERE>'
        #self.app.config['BASIC_AUTH_PASSWORD'] = '<PLACE PASSWORD HERE>'

        #self.basic_auth = BasicAuth(self.app)

        #self.server_runner = ServerRunner()
        self.component_registrar = ComponentRegistrar()

        self.term = Terminal()


        self.add_routes()
        #self.scheduler = APScheduler()
        #self.scheduler.init_app(self.app)
        #self.scheduler.start()
        #self.scheduler.add_listener(self.my_listener, events.EVENT_ALL)
        self.app.register_blueprint(admin_area, url_prefix='/admin')
        self.app.register_blueprint(subject_area, url_prefix='/subject')


    def list_rules(self):
        pass


    def on_resize(self, sig, action):
        print(f'height={self.term.height}, width={self.term.width}')

    def register_blueprint(self, bp):
        Flask.register_blueprint(self, bp)

    def my_listener(self, event):
        print("APSCHEDULER EVENT " + str(event))

    def run_server(self):
        self.list_rules()
        self.socketio.run(self.app, host='0.0.0.0')

    def log_message(self):
        print(f'height={self.term.height}, width={self.term.width}')

    def attach_experiment(self, experiment):
        self.experiment = experiment()
        self.experiment.attach_emitter(emit)
        self.experiment.attach_socketio(self.socketio)

        self.experiment.attach_app(self.app)
        self.experiment.attach_db(None)
        self.experiment.attach_scheduler(self.scheduler)

    def get_response(self, emit):
        return Response(emit, self.app, self.db)

    def add_routes(self):
        pass




    def add_scheduler(self, sched_function):
        self.scheduler.add_job(func=sched_function, trigger=IntervalTrigger(seconds=5),
                               id="print_test", name="print something", replace_existing=True)

