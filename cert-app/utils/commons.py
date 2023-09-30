import logging
METRIC_LOG_LEVEL = 60
AUDIT_LOG_LEVEL = 70
FORMATTER = logging.Formatter('%(asctime)s - %(message)s')
FORMATTER_LEVEL = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

def setup_logger(name, log_file, level=logging.DEBUG, format=FORMATTER):
    handler = logging.FileHandler(filename=log_file, mode='a', encoding='utf-8')
    handler.setFormatter(format)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def write_metric(message=dict):
    format_message = ' | '.join(f'{key} : {value}' for key, value in message.items())
    metric_logger.log(METRIC_LOG_LEVEL, format_message)


def write_audit(message=dict):
    format_message = ' | '.join(f'{key} : {value}' for key, value in message.items())
    audit_logger.log(AUDIT_LOG_LEVEL, format_message)


def write_log(level=logging.INFO, message=dict):
    format_message = ' | '.join(f'{key} : {value}' for key, value in message.items())
    logger.log(level, format_message)


# Metric logger
metric_logger = setup_logger('metric_logger', './cert-app/logs/logging_application.metric' ,METRIC_LOG_LEVEL )
#metric_logger.setLevel(METRIC_LOG_LEVEL)

# Audit logger
audit_logger = setup_logger('audit_logger', './cert-app/logs/logging_application.audit',AUDIT_LOG_LEVEL)

#Logger 
logger = setup_logger('log_logger', './cert-app/logs/global.log', format=FORMATTER_LEVEL)