import atexit

from thespian.actors import *

from mTree.system.actor_system_controller import ActorSystemController
from mTree.utilities.console.mtree_console_app import MTreeConsoleApp


@atexit.register
def shutdown_actor_system() -> None:
    ActorSystemController.shutdown()
    print("mTree finished shutting down")


def main():
    actor_system = ActorSystemController.startup()

    mtree_console_app = MTreeConsoleApp()
    mtree_console_app.run()
