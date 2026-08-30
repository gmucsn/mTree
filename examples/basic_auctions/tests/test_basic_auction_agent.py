import pytest

from mTree.examples.basic_auctions.mes.basic_auction_agent import BasicAuctionAgent

from thespian.actors import *
from mTree.microeconomic_system.message import Message

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

from mTree.microeconomic_system.initialization_messages import *
from mTree.microeconomic_system.probe_messages import ProbeMessage

def test_basic_message(pytest_basic_actor_system):
    actor = pytest_basic_actor_system.createActor(BasicAuctionAgent)
    # Initialization Sequence

    new_message = Message()
    # new_message.set_sender(self.myAddress)
    new_message.set_directive("set_endowment")
    new_message.set_payload({"endowment": 15})
    pytest_basic_actor_system.tell(actor, new_message)
    probe = pytest_basic_actor_system.ask(actor, ProbeMessage())
    assert type(probe) == ProbeMessage

    
    # Initialization Message 2
    pytest_basic_actor_system.tell(actor, "startup")
    # pytest_basic_actor_system.tell(actor, StartupPayload(startup_payload={}))
    # pytest_basic_actor_system.tell(actor, AddressBookPayload(address_book_payload={}))
    

    test_value = 1 # pytest_basic_actor_system.ask(actor, "test")
    # pytest_basic_actor_system.tell(actor, "test")
    # pytest_basic_actor_system.listen()
    
    # pytest_basic_actor_system.listen()
    # print("test")
    assert test_value == 2



def test_setting_endowment():
    test_endowment = 15
    basic_auction_agent = BasicAuctionAgent()
    
    new_message = Message()
    new_message.set_directive("set_endowment")
    new_message.set_payload({"endowment": test_endowment})
    basic_auction_agent.set_endowment(new_message)


    assert basic_auction_agent.endowment == test_endowment


def test_start_bidding():
    value_estimate = 15
    basic_auction_agent = BasicAuctionAgent()
    
    new_message = Message()
    new_message.set_sender = "LOCAL"
    new_message.set_directive("start_bidding")
    new_message.set_payload({"value_estimate": value_estimate})
    basic_auction_agent.start_bidding(new_message)


    assert basic_auction_agent.endowment == test_endowment
