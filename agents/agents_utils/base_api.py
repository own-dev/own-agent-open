"""
Base class to implement API access methods
"""
import atexit
import threading
from abc import abstractmethod
from datetime import timedelta, datetime
from time import sleep
from typing import Optional, Dict

from agents.agents_utils.agents_helper import execute_function_in_parallel
from agents.agents_utils.utils_constants import AGENT_UTILS_NAME
from utils import logger
from utils.credentials_store import CredentialsStore

TIME_BETWEEN_REQUESTS_KEY = 'time_between_requests'
ACTIVE_KEY = 'active'
LAST_REQUEST_KEY = 'last_request'
API_INSTANCE_KEY = 'api_instance'
CREDENTIALS_ID_KEY = 'credentials_id'

SLEEP_TIME_BETWEEN_CHECK_TO_RELEASE_A_KEY = 0.05


class BaseAPI:
    """
    Abstract class for API access instance
    
    IMPORTANT: You need to call release_credentials when you are not using them
    """
    MAX_NUMBER_OF_CREDENTIALS = 3

    def __init__(self, name: str, used_by: str, max_number_of_credentials: int = 3):
        """
        Initialise class
        :param name: a name of a service
        :param used_by: ip of agent which use credentials
        """
        self.MAX_NUMBER_OF_CREDENTIALS = max_number_of_credentials
        self.db = CredentialsStore(name)
        self.name = name
        self.credentials = {}
        self.lock = threading.Lock()
        self.used_by = used_by
        self.max_index = 0
        atexit.register(lambda: self.release_credentials(call_from_atexit=True))

    @abstractmethod
    def _get_api_instance(self) -> Optional[Dict]:
        """
        Get API instance. API instance should throw an error when rate limit reached with message
        containing 'Rate limit exceeded'
        :return: dict containing:
            TIME_BETWEEN_REQUESTS_KEY: time to wait between requests,
            API_INSTANCE_KEY: an object of API,
            CREDENTIALS_ID_KEY: id of credentials
            ACTIVE_KEY: True,
        """
        raise NotImplementedError

    def _add_new_credentials(self) -> bool:
        """
        Add new credentials to a pool of usable ones
        :return: True if they were added, False otherwise
        """
        new_credentials = self._get_api_instance()
        if not new_credentials:
            return False

        self.credentials[self.max_index] = new_credentials
        self.max_index += 1
        return True

    def _get_active_credentials(self) -> Optional[int]:
        """
        Get active credentials
        :return: index of credentials in self.credentials
        """
        tried_to_add_new = False
        while True:
            if not self.credentials:
                res = self._add_new_credentials()
                if not res:
                    return None

            active_credentials = None
            index = None
            for i, credentials in self.credentials.items():
                if credentials.get(ACTIVE_KEY, False):
                    active_credentials = credentials
                    index = i
                    break

            if not active_credentials:
                if not tried_to_add_new and len(self.credentials) < self.MAX_NUMBER_OF_CREDENTIALS:
                    tried_to_add_new = True
                    self._add_new_credentials()
                else:
                    sleep(SLEEP_TIME_BETWEEN_CHECK_TO_RELEASE_A_KEY)

                continue

            return index

    def after_request(self, index: int):
        """
        After each request make a key inactive and sleep to not reach rate limiting
        :param index: an index of the key
        :return: Nothing
        """
        try:
            key = self.credentials[index]
        except Exception as e:
            logger.exception(AGENT_UTILS_NAME, f'Index for a key is wrong. Error: {e}')
            return None

        last_request = key.get(LAST_REQUEST_KEY, None)
        time_between_requests = key.get(TIME_BETWEEN_REQUESTS_KEY, 0)

        if last_request and last_request + \
                timedelta(microseconds=time_between_requests) >= datetime.now():
            time_diff = last_request + timedelta(microseconds=time_between_requests) - datetime.now()
            sleep(time_diff.total_seconds())

        self.lock.acquire()
        try:
            key[ACTIVE_KEY] = True
        finally:
            self.lock.release()

    def call_function(self, method_name: str, *args, **kwargs):
        """
        A wrapper to get API instance and run a method inside it
        :param method_name: a method name to run
        :return: a result of method's execution
        """
        number_of_attemtps = 3
        while number_of_attemtps >= 0:
            number_of_attemtps -= 1

            index = self._get_active_credentials()
            if index is None:
                return None

            current_credentials = self.credentials[index]
            credentials_id = current_credentials[CREDENTIALS_ID_KEY]
            api = current_credentials[API_INSTANCE_KEY]

            try:
                func = getattr(api, method_name)
            except Exception as e:
                logger.exception(AGENT_UTILS_NAME, f'No method "{method_name}" in {self.name} API class. Error {e}')
                return None

            try:
                self.lock.acquire()
                try:
                    current_credentials[ACTIVE_KEY] = False
                finally:
                    self.lock.release()
                result = func(*args, **kwargs)
                current_credentials[LAST_REQUEST_KEY] = datetime.now()
                threading.Thread(target=lambda: self.after_request(index), daemon=True).start()

                return result
            except Exception as e:
                if 'Rate limit exceeded' in str(e):
                    self.db.limit_credentials_for_service_usage(credentials_id)
                    self.db.release_credentials_for_service(credentials_id)
                    self.credentials.pop(index)

                    logger.warning(AGENT_UTILS_NAME, f'Rate limit reached for {self.name} credentials')

        logger.exception(AGENT_UTILS_NAME, f'Failed to get data from {self.name}. Rate limit was'
                                           ' reached in all attempts')
        return None

    def release_credentials(self, call_from_atexit: bool = False):
        """
        Release API credentials
        :param call_from_atexit: the program is shutting down, we should release all credentials
        :return: Nothing
        """

        def release_credentials(key, api):
            already_being_removed = False
            if api[ACTIVE_KEY] is None:
                if not call_from_atexit:
                    return None
                already_being_removed = True

            while not api[ACTIVE_KEY]:
                api[ACTIVE_KEY] = None
                sleep(SLEEP_TIME_BETWEEN_CHECK_TO_RELEASE_A_KEY)

            self.lock.acquire()
            try:
                if not already_being_removed:
                    try:
                        self.credentials.pop(key)
                    except Exception as e:
                        # Error is likely because credentials were already removed
                        logger.warning(AGENT_UTILS_NAME, f'Failed to remove credentials. Error: {e}')

                    self.db.release_credentials_for_service(api[CREDENTIALS_ID_KEY])
            finally:
                self.lock.release()

        def release_in_parallel():
            execute_function_in_parallel(release_credentials, [(key, credentials,)
                                                               for key, credentials in self.credentials.items()])

        if not call_from_atexit:
            threading.Thread(target=release_in_parallel,
                             daemon=True).start()
        else:
            release_in_parallel()
