#! /usr/bin/env python3

# -----------------------------------------------------------------------------
# self-signed-certificates.py Loader for creating self-signed certificates.
# -----------------------------------------------------------------------------

import json
import logging
import os
import sys
import time
import traceback

__all__ = []
__version__ = "0.1.0"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2021-03-09'
__updated__ = '2021-03-10'

SENZING_PRODUCT_ID = "5019"  # See https://github.com/Senzing/knowledge-base/blob/master/lists/senzing-product-ids.md

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

# Configure logging. See https://docs.python.org/2/library/logging.html#levels

log_level_map = {
    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "fatal": logging.FATAL,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

log_format = '%(asctime)s %(message)s'
log_level_parameter = os.getenv("SENZING_LOG_LEVEL", "info").lower()
log_level = log_level_map.get(log_level_parameter, logging.INFO)
logging.basicConfig(format=log_format, level=log_level)

# -----------------------------------------------------------------------------
# Message handling
# -----------------------------------------------------------------------------

# 1xx Informational (i.e. logging.info())
# 3xx Warning (i.e. logging.warning())
# 5xx User configuration issues (either logging.warning() or logging.err() for Client errors)
# 7xx Internal error (i.e. logging.error for Server errors)
# 9xx Debugging (i.e. logging.debug())

MESSAGE_INFO = 100
MESSAGE_WARN = 300
MESSAGE_ERROR = 700
MESSAGE_DEBUG = 900

message_dictionary = {
    "100": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}I",
    "101": "Event: {0}",
    "102": "Context: {0}",
    "111": "Event: {0}",
    "112": "Context: {0}",
    "300": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}W",
    "700": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}E",
    "900": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}D",
    "998": "Debugging enabled.",
    "999": "{0}",
}


def message(index, *args):
    index_string = str(index)
    template = message_dictionary.get(index_string, "No message for index {0}.".format(index_string))
    return template.format(*args)


def message_generic(generic_index, index, *args):
    index_string = str(index)
    return "{0} {1}".format(message(generic_index, index), message(index, *args))


def message_info(index, *args):
    return message_generic(MESSAGE_INFO, index, *args)


def message_warning(index, *args):
    return message_generic(MESSAGE_WARN, index, *args)


def message_error(index, *args):
    return message_generic(MESSAGE_ERROR, index, *args)


def message_debug(index, *args):
    return message_generic(MESSAGE_DEBUG, index, *args)


def get_exception():
    ''' Get details about an exception. '''
    exception_type, exception_object, traceback = sys.exc_info()
    frame = traceback.tb_frame
    line_number = traceback.tb_lineno
    filename = frame.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, line_number, frame.f_globals)
    return {
        "filename": filename,
        "line_number": line_number,
        "line": line.strip(),
        "exception": exception_object,
        "type": exception_type,
        "traceback": traceback,
    }


def logging_info(message):
    print(message)


def logging_error(message):
    print(message)


def logging_warning(message):
    print(message)


def logging_debug(message):
    print(message)

# -----------------------------------------------------------------------------
# Lambda handler
# -----------------------------------------------------------------------------


def handler(event, context):

    result = {}

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        logger.info("Event: {0}".format(json.dumps(event)))
        if event['RequestType'] in ['Create', 'Update']:
            properties = event.get('ResourceProperties', {})
            describe_mount_targets_parameters = properties.get('DescribeMountTargetsParameters', {})
            result['response'] = 'Hello from AWS Lambda using Python' + sys.version + '!'
            logger.info("sleeping 10 seconds")
            time.sleep(10)
            logger.info("Done")
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
    finally:
        pass

    logging_info(message_info(101, json.dumps(event)))
    logging_info(message_info(102, context))
    logging.info(message_info(111, json.dumps(event)))
    logging.info(message_info(112, context))
    return result

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


if __name__ == "__main__":

    logging.debug(message_debug(998))

    event = {}
    context = {}

    response = handler(event, context)
    print(response)
