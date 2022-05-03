import logging

class actorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' in logrecord.__dict__
class notActorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' not in logrecord.__dict__

#####
# The purpose of this file is to centralize the log configuration used for mTree
# This will effect primarily log messages directly using the python logging function
# mTree's own logging functions for experimental data is handled in a separate system
#####

logcfg = { 'version': 1,
           'formatters': {
               'normal': {'format': '%(asctime)s %(levelname)-8s %(message)s', 'datefmt':'%Y-%m-%d %H:%M:%S'},
               'actor': {'format': '%(asctime)s %(levelname)-8s %(actorAddress)s => %(message)s', 'datefmt':'%Y-%m-%d %H:%M:%S'}},
           'filters': { 'isActorLog': { '()': actorLogFilter},
                        'notActorLog': { '()': notActorLogFilter}},
           'handlers': { 'h1': {'class': 'logging.FileHandler',
                                'filename': 'system.log',
                                'formatter': 'normal',
                                'filters': ['notActorLog'],
                                'level': logging.INFO},
                         'h2': {'class': 'logging.FileHandler',
                                'filename': 'system.log',
                                'formatter': 'actor',
                                'filters': ['isActorLog'],
                                'level': logging.INFO},},
           'loggers' : { '': {'handlers': ['h1', 'h2'], 'level': logging.WARNING}}
         }