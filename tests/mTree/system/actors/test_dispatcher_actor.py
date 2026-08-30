import pytest
from thespian.actors import Actor, ActorExitRequest, ActorSystem

from mTree.core_actors.admin_message import AdminMessage
from mTree.system.actors.dispatcher_actor import DispatcherActor


class SystemStatusActor(Actor):
    def __init__(self):
        self.admin_message_stored = False
    
    def receiveMessage(self, msg, sender):
        match msg:
            case AdminMessage():
                self.admin_message_stored = True
            case str():
                if msg == "hello":
                    self.send(sender, "world")
                elif msg == "starting":
                    if self.admin_message_stored:
                        self.send(sender, "registered")
                    else:
                        self.send(sender, "failed")


# 2. Pytest Fixture for Actor System
@pytest.fixture
def actor_system():
    # Initialize the actor system
    system = ActorSystem()
    
    yield system
    # Teardown: shutdown all actors to clean up state
    system.shutdown()

# 3. Test Cases
def test_dispatcher_initialization(actor_system):
    # Arrange
    ssa = actor_system.createActor(SystemStatusActor, globalName="SystemStatusActor")
    dispatcher = actor_system.createActor(DispatcherActor)
    actor_system.tell(dispatcher, "starting")
    response = actor_system.ask(ssa, "starting")

    
    # Assert
    assert response == "registered"

