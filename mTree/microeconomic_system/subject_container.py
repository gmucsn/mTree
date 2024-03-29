from thespian.actors import *
#import logging
#from mTree.microeconomic_system.logging import logcfg
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
import sys
from datetime import timedelta
import logging
import atexit

class SubjectContainer():

    __instance = None

    class __SubjectContainer:
        def __init__(self, logcfg=None):
            atexit.register(self.container_cleanup)

            self.actor_system = None
            self.logcfg = logcfg
            self.create_actor_system()

            self.root_environment = None
            self.environments = {}

        def container_cleanup(self):
            print("CONTAINER SHUTTING DOWN")


        def create_actor_system(self):
            if self.logcfg != None:
                self.actor_system = ActorSystem("multiprocQueueBase", logDefs=self.logcfg)
            else:
                self.actor_system = ActorSystem("multiprocQueueBase") #, logDefs=logcfg)

        def create_environment(self, environment_class, environment_name):
            print("CREATING AN ENVIRONMENT")
            print(environment_class.__module__)
            print(environment_class.__name__)
            print("!@!@!@!@!@")
            t = environment_class()
            #print(t)
            print(sorted(sys.modules))
            import inspect
            print(inspect.getmodule(environment_class))
            for name, obj in inspect.getmembers(sys.modules["cva_mes.cva_environment"]):
                print("lkjlkjlk")
                print(obj)
                if inspect.isclass(obj):
                    print(obj)
                    print(obj.__name__)
                    if obj.__name__ == "CVAEnvironment":
                        target_class = obj
            print("$%^&*")

            print(environment_class)
            print("@@@@@@@@@@@")
            environment_address = self.actor_system.createActor(environment_class)
            self.environments[environment_name] = environment_address
            logging.info("ENVIRONMENT STARTED")
            return environment_address


        def setup_environment_agents(self, environment_name, agent_class, num_agents=1):
            message = Message()
            message.set_directive("setup_agents")
            message.set_payload({"agent_class": agent_class,
                                 "num_agents": num_agents,
                                 "subject_id": environment_name})
            self.actor_system.tell(self.environments[environment_name], message)

        def setup_environment_institution(self, environment_address, institution_class):
            classname = institution_class.__module__ + "." + institution_class.__name__
            message = Message()
            message.set_directive("setup_institution")
            message.set_payload({"institution_class": institution_class })
            self.actor_system.tell(self.environments[environment_address], message)
            logging.info("INSTITUTION STARTED")

        def send_internal_message(self, address, message):
            self.actor_system.tell(address, message)

        def send_root_environment_message(self, environment_name, message):
            self.actor_system.tell(self.environments[environment_name], message)

        def kill_environment(self, environment_name):
            self.send(self.environments[environment_name], ActorExitRequest())

        def kill_subject_environment(self, environment_address):
            self.actor_system.tell(environment_address, ActorExitRequest())

    def __new__(self, logcfg=None):
        if SubjectContainer.__instance is None:
            SubjectContainer.__instance = SubjectContainer.__SubjectContainer(logcfg)
        return SubjectContainer.__instance



