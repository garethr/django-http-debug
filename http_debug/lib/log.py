import logging
from logging.handlers import RotatingFileHandler

from django.conf import settings
    
def init_logging(name):
    """
    We need to initialise out loggers before we can use them
    but we only want to run this once, rather than once per call
    """
    # define our logger
    logger = logging.getLogger(name)
    # be less noisy about imported exceptions
    logging.raiseExceptions = 0
    
    # lets be nice and rotate our logs
    handler = RotatingFileHandler(
                  "%s_%s" % (settings.LOG_FILE, name), 
                  maxBytes=settings.MAX_LOG_FILE_SIZE, 
                  backupCount=settings.NUMBER_LOG_FILES
    )
    
    # nicely formatted messages please
    formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S')

    # make sure we actually use out formatting and rotating
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # and only log what we're interested in from the settings file
    logger.setLevel(getattr(settings, 'LOG_LEVEL', logging.NOTSET))

def get_logger(name):
    "Return the named logger"
    logger = logging.getLogger(name)
    # return the logger now ready for use
    return logger

# we only want one logger but calling addhandler multiple
# times ends up logging multiples to log messages
# we want to make sure we only initialise it once
# when this module is imported
log_initialised = False
if not log_initialised:
    log_initialised = True
    for name in settings.LOGS:
        init_logging(name)