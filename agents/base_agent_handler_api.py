"""
Abstract class for Agent Handler API Implementation
"""
import atexit
import os
import threading
from http import HTTPStatus
from random import shuffle
from time import sleep
from typing import Dict, Optional

import flask
import requests
from werkzeug.datastructures import MultiDict

from agents.agents_utils.agents_helper import get_my_ip
from agents.agents_utils.utils_constants import IP_ADDRESS_KEY, AGENT_NUMBER_KEY, MESSAGE_KEY, NUMBER_OF_TASKS_KEY
from utils import logger
from utils.cloud_firestore_communication import Firestore, AGENT_HANDLER_MAX_TASKS_KEY
from utils.constants import MESSAGE_KEY


class AgentHandlerAPI:
    """
    Abstract API of agent handler instance
    """

    def __init__(self, name: str, app):
        """
        Initialise handler
        :param name: a name of the agent handler
        :param app: an instance of Flask app
        """
        atexit.register(self.delete_ip_address_from_db_on_exit)
        app.add_url_rule('/ping', view_func=self.ping_pong, methods=['GET'])
        app.add_url_rule('/addNewAgentInstance', view_func=self.add_new_agent_instance, methods=['POST'])
        app.before_request(self.before_request)
        app.after_request(self.after_request)

        self.app = app
        self.name = name
        self.agent_ips = {}  # ip -> number of tasks it is doing
        self.number_of_agents_in_db = 0

        self.lock = threading.Lock()
        self.chosen_port = None
        self.handler_id = None
        self.number_of_tasks = 0
        self.max_amount_of_tasks = 0
        self.list_of_util_paths = ['/ping', '/addNewAgentInstance']
        self.enable_feature_toggle = False

        try:
            agent_db_key = os.environ[f'{self.name.upper()}_AGENT_DB_KEY']
        except KeyError as e:
            logger.error(self.name, f'{self.name.upper()}_AGENT_DB_KEY is undefined. Error message: {e}')
            raise Exception

        self.db = Firestore(agent_db_key)

    def default_handler_to_transfer_request_to_agent(self) -> flask.Response:
        """
        If a request should be run one one instance only
        we can transfer it to one agent directly
        :return: flask.Response
        """
        # Merge data from firestore `features` collection with data from task
        data_form = MultiDict()
        data_form.update(flask.request.form)
        if self.enable_feature_toggle:
            feature_dict = self.db.get_agent_feature()
            data_form.update(feature_dict)
        response = self.send_request_to_agent(flask.request.method, flask.request.path, flask.request.args, data_form)

        if response:
            response_json = {}
            try:
                response_json = response.json()
            except Exception as e:
                logger.warning(self.name, f'It seems, there is no content in response {response}. Message: {e}')
            return flask.make_response(flask.jsonify(response_json), response.status_code)
        else:
            return flask.make_response(flask.jsonify({MESSAGE_KEY: 'Failed to get report from agents'}),
                                       HTTPStatus.INTERNAL_SERVER_ERROR)

    def before_request(self):
        """
        Check and update number of tasks before request
        :return: Nothing or response to the request
        """
        if flask.request.path in self.list_of_util_paths:
            return None

        self.lock.acquire()
        try:
            number_of_tasks = flask.request.args.get(NUMBER_OF_TASKS_KEY, type=int, default=0)
            self.number_of_tasks += 1
            self.db.change_number_of_tasks_in_agent_handler(self.handler_id, self.number_of_tasks)
            if self.number_of_tasks != number_of_tasks + 1:
                return flask.make_response(flask.jsonify({MESSAGE_KEY: 'Wrong number of tasks. Please sync with DB.'}),
                                           HTTPStatus.CONFLICT)
            if self.number_of_tasks >= self.max_amount_of_tasks:
                return flask.make_response(flask.jsonify({MESSAGE_KEY: 'Maximum number of tasks reached.'
                                                                       ' Please, wait or try with other handler.'}),
                                           HTTPStatus.BAD_REQUEST)
        finally:
            self.lock.release()

    def after_request(self, response):
        """
        Update a number of tasks after the job was done
        :return: Flask response
        """
        if flask.request.path in self.list_of_util_paths:
            return response

        self.lock.acquire()
        try:
            self.number_of_tasks -= 1
            self.db.change_number_of_tasks_in_agent_handler(self.handler_id, self.number_of_tasks)
        finally:
            self.lock.release()
        return response

    def periodically_update_number_of_tasks(self):
        """
        Periodically check if number of tasks is updated
        :return: Nothing
        """
        SLEEP_TIME = 30
        while True:
            self.db.change_number_of_tasks_in_agent_handler(self.handler_id, self.number_of_tasks)
            sleep(SLEEP_TIME)

    def send_request_to_agent(self, method: str, url: str, params: Dict = None,
                              data: Dict = None) -> Optional[requests.Response]:
        """
        Send a task to a free agent
        :param method: an http method to use
        :param url: an url of endpoint
        :param params: query params to transfer
        :param data: data to transfer
        :return: response or None
        """
        number_of_attempts = 3
        black_list_of_agents = {}
        response = None

        while number_of_attempts > 0:
            agent_ip = self.find_least_busy_agent(black_list_of_agents)
            if not agent_ip:
                break
            black_list_of_agents[agent_ip] = True
            self.lock.acquire()
            try:
                self.agent_ips[agent_ip] += 1
            finally:
                self.lock.release()

            try:
                agent_url = f'{agent_ip}{url}' if url.startswith('/') else f'{agent_ip}/{url}'
                response = requests.request(method=method, url=agent_url, params=params, data=data)
                response.raise_for_status()
                return response
            except Exception as e:
                logger.exception(self.name, f'Agent responded with an error {e}.', response)

            self.lock.acquire()
            try:
                self.agent_ips[agent_ip] -= 1
            finally:
                self.lock.release()

            number_of_attempts -= 1

        logger.exception(self.name, f'Amount of requests to agents from handler exceeded limit.')
        return None

    def find_least_busy_agent(self, black_list_of_agents: Dict[str, bool]) -> str:
        """
        Find an agent with the least amount of tasks
        :return: an ip address of the agent
        """
        self.lock.acquire()
        try:
            for ip, _ in sorted(self.agent_ips.items(), key=lambda x: x[1]):
                if ip not in black_list_of_agents:
                    return ip
        finally:
            self.lock.release()
        return ''

    def ping_agent_ip(self, ip: str) -> bool:
        """
        Pings an agent instance
        :param ip: an ip address of an agent with port for request
        :return: True if the request was successful, false otherwise
        """
        response = None
        try:
            response = requests.get(f'{ip}/ping')
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(self.name, f'Could not ping agent instance {ip}. Error {e}', response)
            return False
        return True

    def periodical_ping(self):
        """
        Ping all agent instances and remove those which are silent
        :return: None
        """
        SLEEP_TIME = 30
        while True:
            ips = self.agent_ips.copy()
            for agent_ip in ips:
                if not self.ping_agent_ip(agent_ip):
                    self.agent_ips.pop(agent_ip)
            sleep(SLEEP_TIME)

    def check_number_of_agents(self):
        """
        Periodically check current number of agents
        :return: Nothing
        """
        SLEEP_TIME = 5
        while True:
            sleep(SLEEP_TIME)
            current_len_of_agent_ips = len(self.agent_ips)
            if current_len_of_agent_ips != self.number_of_agents_in_db and self.handler_id:
                self.number_of_agents_in_db = current_len_of_agent_ips
                self.db.change_number_of_agents_in_agent_handler(self.handler_id, self.number_of_agents_in_db)

    def add_new_agent_instance(self) -> flask.Response:
        """
        Add an agent instance to be controlled by this handler
        :return: response
        """
        self.lock.acquire()
        try:
            ip = flask.request.args.get(IP_ADDRESS_KEY, type=str)
            agent_number = flask.request.args.get(AGENT_NUMBER_KEY, type=int)
            if agent_number != len(self.agent_ips):
                return flask.make_response(flask.jsonify({MESSAGE_KEY: 'Wrong number of agents. Please, sync with DB'
                                                                       ' and try again'}), HTTPStatus.CONFLICT)

            if self.ping_agent_ip(ip):
                if ip not in self.agent_ips:
                    self.agent_ips[ip] = 0
                else:
                    return flask.make_response(flask.jsonify({MESSAGE_KEY: 'Agent is already added'}),
                                               HTTPStatus.BAD_REQUEST)
            else:
                return flask.make_response(flask.jsonify({MESSAGE_KEY: 'The agent did not respond'}),
                                           HTTPStatus.BAD_REQUEST)
            return flask.make_response(flask.jsonify({MESSAGE_KEY: 'Agent added to the queue'}), HTTPStatus.OK)
        finally:
            self.lock.release()

    def ping_pong(self):
        """
        Answer ping request
        :return: response
        """
        return flask.make_response(flask.jsonify({MESSAGE_KEY: 'Pong'}), HTTPStatus.OK)

    def put_ip_address_in_db_on_start(self):
        """
        Send an ip address to db and delete it when server is finished
        :return: Nothing
        """
        TIME_TO_SLEEP_BETWEEN_PINGS = 1
        TIMEOUT_FOR_PING = 0.5
        while True:
            ip_address = get_my_ip()
            ip_with_port = f'http://{ip_address}:{self.chosen_port}'
            try:
                response = requests.get(f'{ip_with_port}/ping', timeout=TIMEOUT_FOR_PING)
                if response.status_code == HTTPStatus.OK:
                    break
            except:
                pass
            sleep(TIME_TO_SLEEP_BETWEEN_PINGS)

        self.handler_id, handler_info = self.db.add_new_agent_handler(ip_with_port)
        self.max_amount_of_tasks = handler_info.get(AGENT_HANDLER_MAX_TASKS_KEY, 0)

        threading.Thread(target=self.periodical_ping, daemon=True).start()
        threading.Thread(target=self.check_number_of_agents, daemon=True).start()
        threading.Thread(target=self.periodically_update_number_of_tasks,
                         daemon=True).start()

    def delete_ip_address_from_db_on_exit(self):
        """
        Delete an ip address from db when the server is stopped
        :return: Nothing
        """
        if self.handler_id:
            self.db.delete_agent_handler(self.handler_id)

    def start(self):
        """
        Start an agent handler api
        :return: Nothing
        """
        ports = self.db.get_available_agent_handler_ports()
        if not ports:
            ports = []
        shuffle(ports)  # Decrease a number of collisions when starting multiple servers
        threading.Thread(target=self.put_ip_address_in_db_on_start, daemon=True).start()
        for port in ports:
            try:
                self.chosen_port = port
                self.app.run(host='0.0.0.0', port=port, threaded=True)
                return
            except Exception as e:
                # Port is busy
                self.chosen_port = None

        if not self.chosen_port:
            logger.error(self.name, f'Could not start {self.name} agent handler on any port')
