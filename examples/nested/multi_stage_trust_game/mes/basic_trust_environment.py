from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import math
import random
import logging
import time
import datetime

@directive_enabled_class
class TrustEnvironment(Environment):
    @directive_decorator("start_environment")
    def start_environment(self, message:Message):
        self.provide_endowment()
        self.start_trust_game()

    def provide_endowment(self):
        endowment = 10
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("set_endowment")  # Set the directive (refer to 3. Make Messages) - has to match receiver decorator
        new_message.set_payload({"endowment": endowment})
        self.address_book.broadcast_message({"address_type": "agent"}, new_message)

    def start_trust_game(self):
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("start_trust")
        new_message.set_payload({"address_book": self.address_book.get_addresses()})
        self.send(self.address_book.select_addresses({"address_type": "institution"}), new_message)  