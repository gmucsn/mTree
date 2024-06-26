import os

from mTree.core_actors.dispatcher import Dispatcher
from mTree.core_actors.system_status_actor import SystemStatusActor

from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.admin_message import AdminMessage

from mTree.server.log_config import logcfg


from thespian.actors import *

    
class ActorSystemController:
    actor_system_base = "multiprocTCPBase"
    actor_system_capabilities = dict([("Admin Port", 19000)])
    admin_actors = []

    @staticmethod
    def startup():
        os.environ['THESPLOG_THRESHOLD'] =  'DEBUG'
        os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "THESPIAN_OUT.LOG")

        actor_system = ActorSystem(systemBase=ActorSystemController.actor_system_base,
            capabilities=ActorSystemController.actor_system_capabilities,
            logDefs=logcfg)

        # The System Status Actor should be the first actor started.
        # This actor will maintain a list of all known actors and what have you
        system_status_actor = actor_system.createActor(SystemStatusActor, globalName="SystemStatusActor")
        actor_system.tell(system_status_actor, "starting")
        ActorSystemController.admin_actors.append("SystemStatusActor")

        dispatcher = actor_system.createActor(Dispatcher, globalName="Dispatcher")
        actor_system.tell(dispatcher, "starting")
        ActorSystemController.admin_actors.append("Dispatcher")

        return actor_system

        
    @staticmethod
    def shutdown():
        print("Shutting down actor system....")
        ActorSystem(systemBase=ActorSystemController.actor_system_base,
            capabilities=ActorSystemController.actor_system_capabilities).shutdown()

    @staticmethod
    def retrieve_connection():
        actor_system = ActorSystem(systemBase=ActorSystemController.actor_system_base,
            capabilities=ActorSystemController.actor_system_capabilities)

        return actor_system

        
    @staticmethod
    def system_inquiry(actor, message):
        actor_system = ActorSystem(systemBase=ActorSystemController.actor_system_base,
            capabilities=ActorSystemController.actor_system_capabilities)
        target_actor = actor_system.createActor(Actor, globalName=actor)
        response = actor_system.ask(target_actor, message)
        
        return response

    