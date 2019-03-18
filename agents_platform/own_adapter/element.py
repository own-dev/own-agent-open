"""
[Incomplete, not full] OWN-board's Element replication
Contains both data and logic
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union
from urllib import parse

import requests
from requests import request, post, HTTPError

from agents_platform.own_adapter.constants import OWN_ADAPTER_NAME, PREFIX, AdapterStatus
from agents_platform.own_adapter.file import File
from agents_platform.own_adapter.platform_access import PlatformAccess
from agents_platform.util.networking import make_request, compose_path
from utils import logger
from utils.link import Link

BOARD_SHIFT = 1
DEFAULT_PROCESSING_DATETIME_VALUE = '2000.01.01 00:00:00'
DEFAULT_PROCESSING_DATETIME_FORMAT = '%Y.%m.%d %H:%M:%S'
DEFAULT_PROCESSING_DATETIME = datetime.strptime(DEFAULT_PROCESSING_DATETIME_VALUE,
                                                DEFAULT_PROCESSING_DATETIME_FORMAT)
DEFAULT_IMAGE_URL = 'https://www.own.space/images/other/htmlrefdefault.png'


class Element:
    """Represents OWN-board's element"""
    __name = ''
    __url = ''
    __board = None
    __last_processing_time = None

    def __init__(self, platform_access: PlatformAccess,
                 name: str = '', identifier: str = '', board: 'Board' = None,
                 pos_x: int = None, pos_y: int = None, size_x: int = None, size_y: int = None,
                 last_processing_time: datetime = DEFAULT_PROCESSING_DATETIME,
                 agent_task_id: int = None, agent_data_id: int = None):
        """
        :param platform_access: PlatformAccess of a user
                                who has access rights to it [board, i.e., boards]
        :param name: Element's caption
        :param identifier: Element's ID
        :param board: The board on which the element is on
        :param pos_x: Element's horizontal position, starting with 1
        :param pos_y: Element's vertical position, starting with 1
        :param size_x: Element's width
        :param size_y: Element's height
        :param last_processing_time: The last time this element was processed
        :param agent_task_id: AgentTask's ID that is assigned to the element (if some)
        :param agent_data_id: AgentData's ID of an agent that is assigned to the element
                              (if there is some)
        """
        self.__platform_access = platform_access
        self.__name = name
        if PREFIX and PREFIX in identifier:
            identifier = identifier[len(PREFIX) + 1:]
        self.__url = platform_access.get_platform_url() + identifier
        self.__id = identifier
        self.__board = board
        self.__last_processing_time = last_processing_time

        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__size_x = size_x
        self.__size_y = size_y

        self.__agent_task_id = agent_task_id
        self.__agent_data_id = agent_data_id

    def get_agent_data_id(self) -> Optional[int]:
        """Returns this element's agent data ID if it was given [in ctor]"""
        # TODO: Request it from a platform instead
        return self.__agent_data_id

    def get_agent_task_id(self) -> Optional[int]:
        """Returns this element's agent task ID if it was given [in ctor]"""
        return self.__agent_task_id

    def get_url(self) -> str:
        """Returns this element's URL"""
        return self.__url

    def get_name(self) -> str:
        """Returns this element's name if it was given [in ctor]"""
        # TODO: Shouldn't it request the data from a back-end?..
        return self.__name

    def set_name(self, new_caption: str) -> Optional[requests.Response]:
        """
        Sets new caption for the element

        :param new_caption: New name to be set as caption
        :return: Returns `requests.Response` if the given parameters were correct, otherwise None
        """
        if not new_caption:
            logger.error(OWN_ADAPTER_NAME, f'No new_caption received for set_name: {new_caption}')
            return None
        if not isinstance(new_caption, str):
            logger.error(OWN_ADAPTER_NAME, f'Received new_caption is not string: {new_caption}')
            return None

        # Update the local caption
        self.__name = new_caption

        # Prepare the data to update request
        method = 'PUT'
        detail = 'element'
        elem_id = self.get_id()
        # TODO: Fix self.get_id() returns '/boards/{board_id}/elements/{elem_id}'
        url = elem_id[1:]
        data = {
            'element': {
                'caption': new_caption
            }
        }

        # Update the remote caption
        response = make_request(platform_access=self.__platform_access,
                                http_method=method, url_postfix=url, detail=detail, data=data)
        if response:
            logger.debug(OWN_ADAPTER_NAME, f'Caption successfully changed to [{new_caption}].', response)
        else:
            logger.error(OWN_ADAPTER_NAME, f'Caption was not set up: {response}')
        # FIXME: Shouldn't we return status_code instead?
        return response

    def get_id(self) -> str:
        """Returns element's ID if it was given (in ctor)"""
        return self.__id

    def get_board(self) -> 'Board':
        """Returns element's board if it was given (in ctor)"""
        return self.__board

    def _get_elem_response(self) -> Optional[Dict]:
        """
        Returns response body for the element

        :return: The dictionary with the following fields:
      "sizeX": {int},
      "sizeY": {int},
      "posX": {int},
      "posY": {int},
      "caption": str,
      "type": "MultiInput",
      "fileCount": {int},
      "agentTaskId": {int|null},
      "_links": [
        {
          "rel": "self",
          "href": "/boards/{int}/elements/{int}"
        },
        {
          "rel": "files",
          "href": "/boards/{int}/elements/{int}/files"
        },
        {
          "rel": "thumbnail",
          "href": "/boards/{int}/elements/{int}/thumbnail"
        },
        {
          "rel": "boardThumbnail",
          "href": "/boards/{int}/elements/{int}/boardThumbnail"
        },
        {
          "rel": "masterThumbnail",
          "href": "/boards/{int}/elements/{int}/masterThumbnail"
        }
      ]
        """
        # Prepare request data
        http_method = 'GET'
        detail = 'element'
        url = self.__url
        values = {}
        headers = self.__platform_access.get_headers(http_method, url, values, detail)
        try:
            response = request(method=http_method, url=url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
        except HTTPError as error:
            logger.exception(OWN_ADAPTER_NAME, 'Could not get response for the element: '
                                               f'{error}')
            return None

        if response_data:
            return response_data['element']
        return None

    def get_position(self) -> Tuple[int, int]:
        """Returns the element's position on the board"""
        # Since response returns elements starting from 1, decrement them (BOARD_SHIFT==1)
        response_body = self._get_elem_response()
        x = int(response_body['posX']) - BOARD_SHIFT
        y = int(response_body['posY']) - BOARD_SHIFT
        return x, y

    def get_size(self) -> Tuple[int, int]:
        """Returns the element's size on the board"""
        response_body = self._get_elem_response()
        size_x = int(response_body['sizeX'])
        size_y = int(response_body['sizeY'])
        return size_x, size_y

    def get_last_processing_time(self) -> datetime:
        """Returns the last "checkpoint" (timestamp) when the element was proceed"""
        return self.__last_processing_time

    def set_last_processing_time(self, last_processing_time: datetime) -> None:
        """Sets a new timestamp for "element's last processed checkpoint"""
        self.__last_processing_time = last_processing_time

    def to_dictionary(self) -> Dict:
        """Returns the element serialized to a dictionary"""
        last_proc_time = self.get_last_processing_time()
        if last_proc_time:
            last_proc_time = last_proc_time.strftime(DEFAULT_PROCESSING_DATETIME_FORMAT)
        else:
            last_proc_time = ''
        sizes = self.get_size()
        coords = self.get_position()

        element_data = {
            'id': self.get_id(),
            'name': self.get_name(),
            'last_processing_time': last_proc_time,
            'url': self.get_url(),
            'pos_x': coords[0],
            'pos_y': coords[1],
            'size_x': sizes[0],
            'size_y': sizes[1],
            'agent_data_id': self.get_agent_data_id(),
            'agent_task_id': self.get_agent_task_id()
        }
        return element_data

    @staticmethod
    def from_dictionary(platform_access: PlatformAccess, element_dict: Dict):
        """Deserializes the given dict and returns a new element"""
        from agents_platform.own_adapter.board import Board
        # DON'T MOVE TO imports SECTION!
        # Otherwise, you'll meet with circular dependency
        # Update: Is it still relevant?..

        name = element_dict['name']
        element_id = element_dict['id']
        board_id = element_id.split('/')[-3]
        board = Board.get_board_by_id(board_id, platform_access, need_name=False)

        str_last_processing_time = element_dict.get('last_processing_time', '')
        last_processing_time = DEFAULT_PROCESSING_DATETIME \
            if not str_last_processing_time \
            else datetime.strptime(str_last_processing_time, DEFAULT_PROCESSING_DATETIME_FORMAT)

        element = Element(platform_access, name, element_id,
                          last_processing_time=last_processing_time, board=board)
        return element

    def get_files(self) -> List[File]:
        """
        Sends the request to the back-end, retrieving element's files
        :return: Files remotely retrieved for an element
        """
        http_method = 'GET'
        detail = 'board'
        url = self.__url + '/files'
        values = {}
        try:
            headers = self.__platform_access.get_headers(http_method, url, values, detail)
            response = request(method=http_method, url=url, headers=headers)
            response_data = response.json()
        except HTTPError as error:
            logger.exception(OWN_ADAPTER_NAME, f'Couldn\'t get the element\'s files: {error}')
            return []

        files = self.__create_files(response_data)
        return files

    def __create_files(self, dictionary: Dict) -> List[File]:
        """
        Creates a list of Files out of the given dictionary
        :param dictionary: Typically, a response from self.get_files()
        :return: Composed list of Files
        """
        files = []
        for element in dictionary['files']:
            href = element['_links'][0]['href']
            name = element['name']
            file_type = element['fileType']
            files.append(File(self.__platform_access, name, href, file_type, self))
        return files

    def put_link(self, link: Link,
                 image_url: str = DEFAULT_IMAGE_URL,
                 return_url: bool = False, scrape_images_from_url: bool = True) -> Union[int, Tuple[int, str], None]:
        """
        Puts a link to this element
        [Links work as Files]

        :param link: Link-object to put in this element
        :param image_url: Link's image URL
        :param return_url: Either return the link's address (URL) or not
                           [It's used when we want to put comment to the link]
        :param scrape_images_from_url: if True, image will be taken from link, else from image_url

        :return: If URL is requested to be returned, tuple of response code and URL;
                 If it wasn't, response code;
                 If there was some exception (like HTTPError), or no link is provided, None
        """
        if not link:
            return None

        link_url = parse.quote(link.get_url(), safe='%/:=&?~#+!$,;\'@()*[]')
        title = link.get_title()
        description = link.get_description()
        response = None

        try:
            http_method = 'POST'
            detail = 'htmlReference'
            url = self.__url + '/files'
            additional_headers = {'Content-Type': 'application/json; charset=UTF-8'}
            payload = json.dumps({
                'htmlReference': {
                    'url': link_url,
                    'defaultImageUrl': image_url,
                    'title': title,
                    'summary': description,
                    'scrapeImagesFromUrl': scrape_images_from_url
                }
            }, separators=(',', ':'), ensure_ascii=False)
            values = {}
            headers = self.__platform_access.get_headers(http_method, url, values, detail,
                                                         payload=payload,
                                                         additional_headers=additional_headers)

            response = post(url, headers=headers, data=payload.encode())
            response_status = response.status_code
            response.raise_for_status()

            response_url = response.json().get('htmlReference').get('_links')[0].get('href')
            full_url = url + '/' + response_url.split('/')[-1]
            if return_url:
                return response_status, full_url
            return response_status
        except HTTPError as http_error:
            logger.exception(OWN_ADAPTER_NAME, f'Error: put link {link_url} to {self.get_name()} failed. '
                                               f'Error type: {http_error}', response)
            return response.status_code
        except ConnectionError as connect_error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Connection-Error: put link {link_url} to {self.get_name()} failed: '
                             f'{connect_error}', response)
            return None
        except Exception as error:
            logger.exception(OWN_ADAPTER_NAME, f'Error: put link {link_url} to {self.get_name()} failed. '
                                               f'Error type: {error}')
            return None

    def put_file(self, file_name: str, file_bytes: Union[bytearray, str],
                 get_file: bool = False) -> Union[int, File, None]:
        """
        Puts an arbitrary file to the element
        (It should have 'multipart/form-data' support automatically.
        Check if there is enough free space if 413 occurs)

        :param file_name: file title to save as
        :param file_bytes: File's bytes, or text to put
        :param get_file: should a File for the uploaded file returned? This costs
        and additional request. See the return section for details.

        :return: if get_file, then returns a File or None on error.
        if not get_file, then returns the status_code from API, or None on non-HTTP errors.
        """
        # use this for multipart/form-data
        # https://stackoverflow.com/questions/6260457/using-headers-with-the-python-requests-librarys-get-method
        # additional reference
        # https://stackoverflow.com/questions/4007969/application-x-www-form-urlencoded-or-multipart-form-data
        # to dump raw requests/responses you can use http://toolbelt.readthedocs.io/en/latest/dumputils.html
        response = None
        http_method = 'POST'
        detail = 'fileCreationResponse'
        url = self.__url + '/files'
        additional_headers = {}
        payload = ''
        values = {}

        try:
            headers = self.__platform_access.get_headers(http_method, url, values, detail, payload=payload,
                                                         additional_headers=additional_headers)
            response = post(url, headers=headers, files={file_name: (file_name, file_bytes)})
            response.raise_for_status()

            if get_file:
                r_json = response.json()
                if 'href' in r_json['fileCreationResponse']['_links'][0]:
                    ref = r_json['fileCreationResponse']['_links'][0]['href']
                    file_id = ref.split('/')[-1]
                    file = File(platform_access=self.__platform_access,
                                identifier=file_id,
                                name=file_name,
                                file_type=r_json['fileCreationResponse']['fileType'],
                                element=self)
                    return file
                # FIXME: Why don't we return status_code from the previous request?..
                return None
            return response.status_code

        except requests.ConnectionError as connection_error:
            logger.warning(OWN_ADAPTER_NAME,
                           f'Warning: put file {file_name} to {self.get_name()} took too long.'
                           f' Probably because file was too large. Error type: {connection_error}', response)
            return AdapterStatus.CONNECTION_ABORTED
        except HTTPError as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error: put file {file_name} to {self.get_name()} failed. '
                             f'Error type: {error}', response)
            return None if get_file else response.status_code
        except Exception as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error: put file {file_name} to {self.get_name()} failed.'
                             f'Error type: {error}')
            return None

    def put_chart(self, title: str, chart_type: str, data: Dict, get_file: bool = False) -> Union[int, File, None]:
        """
        Puts a chart to the element

        :param title: a title of the chart
        :param chart_type: a type of the chart
        :param data: data to show in the chart
        Look for more detailed content explanation here:
        https://own1.docs.apiary.io/#reference/element-files,-thumbnails-and-previews/get

        :return: status_code from api or file_id,
        -1 if some line has less than 2 points,
        0 or exception code in case of exception
        """
        response = None
        try:
            http_method = 'POST'
            detail = 'chart'
            url = self.__url + '/files'
            additional_headers = {'Content-Type': 'application/json; charset=UTF-8'}
            payload = json.dumps({
                'chart': {
                    'title': title,
                    'type': chart_type,
                    'data': data,
                }
            }, separators=(',', ':'), ensure_ascii=False)
            for line in data['series']:
                if len(line['data']) < 2:
                    logger.warning(OWN_ADAPTER_NAME, f'Error: put chart {title} to {self.get_name()} failed. '
                                                     f'Error type: data {line["name"]} has less than 2 points')
                    return -1

            values = {}
            headers = self.__platform_access.get_headers(http_method, url, values, detail, payload=payload,
                                                         additional_headers=additional_headers)

            response = post(url, headers=headers, data=payload.encode())
            response.raise_for_status()
            response_status = response.status_code
            if get_file:
                r_json = response.json()
                chart = r_json.get('chart', {})
                file_id = chart.get('fileId', 0)
                file = File(platform_access=self.__platform_access, identifier=str(file_id), element=self)
                return file
            else:
                return response_status
        except requests.HTTPError as error:
            logger.exception(OWN_ADAPTER_NAME, f'Error: put chart {title} to {self.get_name()} failed. '
                                               f'Error type: {error}', response)
            return response.status_code
        except Exception as error:
            logger.exception(OWN_ADAPTER_NAME, f'Error: put chart {title} to {self.get_name()} failed. '
                                               f'Error type: {error}', response or None)
            return None

    def update_chart(self, title: str, chart_type: str, file_id: str, data: Dict) -> Optional[int]:
        """
        Updates existing chart in element by adding new data
        :param title: chart title
        :param chart_type: type of a chart
        :param file_id: id of chart file
        :param data: new chart data
        :return: success code or 0/None if error happened
        """
        file = File(platform_access=self.__platform_access, identifier=file_id, element=self)
        res = file.update_chart(title, chart_type, data=data)
        return res

    def remove_file(self, file_link: str) -> Optional[int]:
        """
        Removes a file from the element

        :param file_link: URL to a file to remove

        :return:
        """
        response = None
        try:
            http_method = 'DELETE'
            detail = 'board'
            url = file_link
            values = {}
            headers = self.__platform_access.get_headers(http_method, url, values, detail)

            response = request(method=http_method, url=url, headers=headers)
            response_status = response.status_code

            logger.debug(OWN_ADAPTER_NAME, response_status)
            return response_status
        except HTTPError as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error: remove file {file_link} from {self.get_name()} failed. '
                             f'Error type: {error}', response)
            return None

    def remove_files_by_types(self, types_to_rm: List[str], *args) -> None:
        """
        Removes all the files from an element that match the given types
        If no types were given, removes all the files in this element

        :type args: List[File]: To remove certain files
        :param types_to_rm: Types of the files to remove (i.e., it won't remove non-matching type)

        :return: Nothing
        """
        # Flag for removing all the files
        remove_all = False if types_to_rm else True

        # Remove files by the given types
        for file in self.get_files():
            if not remove_all:
                if file.get_type() in types_to_rm:
                    self.remove_file(file.get_url())
            else:
                self.remove_file(file.get_url())

        # Remove certain files
        for file in args:
            self.remove_file(file.get_url())

    @staticmethod
    def get_element_by_id(element_id: int, platform_access: PlatformAccess,
                          board: 'Board') -> Optional['Element']:
        """
        Returns an Element by the given board and ID

        :param element_id: Element's ID to retrieve
        :param platform_access: PlatformAccess of a user with access rights
        :param board: Element's board

        :return: Element if found, otherwise None
        """
        # Compose the request, execute it, and retrieve its data
        http_method = 'GET'
        detail = 'elements'
        url = compose_path(platform_access.get_platform_url(), 'boards', board.get_id(), 'elements', element_id)

        values = {}
        headers = platform_access.get_headers(http_method, url, values, detail)
        response = request(method=http_method, url=url, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        href = response_data['element']['_links'][0]['href']
        name = response_data['element']['caption']

        element = Element(platform_access, name, href, board)
        return element
