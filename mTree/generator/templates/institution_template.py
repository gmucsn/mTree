import logging
import random

from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.message import Message


@directive_enabled_class
class NAME(Institution):
    def __init__(self):
        pass
