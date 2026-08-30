
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.message import Message


@directive_enabled_class
class AuctionEnvironment(Environment):

    @directive_decorator("start_environment")
    def start_environment(self, message: Message):
        self.institution_address = self.address_book.select_addresses(
            {"address_type": "institution"}
        )
        self.send(
            self.institution_address, self.address_book.forward_address_book_message()
        )
        self.provide_endowment()
        self.start_auction()

    def provide_endowment(self):
        endowment = 60
        new_message = Message()  # declare message
        new_message.set_sender(
            self.myAddress
        )  # set the sender of message to this actor
        new_message.set_directive(
            "set_endowment"
        )  # Set the directive (refer to 3. Make Messages) - has to match receiver decorator
        new_message.set_payload({"endowment": endowment})

        self.send_message(
            "set_endowment",
            self.address_book.select_addresses({"address_type": "agent"}),
            {"endowment": endowment},
        )

    def start_auction(self):

        new_message = Message()  # declare message
        new_message.set_sender(
            self.myAddress
        )  # set the sender of message to this actor
        new_message.set_directive("start_auction")
        new_message.set_payload({"address_book": self.address_book.get_addresses()})
        self.send(
            self.address_book.select_addresses({"address_type": "institution"}),
            new_message,
        )
