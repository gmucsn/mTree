import pytest
from mes.basic_auction_agent import AuctionAgent
from mTree.microeconomic_system.message import Message


def component_wrapper(component):
    class Wrapper(component):
        def __init__(self):
            print("SIMPLE")
            self.debug = False
            self.prepare()

            self.log_level = 1
            self.log_level = 1
            self.log_actor = None
            self.previous_message = None

        def myAddress(self):
            return "SELF"

        def send(self, target_address, new_message):
            self.previous_message = new_message

        def get_previous_message(self):
            print("------")
            print(self.previous_message)
            print("^^^^^")
            return self.previous_message

        def __str__(self):
            return "test object"

        def log_message(self, logline, target=None, level=None):
            pass

    bare_component = Wrapper()
    return bare_component


class TestAuctionAgent:
    @pytest.fixture(scope="class", autouse=True)
    def prepare_component(self):
        testing_agent = component_wrapper(AuctionAgent)
        # print (dir(testing_agent))
        return testing_agent

    def test_name_in_header(self, prepare_component):
        print(prepare_component)
        new_message = Message()  # declare message
        new_message.set_sender("TEST")  # set the sender of message to this actor
        new_message.set_directive("bid_for_item")
        new_message.set_payload({"value_estimate": 10, "error": 2})

        prepare_component.start_bidding(new_message)
        message_out = prepare_component.get_previous_message()

        assert message_out.get_payload()["bid"] >= 0
