
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.institution import Institution


@directive_enabled_class
class BasicInstitution(Institution):
    def __init__(self):
        pass
