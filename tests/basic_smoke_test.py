import pytest
from thespian.actors import *
from dataclasses import dataclass

class BaseActorTest(Actor):
    def __init__(self):
        self.actor_system = None

    def receiveMessage(self, msg, sender):
        match msg:
            case str():
                self.state = "test"
                self.send
            case _:
                pass


@pytest.fixture(scope=function)
def pytest_actor_system(request):
    actor_system = ActorSystem("multiPrcQueueBase")
    actor = actor_system.createActor(BaseActorTest, globalName="test")
    actor_system.tell(actor, "")
    def shutdown_actor_system():
        actor_system.shutdown()

    request.addfinalizer(shutdown_actor_system)
    return actor_system

def test_basic_message(pytest_actor_system):
    
    actor = pytest_actor_system.createActor(object, globalName="test")
    test_value = pytest_actor_system.ask(actor, "test")
    pytest_actor_system.tell(actor, "test")
    pytest_actor_system.listen()
    
    pytest_actor_system.listen()
    print("test")
    assert test_value == 2
        