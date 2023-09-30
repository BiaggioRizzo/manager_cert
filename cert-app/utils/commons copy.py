import logging

METRIC_LOG_LEVEL = 60
AUDIT_LOG_LEVEL = 70

def write_metric(message=dict):
    logging.addLevelName(METRIC_LOG_LEVEL,'METRIC')
    logging.basicConfig (filename='logging_application.metric', filemode="a",encoding='utf-8', format='%(asctime)s - %(message)s' )
    logger_metric = logging.getLogger('metric_logger')
    format_message = (' | '.join(f'{key} : {value}' for key, value in message.items()))
    logger_metric.log(METRIC_LOG_LEVEL,format_message)


def write_audit(message=dict):
    logging.addLevelName(AUDIT_LOG_LEVEL,'AUDIT')
    logging.basicConfig (filename='logging_application.audit', filemode="a",encoding='utf-8', format='%(asctime)s - %(message)s' )
    logger_audit = logging.getLogger('audit_logger')
    format_message = (' | '.join(f'{key} : {value}' for key, value in message.items()))
    logger_audit.log(AUDIT_LOG_LEVEL,format_message)

def write_log(level=10,message=dict):
    logging.basicConfig (filename='global.log', filemode="a",encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s' )
    logger_log = logging.getLogger('log_logger')
    format_message = (' | '.join(f'{key} : {value}' for key, value in message.items()))
    logger_log.log(level,format_message)


formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# first file logger
logger = setup_logger('first_logger', 'first_logfile.log')
logger.info('This is just info message')

# second file logger
super_logger = setup_logger('second_logger', 'second_logfile.log')
super_logger.error('This is an error message')

def another_method():
   # using logger defined above also works here
   logger.info('Inside method')