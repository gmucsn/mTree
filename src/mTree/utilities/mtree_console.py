import atexit

from mTree.system.actor_system_controller import ActorSystemController
from mTree.utilities.console.mtree_console_app import MTreeConsoleApp
from thespian.actors import *

# lsof -nP -i:19000


@atexit.register
def shutdown_actor_system():
    ActorSystemController.shutdown()
    print("mTree finished shutting down")


def main():
    print("mTree Console")
    actor_system = ActorSystemController.startup()

    mtree_console_app = MTreeConsoleApp()
    mtree_console_app.run()

    # capabilities = dict([("Admin Port", 19000)])
    # asys = ActorSystem(systemBase ="multiprocTCPBase", capabilities=capabilities)
    # try:
    # hello = actor_system.createActor(Hello)
    # goodbye = actor_system.createActor(Goodbye)
    # greeting = actor_system.ask(hello, 'are you there?', timedelta(seconds=1.5))
    # print(greeting + '\n' + actor_system.ask(goodbye, None,
    #                                             timedelta(milliseconds=100)))
    # except  Exception as e:
    #     print(e)

    # actor_system = ActorSystemController(True)
    # capabilities = dict([("Admin Port", 19020)])
    # asys = ActorSystem(systemBase ="multiprocTCPBase", capabilities =capabilities) #@, logDefs=logcfg)
    # asys = ActorSystem('multiprocTCPBase')systemBase = None,
    #    capabilities = None,
