import datetime
import logging
import math
import random
import time

from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.message import Message


@directive_enabled_class
class AuctionEnvironment(Environment):

    @directive_decorator("start_environment")
    def start_environment(self, message: Message):
        self.institution_address = self.address_book.select_addresses(
            {"address_type": "institution"}
        )
        self.log_message(self.institution_address)
        self.log_message("env forward")
        # self.address_book.forward_address_book(self.institution_address)
        self.send(
            self.institution_address, self.address_book.forward_address_book_message()
        )
        self.log_message("env done forward")
        self.provide_endowment()
        self.log_message("env start auc")
        self.start_auction()

    def provide_endowment(self):
        endowment = 30
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

        # new_message = Message()  # declare message
        # new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        # new_message.set_directive("start_auction")
        # self.send(self.institution_address, new_message)
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
