"""
Basic functionality to work with an Agent

Be ware of this is not a replication! I.e., there is no Agent class on a back-end
"""

import json
from typing import Dict, List, Optional, Union

import redis
from requests import HTTPError

from agents_platform.own_adapter.board import Board
from agents_platform.own_adapter.constants import OWN_ADAPTER_NAME
from agents_platform.own_adapter.element import Element
from agents_platform.own_adapter.platform_access import PlatformAccess
from agents_platform.redis_handler import get_redis_connection
from agents_platform.util.networking import make_request
from utils import logger


class Agent:
    """
    Allows to work with Redis' cache on agents' elements
    """
    def __init__(self, platform_access: PlatformAccess, redis_name: str = ''):
        self.__platform_access = platform_access
        self.__redis_name = redis_name

    def get_platform_access(self) -> PlatformAccess:
        """Returns agent's PlatformAccess"""
        return self.__platform_access

    def get_redis_name(self) -> str:
        """Returns agent's name in Redis"""
        return self.__redis_name

    def get_boards(self) -> Optional[List[Board]]:
        """
        Returns all the boards agent is invited to
        :return: This agent's boards,
                 or None if there was a network or an auth. error
        """
        http_method = 'GET'
        detail = 'boards'
        values = {}
        url_postfix = 'boards'
        response = None
        try:
            response = make_request(platform_access=self.__platform_access,
                                    http_method=http_method,
                                    url_postfix=url_postfix,
                                    detail=detail,
                                    values=values)
            response.raise_for_status()
            response_data = response.json()
            boards = self.__create_boards_from_dict(response_data)
            return boards
        except HTTPError as http_error:
            logger.exception(OWN_ADAPTER_NAME, f'Could not retrieve boards data: {http_error}',
                             response)
            return None
        except ConnectionError as conect_error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Could not get boards list. Exception message: {conect_error}',
                             response)
            return None

    @staticmethod
    def get_agent_tasks_by_id(platform_access: PlatformAccess,
                              agent_data_id: int) -> Optional[List[Dict]]:
        """
        Returns all the agent's AgentTasks by the given AgentDataID
        API-referenece: https://own1.docs.apiary.io/#reference/agent-tasks/agentdataagentdataidagenttasks/get

        :param platform_access: PlatformAccess of a user which has access to the agent
                                (or of an agent itself)
        :param agent_data_id: AgentData's ID to get AgentTasks from

        :return: AgentTasks that are assigned to the agent
        """
        # Get all the forms
        response = make_request(platform_access=platform_access,
                                http_method='GET',
                                url_postfix=f'agentdata/{agent_data_id}/agenttasks',
                                detail='agentTask',
                                data=None, values={})
        if not response:
            return None

        data: Dict = json.loads(response.text)
        tasks: str = data.get('agentTasks', None)
        return json.loads(tasks) if tasks else None

    def __create_boards_from_dict(self, data: Dict) -> Optional[List[Board]]:
        """
        Composes the boards out of the given data

        :param data: {'boards': [..]}
        where [..] = list of dictionaries with mandatory data as follows:
        {
            'rel': board's name,
            'href': board's URL (with its ID)
        }

        :return: List of Board objects for the given data
                 if there is 'boards' key in the given data, and its value isn't empty,
                 otherwise None
        """
        boards_data = data.get('boards', None)
        if not boards_data:
            return None

        boards = []
        for board in boards_data:
            href = board.get('href', '')
            identifier = href.split('/')[-1] if href else None
            name = board.get('rel', None)

            boards.append(Board(self.__platform_access, name=name, identifier=identifier))
        return boards

    def __get_new_boards(self, boards: List[Board]) -> List[Board]:
        """
        Filters all the agent's boards with new ones, updating Redis

        :param boards: Known agent's boards (some could not be cached in Redis yet)

        :return: "given boards" - "existing in Redis boards" = "new boards"
        """
        unique_board_ids = {[board.get_id() for board in boards]}

        # getting boards from Redis
        # the set in Redis is called something like 'news_agent:boards'
        # if there is no such element, or it is empty, it returns just an empty set, not None
        connection = get_redis_connection()
        redis_board_ids = connection.smembers(f'{self.__redis_name}:boards')

        # new boards ids
        new_board_ids = unique_board_ids - redis_board_ids

        # update Redis
        for board_url in new_board_ids:
            connection.sadd(f'{self.__redis_name}:boards', board_url)

        # filter new boards
        new_boards = [board for board in boards if board.get_id() in new_board_ids]

        return new_boards

    def get_elements(self, regexp: str = '') -> List[Element]:
        """
        Returns all the elements agent possesses that exist and are cached

        :param regexp: If given, filters elements' names with regular expression

        :return: Elements that exist and are cached
        """
        elements = []
        for board in self.get_boards():
            elements.extend(board.get_elements(regexp))
        # removing template elements
        # FIXME: Is it still relevant?..
        agent_name = self.get_redis_name().replace('_agent', '')
        elements = [element for element in elements
                    if element.get_name() != f'@{agent_name}: place company name(s) here']

        # getting elements from Redis
        # the set in Redis is called something like 'news_agent:elements:{element_id}'
        # if there is no such element, or it is empty, it returns just an empty set, not None
        connection = get_redis_connection()
        redis_elements = self.__get_cached_elements(elements, connection)

        # new and updated elements
        existing_and_cached_elements = []
        for element in elements:
            if element.get_id() in redis_elements.keys():
                redis_elem_name = redis_elements[element.get_id()].get_name()
                if element.get_agent_task_id() \
                        or element.get_name() == redis_elem_name:
                    last_proc_time = redis_elements[element.get_id()].get_last_processing_time()
                    element.set_last_processing_time(last_proc_time)
                    existing_and_cached_elements.append(element)

        return existing_and_cached_elements

    def cache_element_to_redis(self, element: Element) -> None:
        """
        Caches an element to Redis

        :param element: Element to be cached

        :return: Nothing
        """
        connection = get_redis_connection()
        connection.hmset(f'{self.__redis_name}:elements:{element.get_id()}', element.to_dictionary())

    def remove_element_from_redis(self, element: Union[Element, str]) -> None:
        """
        Removes a cached element from Redis

        :param element: Either element's ID or element itself to remove it from Reidis' cache

        :return: Nothing
        """
        if isinstance(element, Element):
            element_id = element.get_id()
        elif isinstance(element, str):
            element_id = element
        else:
            return

        connection = get_redis_connection()
        connection.delete(f'{self.__redis_name}:elements:{element_id}')

    def __get_cached_elements(self, elements: List[Element],
                              connection: Optional[redis.StrictRedis] = None) -> Dict[str, Element]:
        """
        Returns cached elements from the given ones

        :param elements: Filters the given elements with those that are already cached
        :param connection: Redis connection (like `get_redis_connection()`)
                            -- a new one will be created in case of None

        :return: Element ID - Element mapping (dict)
        """
        if connection is None:
            connection = get_redis_connection()

        redis_elements = {}
        for element in elements:
            element_dict = connection.hgetall(f'{self.__redis_name}:elements:{element.get_id()}')
            if element_dict:
                redis_element = Element.from_dictionary(self.__platform_access, element_dict)
                redis_elements[redis_element.get_id()] = redis_element
        return redis_elements

    def __remove_old_elements_from_redis(self, elements: List[Element],
                                         redis_elements: Dict) -> None:
        """
        Compares actual and cached elements and removes the irrelevant ones

        :param elements: Elements to remove from Redis' cache
        :param redis_elements: Existing Redis' elements

        :return: Nothing
        """
        connection = get_redis_connection()
        element_ids = [element.get_id() for element in elements]

        for redis_element_id in redis_elements.keys():
            if redis_element_id not in element_ids:
                connection.delete(f'{self.__redis_name}:elements:{redis_element_id}')
