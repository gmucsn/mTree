import pytest
from dataclasses import dataclass

from mTree.examples.basic_auctions.mes.basic_auction_agent import BasicAuctionAgent

from thespian.actors import *


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


@pytest.fixture(scope="function")
def pytest_basic_actor_system(request):
    actor_system = ActorSystem()
    # actor = actor_system.createActor(BaseActorTest, globalName="test")
    # actor_system.tell(actor, "")
    def shutdown_actor_system():
        actor_system.shutdown()

    request.addfinalizer(shutdown_actor_system)
    return actor_system

def test_basic_message(pytest_basic_actor_system):
    actor = pytest_basic_actor_system.createActor(BasicAuctionAgent)
    test_value = pytest_basic_actor_system.ask(actor, "test")
    # pytest_basic_actor_system.tell(actor, "test")
    # pytest_basic_actor_system.listen()
    
    # pytest_basic_actor_system.listen()
    # print("test")
    assert test_value == 2
