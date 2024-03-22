import eventlet
# eventlet.monkey_patch()

# from gevent.pywsgi import WSGIServer

from flask import Flask, render_template, render_template_string, session, request, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
import flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler import events
from flask_apscheduler import APScheduler
from flask_basicauth import BasicAuth
import pkgutil
import importlib
import uuid
import sys
import hashlib


import logging
from logging.handlers import RotatingFileHandler
from logging import Handler
from inspect import getframeinfo, stack
import jinja2
from jinja2 import Environment, FileSystemLoader

# from flask_sqlalchemy import SQLAlchemy
import os

from mTree.server.actor_system_connector import ActorSystemConnector
from mTree.development.development_endpoints import development_area
from mTree.subject_interface.subject_endpoints import subject_area
from mTree.development.mtree_configuration import MTreeConfiguration
from mTree.development.subject_directory import SubjectDirectory
from mTree.components import registry
from mTree.base.response import Response
from mTree.microeconomic_system.admin_message import AdminMessage
from mTree.components.registry import Registry
from mTree.simulation.mes_simulation_library import MESSimulationLibrary

# from mTree.microeconomic_system.subject_container import SubjectContainer
# from mTree.components.admin_message import AdminMessage



class RequestsHandler(Handler):
    def __init__(self, emitter):
        logging.Handler.__init__(self)
        self.emitter = emitter

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.emitter('willow_action',{
                'data': {"message": log_entry, "item": "LOGG"}},
                namespace="/developer")

        except:
            pass
        #logging.info("inside handler")
        #return requests.post('http://example.com:8080/',
                             #log_entry, headers={"Content-type": "applicatio

class MyFilter(logging.Filter):
    def filter(self, record):
        record.msg = 'MY FILTER: ' + record.msg
        return 1


class DevelopmentServer(object):
    app = None

    def __init__(self):
        # self.async_mode = 'eventlet' # None
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        thread = None

        # Configure logging for the Socket IO mechanisms
        self.socketio = SocketIO(self.app, 
                # async_mode=self.async_mode, 
                logger=False, 
                engineio_logger=False)
        ###
        # TODO think about the log setup above
        ###
        template_loader = jinja2.ChoiceLoader([self.app.jinja_loader,
                                               jinja2.PackageLoader('mTree', 'development/development_templates'),
                                               ])
        self.app.jinja_loader = template_loader

        #self.app.config['BASIC_AUTH_USERNAME'] = '<PLACE USERNAME HERE>'
        #self.app.config['BASIC_AUTH_PASSWORD'] = '<PLACE PASSWORD HERE>'

        self.basic_auth = BasicAuth(self.app)

        self.mTree_configuration = MTreeConfiguration()
        self.subject_directory = SubjectDirectory()


        self.add_routes()
        # self.scheduler = APScheduler()
        # self.scheduler.init_app(self.app)
        # self.scheduler.start()
        #self.scheduler.add_listener(self.my_listener, events.EVENT_ALL)
        self.app.register_blueprint(development_area, url_prefix='/')

        self.app.register_blueprint(subject_area, url_prefix='/subjects')

        self.subject_container = None #SubjectContainer()

        #self.actor_system = ActorSystemConnector()

        # attempts at logger adding...
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = RequestsHandler(emit)
        handler.setLevel(logging.INFO)
        myfilter = MyFilter()
        handler.addFilter(myfilter)
        #formatter = LogstashFormatter(self.logger_name.upper())
        #handler.setFormatter(formatter)
        #self.logger.addHandler(handler)


    def list_rules(self):
        print(self.app.url_map)


    def examine_directory(self):
        import importlib
        from importlib import import_module
        module = importlib.import_module("mTree.components")

        import glob
        import sys
        from types import ModuleType

        base_module = ModuleType('mTree.components')

        #base_module = ModuleType('cva_mes')
        #sys.modules['cva_mes'] = ModuleType('cva_mes')
        #sys.modules['cva_mes.cva_environment'] = ModuleType('cva_mes.cva_environment')
        #"cva_mes."
        #globals()[module_name] = foo

        modules_imported = []
        module_names = []
        for filename in glob.iglob('./mes/*.py', recursive=True):
            import_name = os.path.splitext(os.path.basename(filename))[0]

            module_name = "mes." + import_name.partition('.')[0]

            import importlib.util


            #try:
            #    return sys.modules[fullname]
            #except KeyError:
            try:
                spec = importlib.util.spec_from_file_location(module_name, filename)
                #spec = importlib.util.find_spec(fullname)
                #sys.modules[module_name] = ModuleType(module_name)
                module = importlib.util.module_from_spec(spec)
                loader = importlib.util.LazyLoader(spec.loader)
                # Make module with proper locking and get it inserted into sys.modules.
                a = loader.exec_module(module)
                sys.modules[module_name] = module
                #return module
            
                print(sys.modules[module_name])
            except Exception as e:
                pass
            #foo = importlib.util.module_from_spec(spec)
            #loader = importlib.util.LazyLoader(spec.loader)

            #globals()[module_name] = module
            #print(module)
            #modules_imported.append((module, spec))
            #module_names.append(module)
            #print(foo)
            #base_module


            #spec.loader.exec_module(foo)
            #sys.modules[module_name] = module
            # print(foo)
            #foo.MyClass()
            # module_path = module
            #
            # module_name = os.path.basename(filename)
            # new_module = __import__(module_name, fromlist=[filename])
            # print(new_module)
            # globals()[module_name] = new_module
        #all_my_base_classes = {cls.__name__: cls for cls in base._MyBase.__subclasses__()}

        sys.modules['mes'] = ModuleType('mes')

        import inspect
        target_class = None
        for name, obj in inspect.getmembers(sys.modules["mTree.server"]):
            if inspect.isclass(obj):
                if obj.__name__ == "CVAEnvironment":
                    target_class = obj

        # print("SHOULD HAVE LOADED THEM>>>>")
        # print(module_names)
        # print("ABOVE")
        # test = modules_imported[0]
        # for i in modules_imported:
        #     print("\t\tAbout to load: ", i[0])
        #     try:
        #         i[1].loader.exec_module(i[0])
        #     except Exception as e:
        #         print("ISSUE LOADING")
        #         print(e)
        #         print("<<<<<<<<")
        # print(test)
        #spec.loader.exec_module(test)

    def load_mtree_module(self, module_name):

        try:
            return sys.modules[module_name]
        except KeyError:
            spec = importlib.util.find_spec(module_name)
            module = importlib.util.module_from_spec(spec)
            loader = importlib.util.LazyLoader(spec.loader)
            # Make module with proper locking and get it inserted into sys.modules.
            loader.exec_module(module)
            return module


    def my_listener(self, event):
        print("APSCHEDULER EVENT " + str(event))

    def add_routes(self):

        @self.socketio.on('connect', namespace='/developer')
        def test_connect(auth):
            emit('subject_message', {'response': 'connected'})

        @self.socketio.on('json', namespace='/developer')
        def admin_json(json):
            print("Received a json message to admin...")
            command = json["command"]
            payload = json["payload"]

            if command == "register_admin":
                join_room("admin")
            if command == "start_subject_experiment":
                subject_directory = SubjectDirectory()
                if not subject_directory.experiment_status():   
                    emit('experiment_status_message', {'response': 'status', 'payload': {'status': 'Started'}})
                    subject_directory.start_experiment()
                    configuration = payload["configuration"]
                    # run_code_gen = str(uuid.uuid4())
                    # run_code = run_code_gen[0:6]
                    


                    component_registry = Registry()
                    working_dir = os.path.join(os.getcwd())
                    simulation_library = MESSimulationLibrary()
                    simulation_library.list_human_subject_files_directory(working_dir)
                    simulation = simulation_library.get_simulation_by_filename(configuration)
                    actor_system = ActorSystemConnector()
                    working_dir = os.path.join(os.getcwd())
                    actor_system.run_human_subject_experiment(working_dir, configuration, simulation["description"].to_hash(), subject_directory.get_subjects())




        @self.socketio.on('disconnect')
        def test_disconnect():
            print('Client disconnected!!!!')

        @self.socketio.on('run_test_configuration', namespace='/developer')
        def run_test_configuration(message):
            actor_system = ActorSystemConnector()
            actor_system.send_message()
            #return self.component_registry.message(message)


        @self.socketio.on('message', namespace='/developer')
        def message_handler(message):
            self.socketio.send(message, namespace='/developer', broadcast=True)


        # @self.socketio.on('admin_mes_message', namespace='/developer')
        # def admin_mes_message(message):
        #     self.actor_system.send_message()
        #     self.socketio.send(message, namespace='/developer', broadcast=True)

        @self.socketio.on('admin_mes_message', namespace='/developer')
        def admin_mes_message(message):

            admin_message = AdminMessage(request=message["request"])
            if "payload" in message.keys():
                admin_message.set_payload(message["payload"])
                
            actor_system = ActorSystemConnector()
            actor_system.send_message(admin_message)

        @self.socketio.on('admin_mes_response', namespace='/developer')
        def admin_mes_response(message):
            print("WebServer handling an MES admin response")
            self.socketio.emit('mes_response', message, namespace='/developer', broadcast=True)



        @self.socketio.on('system_status', namespace='/developer')
        def system_status(message):
            print("Retrieved system status")
            print(message)
            self.socketio.send(message, namespace='/developer', broadcast=True)

            #return self.component_registry.message(message)


        @self.socketio.on('get_system_status', namespace='/developer')
        def get_system_status(message):
            print("Shoud start to run a sim")
            print(message)
            actor_system = ActorSystemConnector()
            actor_system.send_message(message)
            self.socketio.emit({'data': 'echo back'}, namespace='/developer', broadcast=True)

            # self.socketio.emit('message', {'data': 'foo'}, namespace='/admin', broadcast=True)

            #return self.component_registry.message(message)

        @self.socketio.on('log_message_display', namespace='/log_messages')
        def actor_messages(message):
            print("Shoud start to run a sim")
            print(message)
            self.socketio.emit('log_message', {'data': 'foo'}, namespace='/developer', broadcast=True)

            #self.actor_system.send_message()
            #return self.component_registry.message(message)


        @self.app.route('/mes_response_channel', methods=['POST'])
        def mes_response_channel():
            print("MES Response channel activated...")
            data = request.get_json()
            self.socketio.emit('mes_response', data, namespace='/developer', broadcast=True)
            response = {"status": "success"}
            return response, 200

        @self.app.route('/mes_subject_channel', methods=['POST'])
        def mes_subject_channel():
            data = request.get_json()
            command = data["command"]
            if command == "display_ui":
                # get ui...
                ui_file = os.path.join(os.getcwd(), "ui", data["payload"]["ui_file"])
                ui_content = None
                with open(ui_file, "r") as t_file:
                    ui_content = t_file.read()
                emit('display_ui', {'ui_content': ui_content}, namespace='/subject', to=data["subject_id"])
            elif command == "outlet":
                emit('update_data', data["payload"], namespace='/subject', to=data["subject_id"])
            elif command == "update_data":
                emit('update_data', data["payload"], namespace='/subject', to=data["subject_id"])
            elif command == "update_value":
                emit('subject_message', {'response': 'Another Subject Connected '}, namespace='/subject', to=data["subject_id"])
            elif command == "execute_method":
                emit('execute_method', data["payload"], namespace='/subject', to=data["subject_id"])
                        


            response = {"status": "success"}
            return response, 200



        @self.socketio.on('connect', namespace='/subject')
        def subject_connect(message):
            emit('subject_message', {'response': 'Subject Connected'})

        

        @self.socketio.on('disconnect', namespace='/subject')
        def subject_disconnect():
            subject_directory = SubjectDirectory()
            subject_directory.disconnect_subject(request.sid)
            emit('subject_message', {'response': 'subject_connection', 'payload': {"subjects": subject_directory.get_subjects()}}, namespace='/developer', to="admin")



        @self.socketio.on('json', namespace='/subject')
        def subject_json(json):
            
            command = json["command"]
            payload = json["payload"]

            if command == "register_subject_id":
                subject_directory = SubjectDirectory()
                subject_directory.update_subjects(payload["subject_id"], request.sid)
                join_room(payload["subject_id"])
                join_room("all_subjects")
                emit('subject_message', {'response': 'Another Subject Connected '}, to="all_subjects")
                emit('subject_message', {'response': 'subject_connection', 'payload': {"subjects": subject_directory.get_subjects()}}, namespace='/developer', to="admin")
            elif command == "agent_action":
                actor_system = ActorSystemConnector()
                actor_system.send_agent_action(json)
                

        # @self.app.route('/component_view')
        # def component_view():
        #     component_type = request.args.get('component_type')
        #     component_name = request.args.get('component_name')
        #     component_details = registry.get_mes_component_details(component_name)
        #     return render_template('component_view.html', component_details=component_details, component_name=component_name, component_type=component_type)

        # @self.socketio.on('developer_control', namespace='/developer')
        # def admin_control_message(message):
        #     return self.component_registry.message(message)
        #     # self.experiment.admin_event_handler(message)

        # @self.socketio.on('run_simulation', namespace='/developer')
        # def run_simulation_message(message):

        #     #emit("admin_action",{"TEST":"TEST"}, namespace="/developer")
        #     #module = globals()[]
        #     module = sys.modules["cva_mes.cva_environment"]
        #     import inspect
        #     target_class = None
        #     for name, obj in inspect.getmembers(module):
        #         if inspect.isclass(obj):
        #             if obj.__name__ == "CVAEnvironment":
        #                 target_class = obj
        #     self.subject_container = SubjectContainer()
        #     self.subject_container.create_environment(target_class, 1)
        #     #return self.component_registry.message(message)
        print("ADDED")
        # @self.app.route('/subject')  # URL path for the subject screen
        # def not_search():
        #     assignment_id = request.args.get('assignmentId')
        #     hit_id = request.args.get('hitId')
        #     turk_submit_to = request.args.get('turkSubmitTo')
        #     worker_id = request.args.get('workerId')

        #     if assignment_id == "ASSIGNMENT_ID_NOT_AVAILABLE":
        #         # display the preview screen... presumably
        #         context = {}
        #         template = Environment(loader=FileSystemLoader(self.experiment.get_template_location() or './')).get_template(
        #             self.experiment.get_task_preview()).render(context)
        #         print("PREPARING FOR A PREVIEW...")
        #         return template
        #     else:
        #         return render_template('subject_base.html', async_mode=self.socketio.async_mode)


    def run_server(self):
        self.examine_directory()
        self.list_rules()
        # Flask Service Launch
        # TODO think about log output here
        self.socketio.run(self.app, 
            host='0.0.0.0', 
            log_output=False, # another log statement to cocnsider... 
            use_reloader=False)

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

