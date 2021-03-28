import logging

class actorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' in logrecord.__dict__
class notActorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' not in logrecord.__dict__
class informationLogFilter(logging.Filter):
    def filter(self, logRecord):
        return logRecord.levelno == 24
class experimentLogFilter(logging.Filter):
    def filter(self, logRecord):
        return logRecord.levelno == 25


logger = logging.getLogger("mTree")
# set success level
logger.EXPERIMENT = 25  # between WARNING and INFO
logging.addLevelName(logger.EXPERIMENT, 'EXPERIMENT')
logger.MESSAGE = 24  # between WARNING and INFO
logging.addLevelName(logger.MESSAGE, 'MESSAGE')
#setattr(logging, 'experiment', lambda message, *args: logger._log(logging.EXPERIMENT, message, args))


logcfg = { 'version': 1,
           'formatters': {
               'normal': {'format': '%(asctime)s - %(levelname)-8s %(message)s'},
               'actor': {'format': '%(asctime)s - %(levelname)-8s  => %(message)s'}},
           'filters': { 'isActorLog': { '()': actorLogFilter},
                        'notActorLog': { '()': notActorLogFilter},
                        'experimentLogFilter': {'()': experimentLogFilter},
                        'informationLogFilter': {'()': informationLogFilter}},
           'handlers': { 'h1': {'class': 'logging.FileHandler',
                                'filename': 'warnings.log',
                                'formatter': 'normal',
                                'filters': ['notActorLog'],
                                'level': logging.WARN},
                         'h2': {'class': 'logging.FileHandler',
                                'filename': 'messages.log',
                                'formatter': 'actor',
                                'filters': ['informationLogFilter'],
                                'level': 24},
                         'experiment': {'class': 'logging.FileHandler',
                                'filename': 'experiment.log',
                                'formatter': 'normal',
                                'filters': ['experimentLogFilter'],
                                'level': 25},
                         },
           'loggers' : { 'mTree': {'handlers': ['h1', 'h2', 'experiment'], 'level': logging.DEBUG}}
         }