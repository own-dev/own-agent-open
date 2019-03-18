# please, pay attention to 'current_level'
# messages with level that is lower than 'current_level' will not be logged
# messages with level that is lower that 'console_level' will not be written to console
# usage:
#
# from agents_platform import logger
#
#
# logger.debug('current_module_name', 'debug')
# logger.info('current_module_name', 'information')
# logger.warning('current_module_name', 'warning')
# logger.error('current_module_name', 'error')
# logger.exception('current_module_name', 'exception')

import datetime
import traceback
from multiprocessing import Lock

import google.cloud.logging
import requests

from utils.constants import *

known_loggers = ['engine', 'own_adapter', 'test', 'agents_utils', 'utils', 'jokes']
levels = {DEBUG_LEVEL: 0, INFO_LEVEL: 1, WARNING_LEVEL: 2, EXCEPTION_LEVEL: 3, ERROR_LEVEL: 4}

# we can get the level from config, or change it while debugging
current_level = DEBUG_LEVEL
console_level = DEBUG_LEVEL

mutex = Lock()

google_cloud_project_name = None
try:
    google_cloud_project_name = os.environ[f'GOOGLE_CLOUD_PROJECT_NAME']
except KeyError as e:
    print(f'GOOGLE_CLOUD_PROJECT_NAME environment variable is not set up, '
          f'or the project by the given name was not set up correctly.')

google_logging_client = google.cloud.logging.Client(f'{google_cloud_project_name}')
google_logger = google_logging_client.logger(GOOGLE_LOGGER_NAME)

agents_environment = os.environ.get('AGENTS_ENVIRONMENT', None)


# returns True if writing to a file was successful, and False - in other cases
def __log_message(logger_name, message, level, response=None):
    """
    Logs a messages. Prints it to console, file or sends to google logs
    :param logger_name: a name of the one who wants to log
    :param message: a message to log
    :param level: a level of the message, possible levels are in levels variable
    :param response: a response of a request for which the was an error
    :return: True if message was logged, False otherwise
    """
    result = False
    stack_trace = ''.join(traceback.format_stack())
    headers = None

    response_body = None
    if response:
        try:
            headers = response.headers

            if isinstance(response, requests.Response):
                response_body = response.json()
            else:
                response_body = response.read().decode()
        except Exception as e:
            try_print_to_console(f'Unknown type of response. Error message: {e}')

    if logger_name not in known_loggers:
        return result

    if levels[level] >= levels[current_level] or levels[level] >= levels[console_level]:
        now = datetime.datetime.utcnow()
        formatted_time = now.strftime('%Y.%m.%d %H:%M:%S')
        formatted_day = now.strftime('%Y.%m.%d')
        log_message = f'[{logger_name}] {message}'
        log_message_to_log_files_and_console = f'{formatted_time} [{level}] {log_message}'

        # write to a file
        if levels[level] >= levels[current_level]:
            mutex.acquire(timeout=5)
            try:
                agents_home_directory = os.environ['OWN_AGENTS_PATH']
                logs_directory = os.path.join(agents_home_directory, 'logs', logger_name)
                if not os.path.exists(logs_directory):
                    os.makedirs(logs_directory)
            finally:
                mutex.release()
            try:
                log_file_name = os.path.join(logs_directory, f'{formatted_day}.log')

                # If 'AGENTS_ENVIRONMENT' env var is 'production' (i.e. agents platform in production mode)
                if agents_environment == PRODUCTION_ENVIRONMENT:
                    google_logger.log_struct({
                        'message': log_message,
                        'agent': logger_name,
                        'stack_trace': stack_trace,
                        'timestamp_from_agent': formatted_time,  # as time between request arriving to google logs
                        # and time of exception on the server may differ
                        'headers': headers.get('x-uberblik-error', headers) if headers else None,
                        'response_body': response_body
                    }, severity=google_logger_enums.get(level, WARNING_LEVEL))
                else:
                    with open(log_file_name, 'a', encoding='utf-8') as log_file:
                        print(log_message_to_log_files_and_console, file=log_file)
                result = True
            except OSError as e:
                try_print_to_console(f'Directory for logs was not created. Error message: {e}')
            except KeyError as e:
                try_print_to_console(f'The OWN_AGENTS_PATH environment variable is not defined. Error message: {e}')
            except Exception as e:
                try_print_to_console(f'File handler for logs was not created. Exception message: {e}')

        # write to console
        if levels[level] >= levels[console_level]:
            try:
                print(log_message_to_log_files_and_console)
            except Exception as e:
                try_print_to_console(f'Console handler for logs was not created. Error message: {e}')

    return result


# wrappers for different levels
def debug(logger_name, message, response=None):
    return __log_message(logger_name, message, DEBUG_LEVEL, response)


def info(logger_name, message, response=None):
    return __log_message(logger_name, message, INFO_LEVEL, response)


def warning(logger_name, message, response=None):
    return __log_message(logger_name, message, WARNING_LEVEL, response)


def error(logger_name: object, message: object, response: object = None) -> object:
    return __log_message(logger_name, message, ERROR_LEVEL, response)


def exception(logger_name, message, response=None):
    return __log_message(logger_name, message, EXCEPTION_LEVEL, response)


# in case if python can fail while printing to console
# TODO: check if that case is possible
def try_print_to_console(message):
    try:
        print(message)
    except:
        # do nothing, because what else can we do?
        pass
