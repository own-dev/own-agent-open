"""
Abstract class for Agent API Implementation
"""
import threading
from random import shuffle, randint
from time import sleep

import atexit
import flask
import requests
from flask import send_from_directory, after_this_request, safe_join
from google.cloud.firestore_v1beta1 import DocumentReference
from werkzeug.exceptions import NotFound

from agents.agents_utils.agents_helper import get_my_ip, create_downloads_dir_if_not_exist
from agents.agents_utils.utils_constants import *
from utils import logger
from utils.cloud_firestore_communication import Firestore, AGENT_HANDLER_ADDRESS_KEY, \
    AGENT_HANDLER_NUM_AGENTS_KEY
from utils.constants import MESSAGE_KEY


class AgentAPI:
    """
    Abstract API of agent instance
    """

    def __init__(self, name: str, app):
        """
        Initialise handler
        :param name: a name of the agent
        :param app: an instance of Flask app
        """
        app.add_url_rule('/ping', view_func=self.ping_pong, methods=['GET'])

        app.add_url_rule(f'/{DOWNLOADS_DIR}/<path:path>', view_func=self.send_static_files)

        create_downloads_dir_if_not_exist()
        self.app = app
        self.name = name
        self.chosen_port = None
        self.lock = threading.Lock()
        self.handler_ip_address = None
        self.none = None
        self.workers = {}
        self.running = True
        self.worker_lock = threading.Lock()
        atexit.register(self.stop_running_workers_on_exit)

        try:
            self.agent_db_key = os.environ[f'{self.name.upper()}_AGENT_DB_KEY']
        except KeyError as e:
            logger.error(self.name, f'{self.name.upper()}_AGENT_DB_KEY is undefined. Error message: {e}')
            raise Exception(f'{self.name.upper()}_AGENT_DB_KEY is undefined')

        self.db = Firestore(self.agent_db_key)

    def ping_agent_ip(self, ip: str) -> bool:
        """
        Pings an agent instance
        :param ip: an ip address of an agent with port for request
        :return: If the request was successful
        """
        response = None
        try:
            response = requests.get(f'{ip}/ping')
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(self.name, f'Could not ping agent instance {ip}. Error {e}', response)
            return False
        return True

    def ping_pong(self):
        """
        Answers ping request
        :return: None
        """
        return flask.make_response(flask.jsonify({MESSAGE_KEY: 'Pong'}), SUCCESS_CODE)

    def find_agent_handler(self):
        """
        Find an agent handler to handle this instance
        :return: Nothing
        """
        TIME_TO_SLEEP_BETWEEN_PINGS = 1
        TIMEOUT_FOR_PING = 0.5
        RANDOM_SLEEP_RANGE_TO_REQUEST_AGENT_HANDLER = 0, 10

        while True:
            try:
                response = requests.get(f'http://localhost:{self.chosen_port}/ping', timeout=TIMEOUT_FOR_PING)

                if response.status_code == SUCCESS_CODE:
                    break
            except Exception as e:
                pass
            sleep(TIME_TO_SLEEP_BETWEEN_PINGS)

        while True:
            sleep(randint(*RANDOM_SLEEP_RANGE_TO_REQUEST_AGENT_HANDLER))
            handler = self.db.get_least_busy_agent_handler()

            if not handler:
                continue
            handler_id, agent_hanlder = handler
            ip_address = agent_hanlder[AGENT_HANDLER_ADDRESS_KEY]
            agent_number = agent_hanlder[AGENT_HANDLER_NUM_AGENTS_KEY]
            try:
                my_ip_address = get_my_ip()
                my_ip_with_port = f'http://{my_ip_address}:{self.chosen_port}'
                response = requests.post(f'{ip_address}/addNewAgentInstance?{AGENT_NUMBER_KEY}={agent_number}&'
                                         f'{IP_ADDRESS_KEY}={my_ip_with_port}')
                if response.status_code == SUCCESS_CODE:
                    self.handler_ip_address = ip_address
                    self.handler_id = handler_id
                    break
            except requests.ConnectionError:
                logger.exception(self.name, f'Agent handler {ip_address} is not responding.')
                self.db.increase_handler_number_of_fails(handler_id)
            except Exception as e:
                logger.info(self.name, f'Agent handler {ip_address} response to agent is {e}', response)

    def periodical_ping(self):
        """
        Ping an agent handler
        :return: None
        """
        SLEEP_TIME = 30
        while True:
            sleep(SLEEP_TIME)
            if not self.handler_ip_address:
                continue

            response = None
            try:
                response = requests.get(f'{self.handler_ip_address}/ping')
                response.raise_for_status()
            except requests.RequestException as e:
                logger.warning(self.name, f'Could not ping agent instance {self.handler_ip_address}.'
                                          f' Error {e}', response)

                self.db.increase_handler_number_of_fails(self.handler_id)
                self.find_agent_handler()

    def start(self):
        """
        Start an agent handler API
        :return: Nothing
        """
        chosen_port = None
        ports = self.db.get_available_agent_ports()
        if not ports:
            ports = []
        shuffle(ports)  # Decrease a number of collisions when starting multiple servers
        threading.Thread(target=self.find_agent_handler, daemon=True).start()
        threading.Thread(target=self.periodical_ping, daemon=True).start()
        for port in ports:
            try:
                self.chosen_port = port
                self.app.run(host='0.0.0.0', port=port, threaded=True)
                return
            except Exception as e:
                # Port is busy
                self.chosen_port = None

        if not chosen_port:
            logger.error(self.name, f'No port to start {self.name} agent')

    def constant_task_handler(self, task_name: str, doc_ref: DocumentReference):
        """
        Handle a constantly running task
        :param task_name: a name of the task
        :param doc_ref: a reference of a document containing info about the task
        :return: Nothing
        """
        raise NotImplementedError

    def start_workers(self, task_name: str, period_time: int = 150):
        """
        Check constant tasks in Firestore and start workers for them
        
        :param period_time: how many seconds to wait before checking for task
        :param task_name: a name of a task to start
        :return: Nothing
        """

        while True:
            with self.worker_lock:
                if not self.running:
                    return
                doc = self.db.get_agent_task_from_firestore(task_name, runners_dict=self.workers, worker=True)
            if doc:
                threading.Thread(target=lambda: self.constant_task_handler(task_name, doc),
                                 daemon=True).start()
            sleep(period_time)

    def stop_running_workers_on_exit(self):
        """
        Update values in DB for tasks being process by workers before exiting

        :return: Nothing
        """
        self.running = False
        with self.worker_lock:
            for doc in self.workers.copy().values():
                self.db.finish_monitoring_task(doc, worker=True)

    @staticmethod
    def send_static_files(path):
        """
        Serve static files generated by agent
        :return: a file
        """

        @after_this_request
        def remove_file(response):
            try:
                os.remove(safe_join(AGENTS_PATH, DOWNLOADS_DIR, path))
            except NotFound as e:
                return flask.make_response(
                    flask.jsonify({MESSAGE_KEY: 'The requested URL was not found on the server'}),
                    HTTPStatus.NOT_FOUND)
            return response

        return send_from_directory(os.path.join(AGENTS_PATH, DOWNLOADS_DIR), path)
