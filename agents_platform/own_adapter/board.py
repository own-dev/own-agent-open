"""
Interaction with OWN Platform's Board
Board class is only partially replicated
"""

import json
import re
from typing import List, Dict, Union, Optional
from http import HTTPStatus
from requests import ConnectionError, HTTPError

from requests import request

from agents_platform.own_adapter.constants import OWN_ADAPTER_NAME, PREFIX
from agents_platform.own_adapter.element import Element
from agents_platform.own_adapter.platform_access import PlatformAccess
from agents_platform.util.networking import compose_path
from utils import logger


class Board:
    """
    OWN's Board replication
    """
    def __init__(self, platform_access: PlatformAccess,
                 name: str = '', identifier: str = ''):
        """
        :param platform_access: PlatformAccess-object a(n) user/agent of that is on the board?..
        :param name: Board's name
        :param identifier: Board's ID on the platform
        """
        self.__platform_access = platform_access
        self.__name = name
        self.__url = compose_path(self.__platform_access.get_platform_url(), 'boards', identifier)
        self.__id = identifier

    def get_name(self) -> str:
        """Returns board's name if it was given in the constructor"""
        return self.__name

    def get_url(self) -> str:
        """Returns URL to the board"""
        return self.__url

    def get_id(self) -> str:
        """Returns board's ID"""
        return self.__id

    def get_elements(self, regexp: str = '') -> List[Element]:
        """
        Returns all the board's elements
        If regexp is given will return only matched ones?..

        :param regexp: Elements caption-filter regular expression

        :return: A list of parsed board's elements (filtered by regexp for caption if given)
        """
        response_data = self.__elements_request()
        elements = self.__create_elements(response_data, regexp)
        return elements

    @staticmethod
    def get_board_by_id(board_id: str, platform_access: PlatformAccess,
                        need_name: bool = True) -> Optional['Board']:
        """
        Returns a board by its ID

        :param board_id: Board's ID on the platform/back-end
        :param platform_access: PlatformAccess object of a(n) user/agent
                                                which has access to this board?..
        :param need_name: Either to force-get (via request) board's name or not

        :return: Board instance for the given ID, or None if a board can't be created
        """
        name = ''
        if need_name:
            http_method = 'GET'
            detail = 'boards'
            url = f'{platform_access.get_platform_url()}/boards/{board_id}'
            values = {}
            headers = platform_access.get_headers(http_method, url, values, detail)
            response = None
            try:
                response = request(method=http_method, url=url, headers=headers)
                response.raise_for_status()
            except HTTPError as http_error:
                logger.exception(OWN_ADAPTER_NAME,
                                 f'Could not perform name extraction: {http_error}',
                                 response)
            except ConnectionError as connect_error:
                logger.exception(OWN_ADAPTER_NAME,
                                 f'Could not perform name extraction, connection-error: {connect_error}',
                                 response)
            else:
                response_data = response.json()
                name = response_data['board']['name']

        # TODO: Check if the board exists?.. I.e., ID is correct, and the PlatformAccess-object can get it
        board = Board(platform_access, name, board_id)
        return board

    def __elements_request(self) -> Optional[Dict]:
        """
        Composes board's elements

        :return: Data on/of board's elements if a request was successful, otherwise None
        """
        http_method = 'GET'
        detail = 'elements'
        url = compose_path(self.__url, 'elements')
        values = {}
        headers = self.__platform_access.get_headers(http_method, url, values, detail)
        try:
            response = request(method=http_method, url=url, headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            logger.exception(OWN_ADAPTER_NAME, f'{http_error}')
            return None
        except ConnectionError as connect_error:
            logger.exception(OWN_ADAPTER_NAME, f'{connect_error}')
            return None
        response_data = response.json()
        return response_data

    def __create_elem_from_response(self, elem_response: Dict,
                                    regexp: str = None) -> Optional[Element]:
        """
        Creates element from a response dictionary.
        If regexp is given, also checks if name/caption matches regular expression

        :param elem_response: Raw data from a platform's response for a single Element
        :param regexp: Regular expression to a caption-match check

        :return: object: New Element, if every field persist.
                If regexp is given, also filters element's name/caption
                Any other case -- None
        """
        name = ''
        agent_task_id = elem_response.get('agentTaskId', None)
        agent_data_id = None
        if agent_task_id:
            for link in elem_response['_links']:
                if link['rel'] == 'agentTask':
                    # Extract AgentData's ID
                    agent_data_id = int(link['href'].split('agentdata/')[1].split('/')[0])

        # Caption
        if elem_response['caption'] is not None:
            name = elem_response['caption']

            if regexp and not re.match(regexp, name):
                return None
        elif not agent_task_id:
            return None

        # Identifier
        if elem_response['_links'][0]['href']:
            id_href = elem_response['_links'][0]['href']
        else:
            return None

        # Position and size
        if elem_response['posX'] and elem_response['posY'] \
                and elem_response['sizeX'] and elem_response['sizeY']:
            pos_x = elem_response['posX']
            pos_y = elem_response['posY']
            size_x = elem_response['sizeX']
            size_y = elem_response['sizeY']
        else:
            return None

        element = Element(platform_access=self.__platform_access,
                          name=name, identifier=id_href, board=self,
                          pos_x=pos_x, pos_y=pos_y, size_x=size_x, size_y=size_y,
                          agent_task_id=agent_task_id, agent_data_id=agent_data_id)
        return element

    def __create_elements(self, data: Dict, regexp: str) -> List[Element]:
        """
        Reads response-dictionary, and returns elements that names match regular expression

        :param data: Response from platform, should contain a list of dicts on 'elements' key
        :param regexp: Regular expression to filter the lements

        :return: Returns all the elements which names match regexp
        """
        elements = []
        for element_response in data['elements']:
            new_elem = self.__create_elem_from_response(element_response, regexp)
            if new_elem is not None:
                elements.append(new_elem)
        return elements

    def put_message(self, message: str) -> Optional[int]:
        """
        Posts a new message on the board's activity chat
        Multiple languages are supported

        :param message: Text to post

        :return: Response's status code, or None
        """
        if not message:
            return None

        http_method = 'POST'
        url = compose_path(self.__url, 'posts')
        detail = 'post'

        payload_data = {
            'post': {'message': message}
        }
        payload = json.dumps(payload_data, separators=(',', ':'), ensure_ascii=False)
        values = {}
        headers = self.__platform_access.get_headers(http_method, url, values, detail,
                                                     payload=payload)
        try:
            response = request(method=http_method, url=url, headers=headers, data=payload.encode())
            response_status = response.status_code
            if response_status != HTTPStatus.CREATED:
                logger.exception(OWN_ADAPTER_NAME,
                                 f'Couldn\'t put new message in the {self.get_name()} board. '
                                 f'{response.content}', response)
            return response_status
        except Exception as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Couldn\'t put new message in the {self.get_name()} board.'
                             f'{error}')
            return None

    def get_board_size(self) -> Optional[Dict[str, int]]:
        """
        Gets the board's maximum columns and rows numbers
        :return: dict: {'sizeX': board's max X size, 'sizeY': board's max Y size},
                 or None due to exceptions (BadRequest, etc.)
        """
        http_method = 'GET'
        detail = 'board'
        url = self.__url
        values = {}
        response = None
        try:
            headers = self.__platform_access.get_headers(http_method, url, values, detail)
            # TODO: Bad request handling
            response = request(method=http_method, url=url, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            board_size = {'sizeX': response_data['board']['sizeX'],
                          'sizeY': response_data['board']['sizeY']}
            return board_size
        except Exception as excpt:
            logger.error('engine',
                         f'Bad request response. Check the internet connection.'
                         f'Message: {excpt}',
                         response)
            return None

    def get_elements_matrix(self) -> List[List]:
        """Returns board's grid as 2D matrix"""
        board_size = self.get_board_size()
        response_data = self.__elements_request()
        elements_matrix = self.__create_elements_matrix(board_size, response_data)
        return elements_matrix

    @staticmethod
    def __create_elements_matrix(board_size: Dict,
                                 response_data: Dict) -> Optional[List[List[int]]]:
        """
        Forms 2D-occupation-matrix according board's elements

        :param board_size: {'sizeX': int, 'sizeY': int}
        :param response_data: Data from get_elements' response
        Reference: https://github.com/own-dev/own-agent-open/blob/master/docs/APIDescription.md#get-boardsboardidelements

        :return: 2D-matrix where 1 means this [i;j] cell is occupied by some element,
                                 0 otherwise
                 If IndexError occurred, X-Y matrix filled with 1 is returned
                 FIXME: None is returned instead
        """
        elements_matrix = [[0] * board_size['sizeX'] for _ in range(board_size['sizeY'])]
        for element in response_data['elements']:
            for i in range(1, element['sizeY'] + 1):
                for j in range(1, element['sizeX'] + 1):
                    try:
                        elements_matrix[element['posY'] + i - 2][element['posX'] + j - 2] = 1
                    except IndexError as error:
                        logger.exception(OWN_ADAPTER_NAME,
                                         f'Failed to create elements matrix. Error message: {error}')
                        elements_matrix = [[1] * board_size['sizeX'] for _ in range(board_size['sizeY'])]
                        return elements_matrix
        return elements_matrix

    # put new element on the board
    # two steps: 1. add element with empty name (no message on the board chat);
    # 2. add caption to new element (message on the board chat)
    def add_element(self, pos_x: int, pos_y: int,
                    size_x: int = 1, size_y: int = 1,
                    caption: str = '') -> Union[Element, int, None]:
        """
        Tries to add new element with the given input parameters

        :param pos_x: Start of the element on the X axis
        :param pos_y: Start of the element on the Y axis
        :param size_x: Width of the element (X axis)
        :param size_y: Height of the element (Y axis)
        :param caption: The name of the element

        :return: Either new Element object (if succeeded), or response code
        """
        # add element with an empty name (no creation of the message on the board chat)
        new_element_link = ''
        response = None
        try:
            http_method = 'POST'
            detail = 'activities'
            url = self.__url + '/elements'
            payload_data = {
                'element': {
                    'posX': pos_x,
                    'posY': pos_y,
                    'sizeX': size_x,
                    'sizeY': size_y,
                    'type': 'MultiInput',
                    'caption': caption
                }
            }
            payload_data = json.dumps(payload_data, separators=(',', ':'), ensure_ascii=False)
            values = {}
            headers = self.__platform_access.get_headers(http_method, url, values,
                                                         detail, payload=payload_data)

            response = request(method=http_method, url=url, headers=headers,
                               data=payload_data.encode())
            response.raise_for_status()
            response_data = response.json()
            new_element_link = response_data["element"]["_links"][0]["href"]
        except HTTPError as http_error:
            logger.exception(OWN_ADAPTER_NAME, f'Error: add element to {self.get_name()} failed. '
                                               f'Error type: {http_error}', response)
            return response.status_code
        except ConnectionError as connect_error:
            logger.exception(OWN_ADAPTER_NAME, f'Error: add element to {self.get_name()} failed. '
                                               f'Error type: {connect_error}', response)
            return response.status_code
        except Exception as error:
            logger.exception(OWN_ADAPTER_NAME, f'Unknown error for adding element: {error}',
                             response)
            return None
        # add element name (creation of the message on the board chat)
        try:
            http_method = 'PUT'
            detail = 'element'
            if PREFIX and PREFIX in new_element_link:
                new_element_link = new_element_link[len(PREFIX) + 1:]
            url = compose_path(self.__platform_access.get_platform_url(), new_element_link)
            payload_data = {
                'element': {
                    'posX': pos_x,
                    'posY': pos_y,
                    'sizeX': size_x,
                    'sizeY': size_y,
                    'type': 'MultiInput',
                    'caption': caption
                }
            }
            payload = json.dumps(payload_data, separators=(',', ':'), ensure_ascii=False)
            values = {}
            headers = self.__platform_access.get_headers(http_method, url,
                                                         values, detail, payload=payload)

            response = request(method=http_method, url=url, headers=headers, data=payload.encode())
            response.raise_for_status()
            response_data = response.json()

            new_element = self.__create_elem_from_response(response_data['element'])
            return new_element

        except (HTTPError, ConnectionError) as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error: add element name {caption} to {self.get_name()} failed. '
                             f'Error type: {error}', response)
            return error

    def remove_element(self, element_url) -> Optional[int]:
        """
        Removes board's element by the given element's URL

        :param element_url: Element's URL to be removed

        :return: [Platform's] Response's status code if no networking error occurred,
                              otherwise None is returned
        """
        response = None
        try:
            http_method = 'DELETE'
            detail = 'element'
            url = element_url
            values = {}
            headers = self.__platform_access.get_headers(http_method, url, values, detail)
            response = request(method=http_method, url=url, headers=headers)
            response.raise_for_status()
            return response.status_code
        except HTTPError as error:
            logger.exception(OWN_ADAPTER_NAME, f'Error: remove element {element_url} from'
                                               f'{self.get_name()} failed. Error type: {error}',
                             response)
            return response.status_code
        except ConnectionError as connect_error:
            logger.exception(OWN_ADAPTER_NAME, f'Connection-Error occured for deleting element: '
                                               f'{connect_error}',
                             response)
            return None

    # ––––––––––––––––––––
    # Layout allocation
    # ––––––––––––––––––––
    def find_first_empty_element(self, caller: str = OWN_ADAPTER_NAME) -> Optional[Dict[str, int]]:
        """
        Searchs for an empty element on the given board

        :param caller: Name for the logger

        :return: coordinates (x; y) of the first found empty element, or None
        """
        try:
            grid = self.get_elements_matrix()
            # TODO: extract to a method that finds an empty spot for an element
            # TODO: make saying hello a two step process. The OWN chat message is empty after 'hello'
            # TODO: or is it a frontend problem?

            for pos_y, pos_x in ((y, x) for y in range(len(grid)) for x in range(len(grid[y]))):
                if grid[pos_y][pos_x] == 0:
                    return {'x': pos_x + 1, 'y': pos_y + 1}
            return None
        except Exception as excpt:
            logger.exception(caller,
                             'Error occurred while searching an empty element (Board ID: {}). '
                             'Exception message: {}'.format(str(self.get_id()), str(excpt)))
            return None
