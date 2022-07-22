from thespian.actors import *
from thespian.initmsgs import initializing_messages
from datetime import datetime, timedelta
import time
import traceback
import json
import os
import sys

import logging

from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.log_message import LogMessage
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
from mTree.microeconomic_system.address_book import AddressBook
from mTree.microeconomic_system.mes_exceptions import *
from mTree.microeconomic_system.sequence_event import SequenceEvent

class MESContainer(Actor):
    def receiveMessage(self, message, sender):
        logging.info('MES Container Started')
