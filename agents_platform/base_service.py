"""
Base class for agent_service
"""

import atexit
import datetime
import json
import re
import threading
import time
import urllib.parse
from abc import ABCMeta, abstractmethod
from configparser import ConfigParser, NoSectionError, NoOptionError
from http import HTTPStatus
from multiprocessing.pool import ThreadPool
from typing import Dict, List, Optional

import requests
import websocket
from firebase_admin import firestore

from agents_platform.constants import *
from agents_platform.own_adapter.agent import Agent
from agents_platform.own_adapter.agent_data import get_agent_data_by_user_id
from agents_platform.own_adapter.agent_task import get_agent_task_answers_by_id
from agents_platform.own_adapter.board import Board
from agents_platform.own_adapter.constants import ENGINE_NAME, PROTOCOL, STATUS, AGENTS_SERVICES_PATH, AdapterStatus
from agents_platform.own_adapter.element import Element
from agents_platform.own_adapter.platform_access import PlatformAccess
from utils import logger
from utils.cloud_firestore_communication import Firestore
from utils.constants import *
from utils.logger import debug, error, exception, info


class AgentService(metaclass=ABCMeta):
    """Base class for agent_service"""

    def __init__(self, config_path: str = 'settings.conf') -> None:
        # Config-based parameters
        try:
            self._agent_config = ConfigParser()
            self._agent_config.read(config_path)

            # Meta-data extraction
            self.name = self._agent_config.get(META_SECTION_KEY, 'name')
            self.redis_name = self._agent_config.get(META_SECTION_KEY, 'redis_name') or f'{self.name}_agent'
            self.description = self._agent_config.get(META_SECTION_KEY, 'description')
            self.status = self._agent_config.getint(META_SECTION_KEY, 'status')
            self.pool = ThreadPool(NUM_THREADS_PER_SERVICE)

            # Subscription data extraction
            currency = self._agent_config.get(SUBSCRIPTION_SECTION_KEY, CURRENCY_KEY)
            self.subscriptions = {
                SUBSCRIPTION_PLANS_KEY: [
                    {
                        SUBSCRIPTION_INTERVAL_KEY: DAY_KEY,
                        SUBSCRIPTION_INTERVAL_COUNT_KEY: self._agent_config.getint(SUBSCRIPTION_SECTION_KEY,
                                                                                   DAY_INTERVAL_KEY),
                        CAPACITY_KEY: DAY_CAPACITY_KEY,
                        PLAN_PRICINGS_KEY: [
                            # TODO: Somehow read it through loop
                            {
                                CURRENCY_KEY: currency,
                                SALARY_KEY: self._agent_config.getfloat(SUBSCRIPTION_SECTION_KEY, DAY_SALARY_KEY)
                            }
                        ]
                    },
                    {
                        SUBSCRIPTION_INTERVAL_KEY: WEEK_KEY,
                        SUBSCRIPTION_INTERVAL_COUNT_KEY: self._agent_config.getint(SUBSCRIPTION_SECTION_KEY,
                                                                                   WEEK_INTERVAL_KEY),
                        CAPACITY_KEY: self._agent_config.getint(SUBSCRIPTION_SECTION_KEY, WEEK_CAPACITY_KEY),
                        PLAN_PRICINGS_KEY: [
                            # TODO: Somehow read it through loop
                            {
                                CURRENCY_KEY: currency,
                                SALARY_KEY: self._agent_config.getfloat(SUBSCRIPTION_SECTION_KEY, WEEK_SALARY_KEY)
                            }
                        ]
                    },
                    {
                        SUBSCRIPTION_INTERVAL_KEY: MONTH_KEY,
                        SUBSCRIPTION_INTERVAL_COUNT_KEY: self._agent_config.getint(SUBSCRIPTION_SECTION_KEY,
                                                                                   MONTH_INTERVAL_KEY),
                        CAPACITY_KEY: self._agent_config.getint(SUBSCRIPTION_SECTION_KEY, MONTH_CAPACITY_KEY),
                        PLAN_PRICINGS_KEY: [
                            # TODO: Somehow read it through loop
                            {
                                CURRENCY_KEY: currency,
                                SALARY_KEY: self._agent_config.getfloat(SUBSCRIPTION_SECTION_KEY, MONTH_SALARY_KEY)
                            }
                        ]
                    },
                ]
            }

            # Service data extraction
            self.port = str(self._agent_config.get(SERVICE_SECTION_KEY, 'port'))
            self.elements_checker_period = self._agent_config.getfloat(SERVICE_SECTION_KEY, 'elements_checker_period')
            self.updating_time_interval = self._agent_config.getfloat(SERVICE_SECTION_KEY, 'updating_period')
            self.new_checker_period = self._agent_config.getfloat(SERVICE_SECTION_KEY, 'new_checker_period')

            # Content data (messages) extraction
            self.hello_message = self._agent_config.get(CONTENT_SECTION_KEY, 'hello_message').format(name=self.name)

            self.thread_names = {
                'service': f'{self.name}_service_thread',
                'websocket': f'{self.name}_websocket_thread',
                'updater': f'{self.name}_updater_thread'
            }

            self.platform_access = None
            self.agent_db_key = os.environ[f'{self.name.upper()}_AGENT_DB_KEY']
            self.db = Firestore(self.agent_db_key)
            self.task_running_listeners = {}
            self.task_running_updaters = {}
            self.running = True
            self.updater_thread_lock = threading.Lock()
            self.listener_thread_lock = threading.Lock()

            atexit.register(self.stop_running_tasks_on_exit)

            for task_file_name in self.get_agent_tasks_names():
                task_name = task_file_name.replace('.json', '')
                threading.Thread(target=lambda: self._start_periodical_updates(task_name,
                                                                               DEFAULT_PERIOD_TIME_FOR_UPDATES_CHECKER),
                                 daemon=True).start()

        except NoSectionError as no_section_err:
            error(ENGINE_NAME, f'Missing config section: {no_section_err}')
        except NoOptionError as no_option_err:
            error(ENGINE_NAME, f'Missing config option: {no_option_err}')
        except KeyError as key_error:
            error(ENGINE_NAME, f'Missing parameter in config. {key_error}')
        except Exception as excpt:
            error(ENGINE_NAME, f'Unexpectedly couldn\'t read config. {excpt}')
        else:
            debug(self.name, f'New agent-service [{self.name}] is registered')

        try:
            platform_access = self.__get_platform_access()
            self.agents_user_id = platform_access.get_user_id()
        except Exception as excpt:
            # TODO: Catch all the exceptions
            error(ENGINE_NAME, excpt)

    # Base service layer
    def _run_on_board(self, board: Board) -> None:
        """
        Runs the agent on the given board's elements
        :param board: Object: own_platform.board.Board on which the agent [should be / is] invited
        :return: Nothing
        """
        regexp = '@' + self.name + ':.+'
        elements = board.get_elements(regexp)
        for element in elements:
            # TODO: Threads, maybe?..
            self._run_on_element(element)

    @abstractmethod
    def identify_and_pass_task(self, element: Element, agent_task: Dict, update: bool = False,
                               doc_id: str = None) -> Optional[Element]:
        """
        Identify a task and pass it to appropriate method
        :param element: own_adapter.element.Element on which Company-agent should run
        :param agent_task: an agent task to get details from
        :param update: an element meant to be updated
        :param doc_id: optional id of a document in Firestore to send messages from Agent
        :return: Target element or None if task wasn't complete correctly
        """
        raise NotImplementedError

    def _run_on_element(self, element: Element, agent_task: Dict = None, update: bool = False,
                        doc_id: str = None) -> Optional[Element]:
        """
        Running on a target element...
        :param element: own_adapter.element.Element on which the agent should run...
        :param agent_task: an agent_task with answers for an agent to process
        :param update: if an element is being updated
        :param doc_id: optional id of a document in Firestore to send messages from Agent
        :return: Target element or None if board or board.element or task are not defined
        """
        if not element:
            logger.exception(self.name, 'Element was not provided')
            return None

        board = element.get_board()
        if not board:
            logger.exception(self.name, f'Board is undefined.')
            return None

        if agent_task:
            return self.identify_and_pass_task(element, agent_task, update)

        return None

    def communication_handling(self, doc_ref: firestore.firestore.DocumentReference):
        """
        Periodically check messages in Firestore and send them to OWN
        
        :param doc_ref: a reference to document containing messages
        :return: Nothing
        """
        doc_id = None
        try:
            doc_id = self.db.get_doc_id(doc_ref)
            self.task_running_listeners[doc_id] = doc_ref
            platform_access = self.__get_platform_access()
            content = self.db.get_doc_content(doc_ref)
            if not content:
                return
            board = Board(platform_access,
                          identifier=content[BOARD_IDENTIFIER_KEY])

            self.retrieve_and_upload_data(doc_ref, board)

        finally:
            if doc_id:
                self.db.finish_monitoring_task(doc_ref, listener=True)
                self.task_running_listeners.pop(doc_id)

    def retrieve_and_upload_data(self, doc_ref: firestore.firestore.DocumentReference,
                                 board: Board):
        """
        Implements communication functionality between agents and platform for constant monitoring tasks
        :param doc_ref: a reference to a document containing info about the task
        :param board: constant monitoring task's board
        :return: Nothing
        """
        self.retrieve_and_upload_messages_to_board(doc_ref, board)

    def retrieve_and_upload_messages_to_board(self, doc_ref: firestore.firestore.DocumentReference,
                                              board: Board):
        """
        Method for upload messages on a board
        :param doc_ref: a reference to a document containing info about the task
        :param board: constant monitoring task's board
        :return: Nothing
        """

        content = self.db.get_doc_content(doc_ref)
        if not content:
            return

        last_message_read = content[LAST_MESSAGE_READ_KEY]
        messages = content[MESSAGES_KEY]
        last_index = max(last_message_read, messages[-1][INDEX_KEY] if messages else 0)
        new_messages = list(filter(lambda message: message[INDEX_KEY] > last_index, messages))

        self.db.update_document(doc_ref, {
            LAST_MESSAGE_READ_KEY: last_index,
            MESSAGES_KEY: new_messages,
        })
        for message in messages:
            if message[INDEX_KEY] <= last_index:
                board.put_message(message[MESSAGE_KEY])

    def stop_running_tasks_on_exit(self):
        """
        Update values in DB for monitoring tasks before exiting
        :return: Nothing
        """
        self.running = False
        with self.listener_thread_lock:
            for doc in self.task_running_listeners.copy().values():
                self.db.finish_monitoring_task(doc_ref=doc, listener=True)
        with self.updater_thread_lock:
            for doc in self.task_running_updaters.copy().values():
                self.db.finish_monitoring_task(doc_ref=doc, update=True)

    def _run_on_element_default(self, element: Element, query_id: str = '', agent_task: Optional[Dict] = None,
                                update: bool = False, constant_monitoring: bool = False) -> Optional[Element]:
        """
        Run on element and save task to db
        
        :param query_id: an id of agent task query
        :param update: if an element is being updated
        :param element: own_adapter.element.Element on which the agent should run
        :param agent_task: an agent_task with answers for an agent to process
        :param constant_monitoring: whether this task should run in constant monitoring mode
        :return: Target element
        """
        task_name = self.identify_task(agent_task)
        return self._run_on_element_and_save_task(element, query_id=query_id, task_name=task_name,
                                                  agent_task=agent_task, update=update,
                                                  constant_monitoring=constant_monitoring)

    def _run_on_element_and_save_task(self, element: Element, task_name: str, query_id: str,
                                      agent_task: Dict = None, start_listener: bool = False,
                                      update: bool = False, constant_monitoring: bool = False) \
            -> Optional[Element]:
        """
        Create document to communicate with agent, run on a target element
        
        :param query_id: an id of agent task query
        :param task_name: a name of task which is being executed
        :param update: if an element is being updated
        :param element: own_adapter.element.Element on which the agent should run
        :param agent_task: an agent_task with answers for an agent to process
        :param constant_monitoring: whether this task should run in constant monitoring mode
        :param start_listener: if a communication listener should be started for this task
        :return: Target element
        """
        self.db.delete_old_agent_tasks(element.get_id())
        doc_ref = self.db.create_new_doc_for_task(element.get_board().get_id(), element.get_id(), query_id, task_name,
                                                  update_period=self.updating_time_interval,
                                                  constant_monitoring=constant_monitoring, agent_task=agent_task)
        doc_id = self.db.get_doc_id(doc_ref)
        try:
            self.task_running_updaters[doc_id] = doc_ref
            if start_listener or constant_monitoring:
                threading.Thread(target=lambda: self.communication_handling(doc_ref),
                                 daemon=True).start()
            res = self._run_on_element(element, agent_task, update, doc_id)
            if not res:
                self.db.delete_doc(doc_ref)
            return res
        except Exception as e:
            logger.exception(self.name, f'Couldn\'t run updates on element for task: {task_name}. Error: {e}')
        finally:
            self.db.finish_monitoring_task(doc_ref, update=True)
            self.task_running_updaters.pop(doc_id)

    def _run_update_for_task(self, doc_ref: firestore.firestore.DocumentReference, task_name: str) \
            -> Optional[Element]:
        """
        Run a periodical update for agent task stored in Firestore
        :param doc_ref: a reference to Firestore document with info about the task
        :param task_name: a name of the task
        :return: Nothing
        """
        doc_id = None
        try:
            task_content = self.db.get_doc_content(doc_ref)
            platform_access = self.__get_platform_access()
            board = Board(platform_access, identifier=task_content[BOARD_IDENTIFIER_KEY])
            element = Element(platform_access, identifier=task_content[ELEMENT_ID_KEY], board=board)
            agent_task = task_content[AGENT_TASK_KEY]
            doc_id = self.db.get_doc_id(doc_ref)
            self.task_running_updaters[doc_id] = doc_ref
        except Exception as e:
            logger.exception(self.name, f'Could not perform periodical update for task {task_name}. Error: {e}')
            return None
        else:
            self._run_on_element(element=element, agent_task=agent_task, update=True, doc_id=doc_id)
        finally:
            self.db.finish_monitoring_task(doc_ref, update=True)
            if doc_id:
                self.task_running_updaters.pop(doc_id)

    # Web-sockets
    def on_websocket_message(self, ws: websocket.WebSocketApp, message: str) -> None:
        """Processes websocket messages"""
        message_dict = json.loads(message)
        content_type = message_dict['contentType']
        message_type = content_type.replace('application/vnd.uberblik.', '')
        debug(self.name, message)

        if message_type == 'liveUpdateAgentTaskElementAnswersSaved+json':
            # Get the data from the LiveUpdate's message
            agent_data_id = int(message_dict['agentDataId'])
            agent_task_id = int(message_dict['agentTaskId'])
            element_id = int(message_dict['elementId'])
            board_id = int(message_dict['boardId'])
            query_id = str(message_dict['agentQueryId'])

            agent = self.get_agent()
            agent_task = get_agent_task_answers_by_id(agent.get_platform_access(),
                                                      agent_data_id=agent_data_id,
                                                      agent_task_id=agent_task_id,
                                                      board_id=board_id,
                                                      element_id=element_id)

            board = Board.get_board_by_id(board_id,
                                          agent.get_platform_access(),
                                          need_name=False)

            element = Element.get_element_by_id(element_id,
                                                agent.get_platform_access(),
                                                board)

            if element:
                # Run AgentTask on the element
                updated_element = self._run_on_element_default(element, query_id, agent_task)
                if updated_element:
                    element = updated_element
                element.set_last_processing_time(datetime.datetime.now())
                agent.cache_element_to_redis(element)

        elif message_type in ['liveUpdateElementPermanentlyDeleted+json', 'liveUpdateElementDeleted+json']:
            element_id = f'/{"/".join(message_dict["path"].split("/")[-4:])}'
            self.db.delete_old_agent_tasks(element_id)

        elif message_type == 'liveUpdateAgentTaskElementDeleted+json':
            # Get the data from the LiveUpdate's message
            element_id = int(message_dict['elementId'])
            board_id = int(message_dict['boardId'])

            full_element_id = f'/boards/{board_id}/elements/{element_id}'
            self.db.delete_old_agent_tasks(full_element_id)

        elif message_type == 'liveUpdateBoardDeleted+json':
            board_id = int(message_dict['path'].split('/')[-1])
            self.db.delete_old_agent_tasks('', board_id)

    def identify_task(self, agent_task: Optional[Dict] = None, agent_task_id: Optional[int] = None) -> str:
        """
        Identify a task
        :param agent_task_id: an id of the agent task
        :param agent_task: an agent task to get details from
        :return: a name of the task
        """
        if agent_task_id:
            agent_task_config_id = agent_task_id
        else:
            if not agent_task:
                return ''

            agent_task_answers = agent_task['agentTaskElement']['agentTask']
            agent_task_config_id = agent_task_answers['id']

        # Get all the agent-tasks
        possible_files = self.get_agent_tasks_names()

        # Find the AgentTask to run
        for filename in possible_files:
            if self.get_agent_task_config_from_file(filename)['agentTask'].get('id', None) == agent_task_config_id:
                return filename.replace('.json', '')

        return ''

    def on_websocket_error(self, ws, err):
        """Logs websocket errors"""
        error(self.name, err)

    def on_websocket_open(self, ws):
        """Logs websocket openings"""
        info(self.name, f'{self.redis_name}\'s websocket is open')

    def on_websocket_close(self, ws):
        """Logs websocket closings"""
        info(self.name, f'{self.redis_name}\'s Websocket is closed')

    def open_websocket(self):
        """Opens a websocket to receive messages from the boards about events"""
        agent = self.get_agent()
        query = {}

        # getting the service url without protocol name
        platform_url_no_protocol = agent.get_platform_access().get_platform_url().split('://')[1]
        query['token'] = agent.get_platform_access().get_access_token()
        url = f'{PROTOCOL}://{platform_url_no_protocol}/opensocket?{urllib.parse.urlencode(query)}'
        ws = websocket.WebSocketApp(url,
                                    on_message=lambda *args: self.pool.starmap_async(self.on_websocket_message, [args]),
                                    on_error=self.on_websocket_error,
                                    on_open=self.on_websocket_open,
                                    on_close=self.on_websocket_close)
        ws.run_forever()

    def run(self) -> None:
        """
        Runs the agent by starting websocket and updater threads
        :return: Nothing
        """
        if self.status == STATUS['INACTIVE']:
            info(self.name, f'The {self.name}-agent is inactive.')
            return

        websocket_thread = None
        # TODO: Add multi-threaded lock/stop here
        while True:
            # opening a websocket for catching server messages
            if websocket_thread is None or not websocket_thread.is_alive():
                try:
                    websocket_thread = threading.Thread(target=self.open_websocket,
                                                        name=self.thread_names['websocket'],
                                                        args={}, daemon=True)
                    websocket_thread.start()
                    debug(self.name, f'{self.name} started websocket')
                except Exception as excpt:
                    exception(self.name,
                              f'Could not open a websocket. Exception message: {str(excpt)}')

            # wait until next check
            time.sleep(10)

    # Util
    def get_agent(self) -> [Agent, None]:
        """
        Returns the current agent
        :return: Object: Instance of own_platform.agent.Agent,
                         or None with incorrect authentication data
        """
        platform_access = self.__get_platform_access()
        agent = Agent(platform_access, self.redis_name)

        return agent

    def __get_platform_access(self) -> [PlatformAccess, None]:
        """Returns PlatformAccess with valid agent's credentials (environ), None otherwise"""
        if not self.platform_access:
            try:
                login = os.environ[f'OWN_{self.name.upper()}_AGENT_LOGIN']
                password = os.environ[f'OWN_{self.name.upper()}_AGENT_PASSWORD']
                self.platform_access = PlatformAccess(login, password)
            except KeyError as key_error:
                exception(self.name,
                          f'Failed get credentials for {self.name}-agent. Error message: {str(key_error)}')
            except Exception as err:
                error(self.name, f'Some error occurred while establishing connection to the platform: {err}')

        return self.platform_access

    def get_service_id(self) -> int:
        """Returns ID of the agent-service"""
        response = get_agent_data_by_user_id(self.__get_platform_access(), self.agents_user_id)
        resp_content = json.loads(response.content.decode())
        result = int(resp_content['agentData']['_links'][0]['href'].split('/')[-1])
        return result

    def get_agent_task_config_from_file(self, file_name: str) -> Dict:
        """
        Return an agent task config stored in a file
        :param file_name: a name of the file relative to agent tasks folder
        :return: the agent task config
        """

        file_location = os.path.join(AGENTS_SERVICES_PATH, f'{self.name}_service', 'agent_tasks', file_name)
        try:
            with open(file_location, 'r') as file:
                agent_task_config = json.load(file)
        except Exception as e:
            error(self.name, f'Agent task config in {file_name} not found. Exception {e}.')
            raise

        return agent_task_config

    def update_element_caption(self, element: Element, update_with_data: str) -> None:
        """
        Sets the new caption for the element
        "<agent_name>: <new_data>[, <old_query>]"
        :param element: Element to update the caption on
        :param update_with_data: the data (sentence, or a keyword) to update the element with.
        :return: Nothing
        """
        # Save the old caption
        old_caption = element.get_name()

        # Form the new caption
        new_caption = f'{self.name}: {update_with_data}'

        # Do nothing if they are the same
        if old_caption == new_caption:
            return

        # Check if the old caption matches the pattern
        pattern = re.compile(f'{self.name}: [^\n\r]+')
        if pattern.match(old_caption):
            # If it is, extract the query itself, leaving the sender
            old_caption_queries = old_caption.replace(f'{self.name}: ', '')

            # Check if last query wasn't the same (i.e., it's not a periodical update
            last_old_query = old_caption_queries.split(', ')[0]
            if last_old_query != update_with_data:
                new_caption += f', {old_caption_queries}'

        element.set_name(new_caption)

    def get_agent_tasks_names(self) -> List[str]:
        """Returns AgentTasks' names in the agent-service agent_task directory"""
        # Form the agent_tasks absolute path
        this_service_tasks_path = os.path.join(AGENTS_SERVICES_PATH, f'{self.name}_service', 'agent_tasks')
        if not os.path.exists(this_service_tasks_path):
            return []

        # Get all the filenames that are .json
        possible_files = [file for file in os.listdir(this_service_tasks_path) if file.endswith('.json')]

        # TODO: Check if they are really AgentTasks
        return possible_files

    def send_request_to_agent_handler(self, method: str, url: str, params: Dict = None, data: Dict = None) \
            -> Optional[requests.Response]:
        """
        Send a task to a free agent handler
        :param method: an http method to use
        :param url: An URL of endpoint
        Example: for http://localhost:5000/handler, 'url' will be 'handler'
        Example: for http://localhost:5000/, 'url' will be an empty string ('')
        :param params: query params to transfer
        :param data: data to transfer
        :return: response
        """
        MAX_NUMBER_OF_ATTEMPTS = 5
        number_of_attempts = 0
        black_list_of_agent_handlers = set()
        response = None
        SLEEP_TIME = 2

        while number_of_attempts <= MAX_NUMBER_OF_ATTEMPTS:
            handler = self.db.get_agent_handler_with_least_amount_of_tasks(list(black_list_of_agent_handlers))
            if not handler:
                break

            handler_id, handler_info = handler
            handler_ip = handler_info.get(AGENT_HANDLER_ADDRESS_KEY, None)
            if not handler_ip:
                continue

            black_list_of_agent_handlers.add(handler_id)
            num_of_tasks_in_handler = handler_info.get(AGENT_HANDLER_NUM_TASKS_KEY, 0)
            if not params:
                params = {}
            params[NUMBER_OF_TASKS_KEY] = num_of_tasks_in_handler

            try:
                response = requests.request(method=method, url=f'{handler_ip}/{url}', params=params, data=data)
                if response.status_code == HTTPStatus.CONFLICT:
                    black_list_of_agent_handlers.remove(handler_id)

                response.raise_for_status()
                return response
            except requests.ConnectionError as e:
                self.db.increase_handler_number_of_fails(handler_id)
                logger.exception(self.name, f'Agent handler is not reachable. Error {e}.', response)
            except requests.RequestException as e:
                logger.exception(self.name, f'Agent handler responded with an error {e}.', response)

            number_of_attempts += 1
            time.sleep(SLEEP_TIME * (number_of_attempts ** 2))

        logger.exception(self.name, f'Amount of requests to agents from handler exceeded limit.')
        return response

    def _start_listeners(self, task_name: str, period_time: float):
        """
        Check constant tasks in Firestore and start listeners for them
        
        :param task_name: a name of task which is being executed
        :param period_time: amount of seconds to wait between checks
        :return: Nothing
        """
        SLEEP_TIME = 1
        MAX_NUMBER_OF_TASKS_FOR_ONE_PERIOD = 10
        docs = {}

        while True:
            for i in range(MAX_NUMBER_OF_TASKS_FOR_ONE_PERIOD):
                with self.listener_thread_lock:
                    if not self.running:
                        return
                    doc = self.db.get_agent_task_from_firestore(task_name, runners_dict=self.task_running_listeners,
                                                                listener=True, constant_monitoring=True)
                if not doc:
                    break
                docs[self.db.get_doc_id(doc)] = doc

                time.sleep(SLEEP_TIME)

            for doc_id, doc in docs.copy().items():
                docs.pop(doc_id)
                threading.Thread(target=lambda: self.communication_handling(doc), daemon=True).start()

            time.sleep(period_time)

    def _start_periodical_updates(self, task_name: str, period_time: float):
        """
        Check if there are tasks in Firestore that should be updated

        :param task_name: a name of a task to check
        :param period_time: amount of seconds to wait between checks
        :return: Nothing
        """
        while True:
            with self.updater_thread_lock:
                if not self.running:
                    return
                doc = self.db.get_agent_task_from_firestore(task_name, runners_dict=self.task_running_updaters,
                                                            constant_monitoring=False, update=True)
            if doc:
                threading.Thread(target=lambda: self._run_update_for_task(doc, task_name),
                                 daemon=True).start()
            time.sleep(period_time)

    def get_file_from_agent_and_send_to_element(self, file_url: str, filename: str, element: Element) -> bool:
        """
        Downloads a file from agent and uploads it to an element
        :param file_url: a url of the file
        :param filename: a name of the file to display in the element
        :param element: the element where file should be placed
        :return: True if files was uploaded, False otherwise
        """
        if not (file_url and filename and element):
            return False
        try:
            file_bytes = requests.get(file_url).content
        except Exception as e:
            logger.error(self.name, f'Agent can\'t download file by url {file_url}. Error {e}')
            return False

        returned_code = element.put_file(filename, file_bytes)
        if returned_code not in [HTTPStatus.CREATED, AdapterStatus.CONNECTION_ABORTED]:
            logger.error(self.name, f'Agent can\'t upload file to element {element.get_id()}.')
            return False
        else:
            return True
