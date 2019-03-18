"""
Helper function for agents
"""

import multiprocessing
import os
import pickle
import queue
import socket
import threading
import traceback
from functools import wraps
from inspect import getframeinfo, stack
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from random import uniform
from sys import _getframe
from time import sleep, time
from timeit import default_timer
from typing import Callable, List, Any

import requests
from google.cloud import translate

from agents.agents_utils.utils_constants import MAX_INT, TIMEOUT_INTERVAL, ENGLISH, MARKETS, AGENT_UTILS_NAME, \
    AGENTS_PATH, DOWNLOADS_DIR, UNDEFINED_LANGUAGE, USER_DEFINED_MARKETS, MARKET_LANGUAGES, MARKET_TRANSLATE_LANGUAGES
from utils import logger

translate_client = translate.Client()


# TODO: use 'inspect' instead of protected '_getframe'
def get_function_name(level: int = 1) -> str:
    """
    Gets the current function name
    :return:
    """
    return _getframe(level).f_code.co_name


def time_usage(debug_name: str):
    """
    Time calculating wrapper for logger.debug output
    :param debug_name:
    :return:
    """

    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(debug_name,
                         '\x1b[33m[{}]\x1b[0m is started'
                         .format(func.__name__))
            beg_ts = default_timer()
            retval = func(*args, **kwargs)
            end_ts = default_timer()
            elapsed_time = end_ts - beg_ts

            # elapsed_time_per_function is used for storing summary time elapsed per function with `time_usage` wrapper.
            # Bellow condition is used for adding information about time and number of calls in function
            if func.__name__ in time_usage.elapsed_time_per_function:
                time_usage.elapsed_time_per_function[func.__name__]['time'] += elapsed_time
                time_usage.elapsed_time_per_function[func.__name__]['calls'] += 1
            else:
                time_usage.elapsed_time_per_function[func.__name__] = {'time': elapsed_time, 'calls': 1}
            if logger.console_level == logger.DEBUG_LEVEL:
                logger.debug(debug_name,
                             '\x1b[33m[{}]\x1b[0m is performed in [{}] seconds.'
                             .format(func.__name__, elapsed_time))
            return retval

        return wrapper

    return real_decorator


# Using this Dict, you can see how many time was spent per function with `time_usage` decorator.
time_usage.elapsed_time_per_function = {}


def full_debug(logger_name: str, message: str) -> None:
    """

    :param logger_name:
    :param message:
    :return:
    """
    caller = getframeinfo(stack()[1][0])
    # TODO: read the 'logger_name' from a real path?..
    logger.debug(logger_name,
                 '[{}::{}:{}] {}'.format(caller.filename,
                                         caller.function,
                                         caller.lineno,
                                         message))


def get_size_from_path(start_path: str = '.') -> int:
    """Returns the size of directory or file (cascade)"""
    # TODO: Check if it exists
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            total_size += os.path.getsize(fullpath)
    return total_size


def timeout(seconds: int = TIMEOUT_INTERVAL) -> None:
    """
    Sleeps for the given time
    :param seconds: Seconds to sleep?..
    :return: Nothing
    """
    sleep(seconds)


def wait_between(_from: int, _to: int) -> None:
    """Waits between the given parameters"""
    if _from <= _to:
        rand = uniform(_from, _to)
        sleep(rand)


def make_debug_line(debug_name: str, num: int = 1, length: int = 66, symbol: str = '-') -> None:
    """
    Prints separator-line of given `length` `num` of times

    :param num:
    :param length:
    :param symbol:
    :return:
    """
    for _ in range(num):
        logger.debug(debug_name, f'{symbol * length}')


NUM_OF_THREADS = 15
thread_pool = None

NUM_OF_PROCESSES = 10
process_pool = None


def execute_function_in_parallel(func: Callable, list_args: List, processes: bool = False,
                                 local_pool: bool = False, num_threads: int = NUM_OF_THREADS,
                                 num_processes: int = NUM_OF_PROCESSES) -> List:
    """
    Execute a function in parallel using ThreadPool or ProcessPool
    :param local_pool: create a new pool of threads/processes
    :param num_processes: a num of processes to create
    :param num_threads: a num of threads to create
    :param processes: execute tasks in separate processes
    :param func: a func to call
    :param list_args: an array containing calling params
    :return: an array with results
    """
    if not (func and list_args):
        return []

    if local_pool:
        pool = ThreadPool(num_threads) if not processes else Pool(num_processes)
    else:
        global process_pool
        if processes:
            if not process_pool:
                process_pool = Pool(NUM_OF_PROCESSES)
            pool = process_pool
        else:
            global thread_pool
            if not thread_pool:
                thread_pool = ThreadPool(NUM_OF_THREADS)
            pool = thread_pool
    results_tmp = pool.starmap_async(func, list_args)
    results = [result for result in results_tmp.get() if result is not None]
    if local_pool:
        pool.close()
    return results


def execute_list_of_functions_in_parallel(funcs: List[Callable], processes: bool = False,
                                          local_pool: bool = False, num_threads: int = NUM_OF_THREADS,
                                          num_processes: int = NUM_OF_PROCESSES) -> List:
    """
    Execute a list of functions in parallel
    :param funcs: a list of functions to call
    :param processes: execute tasks in separate processes
    :param local_pool: create a new pool of threads/processes
    :param num_threads: a num of threads to create
    :param num_processes: a num of processes to create
    :return: an array with results
    """

    def execute_function(func: Callable):
        return func()

    return execute_function_in_parallel(execute_function, [(func,) for func in funcs], processes, local_pool,
                                        num_threads, num_processes)


def clamp(val: float, min_: float, max_: float) -> float:
    """Clamps (or clips) the given float value between min_ and max_"""
    return max(min_, min(val, max_))


def get_market_by_language(language):
    return MARKETS.get(language, MARKETS[ENGLISH])


def get_language_by_market(market):
    """
    Gets languag code from bing market
    :param market: market code
    :return: language code from google api standard
    """
    if not market:
        return None
    market_code = USER_DEFINED_MARKETS.get(market, '')
    market_language = MARKET_LANGUAGES.get(market_code, '')  # detect source language from market search
    # bing and google language codes differ
    google_language_code = MARKET_TRANSLATE_LANGUAGES.get(market_language, '')
    return google_language_code

def detect_language(keywords):
    """
    Detect a language here from a query

    :param keywords: search query
    :return: a language of the query
    """
    if len(keywords) > 2:
        try:
            return translate_client.detect_language(keywords).get('language', ENGLISH)
        except Exception as e:
            logger.warning(AGENT_UTILS_NAME, f'Could not detect the language of the query: "{keywords}".'
                                             f' Error message: {e}')


def detect_market(keywords):
    """
    Detect a language here from the query, and then add a market

    :param keywords: search query
    :return: market associated with a detected language
    """
    language = ENGLISH
    detected_language = detect_language(keywords)
    if detected_language:
        language = detected_language

    return get_market_by_language(language)


def translate(text: str, from_language: str = None, to_language: str = ENGLISH) -> str:
    """
    Translate a piece of text
    :param text: a text to translate
    :param from_language: original language, leave empty to detect it from the text
    :param to_language: desired language
    :return: translated text or an original one, if translation wasn't found
    """
    if not text:
        return ''

    if not to_language:
        to_language = ENGLISH

    if from_language == UNDEFINED_LANGUAGE:
        from_language = None

    try:
        if from_language:
            translation = translate_client.translate(text, source_language=from_language,
                                                     target_language=to_language)
        else:
            translation = translate_client.translate(text, target_language=to_language)
        text = translation.get('translatedText', '')
    except Exception as e:
        logger.warning(AGENT_UTILS_NAME, f'Could not translate query: "{text}" to {to_language}.'
                                         f' Error message: {e}')

    return text


def distance_between_positions(positions_1: List[int], positions_2: List[int]) -> float:
    """
    Find a minimum distance between positions in two arrays
    :param positions_1: an array containing positions of the first element
    :param positions_2: an array containing positions of the second element
    :return: min distance
    """
    # Sliding window method
    min_dist = MAX_INT

    if not (positions_1 and positions_2):
        return min_dist

    i = 0
    j = 0
    while i < len(positions_1) and j < len(positions_2):
        min_dist = min(min_dist, abs(positions_1[i] - positions_2[j]))
        if positions_1[i] < positions_2[j]:
            i += 1
        else:
            j += 1
    if i == len(positions_1):
        while j < len(positions_2):
            min_dist = min(min_dist, abs(positions_1[i - 1] - positions_2[j]))
            j += 1
    else:
        while i < len(positions_1):
            min_dist = min(min_dist, abs(positions_1[i] - positions_2[j - 1]))
            i += 1

    return min_dist


def save_file(object_to_save: Any, filename: str) -> None:
    """
    Save an object to file using pickle
    :param object_to_save: an object to save
    :param filename: a filename relevant to AGENTS_PATH
    :return: None
    """
    try:
        file_name = os.path.join(AGENTS_PATH, filename)
        with open(file_name, 'wb') as file:
            pickle.dump(object_to_save, file, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        logger.error(AGENT_UTILS_NAME, f'Error while writing to file {filename}. Error {e}')


def load_file(filename: str) -> Any:
    """
    Loads an object from a file using pickle
    :param filename: a filename relevant to AGENT_PATH
    :return: the object
    """
    try:
        file_name = os.path.join(AGENTS_PATH, filename)
        with open(file_name, 'rb') as file:
            unserialized_data = pickle.load(file)
    except Exception as e:
        logger.error(AGENT_UTILS_NAME, f'Error while reading from file {filename}. Error {e}')
        return None

    return unserialized_data


def execute_function_in_parallel_with_time_limit(func: Callable, list_args: List, time_limit_sec: float,
                                                 num_threads: int = multiprocessing.cpu_count(),
                                                 return_list: List = list()) -> List:
    def start_worker(func: Callable, return_list: List, tasks_queue: queue.Queue, time_limit_sec: float,
                     start_time: float = time()) -> None:
        """
        Temporary (time limited) runs a start_worker: execute the given function on the given queue.

        :param func: function to execute
        :param return_list: sharable Manager.list for returned data
        :param tasks_queue: queue.Queue for task storing
        :param time_limit_sec: limitation of time (in seconds)
        :param start_time: UNIX time

        :return: Nothing
        """
        while True:
            if time() - start_time < time_limit_sec:
                try:
                    item = tasks_queue.get()
                    if item is None:
                        break
                    return_list.append(func(*item))
                    tasks_queue.task_done()
                except Exception as e:
                    logger.exception(AGENT_UTILS_NAME, f'Error in start_worker: {e}\n{traceback.print_exc()}')
                    tasks_queue.task_done()
                    continue
            else:
                # Time exceed
                logger.info(AGENT_UTILS_NAME, 'Time for start_worker was exceed')
                try:
                    while not tasks_queue.empty():
                        tasks_queue.get(block=False, timeout=0)
                        tasks_queue.task_done()
                        logger.debug(AGENT_UTILS_NAME, f'{tasks_queue.qsize()} tasks remain.')
                    logger.debug(AGENT_UTILS_NAME, f'Tasks queue is empty for function {func.__name__}.')
                except queue.Empty:
                    logger.info(AGENT_UTILS_NAME, 'Tasks queue is empty.')
                    break
                except Exception as e:
                    logger.exception(AGENT_UTILS_NAME, f'Error in start_worker. Message: {e}')
                    break
                break

    q = queue.Queue()
    threads = []

    try:
        for i in range(num_threads):
            t = threading.Thread(target=start_worker, args=(func, return_list, q, time_limit_sec))
            t.start()
            threads.append(t)

        for item in list_args:
            q.put(item)

        # block until all tasks are done
        q.join()

        # stop workers
        for i in range(num_threads):
            q.put(None)

        for t in threads:
            t.join()

        return return_list

    except Exception as e:
        logger.exception(AGENT_UTILS_NAME, f'Error with using `execute_function_in_parallel_with_time_limit` function.',
                         e)
        return []


def get_my_local_ip():
    """
    Get a local ip address of the machine
    :return: an ip
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def get_my_ip() -> str:
    """
    Get an ip address of the machine
    :return: an ip
    """
    local = None
    try:
        local = os.environ[f'USE_LOCAL_IP']
    except KeyError as e:
        pass

    if local:
        return get_my_local_ip()

    response = None
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.exception(AGENT_UTILS_NAME, f'Could not get an ip address. Error {e}', response)
        return ''


def str_to_bool(bool_string: str) -> bool:
    """
    Uses with flask.request.form.get to cast str 'False' or 'True' to bool
    :param bool_string: 'False', 'True', or any other string
    :return: False if bool_string is 'False' or empty, otherwise True
    """
    if not bool_string or bool_string == 'False':
        return False
    else:
        return True


def create_downloads_dir_if_not_exist():
    """
    Creates directory to store static files used by agents
    """
    path_to_the_downloads_dir = os.path.join(AGENTS_PATH, DOWNLOADS_DIR)
    if not os.path.exists(path_to_the_downloads_dir):
        logger.info(AGENT_UTILS_NAME,
                    f'Download directory does not exist. Creating at {path_to_the_downloads_dir}')
        os.mkdir(path_to_the_downloads_dir)
