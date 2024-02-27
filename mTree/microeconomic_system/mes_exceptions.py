class UndefinedDirectiveException(Exception):
    def __init__(self, directive, message="Directive not defined. Check your MES component file!"):
        self.directive = directive
        self.message = message
    
    def __str__(self):
        return f'!! MES Unedfined Directive Exception!! Directive:{self.directive} -- {self.message}'

class BadSimulationConfigurationFile(Exception):
    def __init__(self, directive, message="Bad Simulation Configuration File! Check Format.", source_file=None):
        self.directive = directive
        self.message = message
        self.source_file = source_file
    
    def __str__(self):
        return f"mTree Bad Simulation Configuration File! Check Format. { self.source_file }"
