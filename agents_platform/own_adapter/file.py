"""
Basic functionality to work with back-end's File
* put_comment
* get_download_link
"""

import json
import sys
from http import HTTPStatus
from typing import Optional, Dict, Union
from urllib import request

import requests
from deprecation import deprecated
from requests import request

from agents_platform.own_adapter.chart_formatter import format_chart_data
from agents_platform.own_adapter.constants import OWN_ADAPTER_NAME, TYPE_KEY, LINE_CHART_TYPE, BAR_CHART_TYPE, \
    PIE_CHART_TYPE, RADAR_CHART_TYPE, SCATTER_CHART_TYPE, AdapterStatus
from agents_platform.own_adapter.platform_access import PlatformAccess
from utils import logger

POSSIBLE_CHART_TYPES = [LINE_CHART_TYPE, BAR_CHART_TYPE, PIE_CHART_TYPE, RADAR_CHART_TYPE, SCATTER_CHART_TYPE]
CHARTS_TO_FORMAT = [LINE_CHART_TYPE, BAR_CHART_TYPE, RADAR_CHART_TYPE]


class File:
    """
    "Replica" of a back-end's File
    """
    __name = ''
    __url = ''
    __type = ''
    __element = None
    __identifier = ''

    # TODO: For thee, be ware of circular dependency (Element)!..
    def __init__(self, platform_access: PlatformAccess, name: str = '',
                 identifier: str = '', file_type: str = '',
                 element: 'Element' = None):
        """
        :param platform_access:
        :param name: File's caption/name
        :param identifier: File's ID in the board+element
        :param file_type: File's type, one of {}
        :param element: Parent element
        """
        self.__platform_access = platform_access
        self.__name = name
        self.__url = element.get_url() + '/files/' + identifier.split('/')[-1]
        self.__type = file_type
        self.__element = element
        self.__identifier = identifier

    def get_name(self) -> str:
        """Returns file's caption/name if it was given in ctor"""
        return self.__name

    def get_type(self) -> str:
        """Returns file's type if it was given in ctor"""
        return self.__type

    def get_url(self) -> str:
        """Returns file's ID if it was given in ctor"""
        return self.__url

    def get_identifier(self) -> str:
        """Returns file's ID if it was given in ctor"""
        return self.__identifier

    def get_element(self) -> 'Element':
        """Returns parent Element if it was given in ctor"""
        return self.__element

    def get_download_link(self) -> Optional[str]:
        """
        Retrieves a download link from a back-end
        :return: Download URL if request was successful, otherwise None
        """
        # there is no download link to files with type "htmlReference"
        if self.__type == 'application/vnd.uberblik.htmlReference':
            return None
        http_method = 'POST'
        detail = 'downloadLink'
        # FIXME: Change to the utility function of urljoin from Andrew
        url = f'{self.__url}/downloadLink'
        values = {}
        try:
            headers = self.__platform_access.get_headers(http_method, url, values, detail)
        except Exception as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error occurred while retrieving file\'s download URL: {error}')
            return None

        try:
            response = request(method=http_method, url=url, headers=headers)
            response_data = response.json()
            download_link = response_data['downloadLink']['url']
            return download_link
        except KeyError as key_error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Key was not found in response\'s data for file\'s download URL: {key_error}')
        except Exception as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error occurred while retrieving file\'s download URL: {error}')
            return None

    @deprecated(details='Use Element.remove_file(file_url) instead')
    def remove(self) -> Optional[int]:
        """
        Removes the file from the element?..
        :return: Either response's status code (if request was successful) or None
        """
        http_method = 'DELETE'
        detail = 'board'
        url = self.__url
        values = {}
        try:
            headers = self.__platform_access.get_headers(http_method, url, values, detail)
        except Exception as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error occured while removing the file: {error}')
            return None

        response = None
        try:
            response = request(method=http_method, url=url, headers=headers)
            response_code = response.status_code
            response.raise_for_status()
        except Exception as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error occurred while removing the file: {error}',
                             response)
            return None
        logger.debug(OWN_ADAPTER_NAME, response_code, response)
        return response_code

    def put_comment(self, comment: str = '') -> Optional[int]:
        """
        Puts a comment to file
        :param comment: Text to put as a comment
        :return: Response's status code if request was done,
                 None if some exception occurred
        """
        response = None
        try:
            http_method = 'POST'
            detail = 'commentCreationResponse'
            url = self.__url + '/comments'
            additional_headers = {'Content-Type': 'application/json; charset=UTF-8'}
            payload = json.dumps({
                'fileComment': {
                    'message': comment
                }
            }, separators=(',', ':'), ensure_ascii=False)
            values = {}
            headers = self.__platform_access.get_headers(http_method, url, values, detail, payload=payload,
                                                         additional_headers=additional_headers)

            response = requests.post(url=url, headers=headers, data=payload.encode())
            response_status = response.status_code
            response.raise_for_status()
            return response_status
        except requests.HTTPError as http_error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error: put comment {self.get_name()} to {self.get_name()} failed. Error type: {http_error}',
                             response)
            return None
        except Exception as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error: put comment {self.get_name()} to {self.get_name()} failed. Error type: {error}')
            return None

    def get_chart_data_from_file(self) -> Optional[Dict]:
        """
        Gets data from chart
        :return: dictionary with chart data:
        {
            'title': 'very interesting company chart',
            'type': 'BAR',
            'data': { 'series': [],
                      'xAxis{indicator}':{}, … specific to chart type
                      }
        }
        """
        chart = None
        if self.__identifier and self.__identifier != '0':
            response = None
            try:

                http_method = 'GET'
                detail = 'chart'
                values = {}
                additional_headers = {
                    'Content-Type': 'application/json'
                }
                headers = self.__platform_access.get_headers(http_method, self.get_url(), values, detail,
                                                             additional_headers=additional_headers)
                response = requests.get(self.get_url(), headers=headers)
                response.raise_for_status()

                file_dict = json.loads(response.content)
                chart = file_dict['chart']
            except requests.HTTPError as e:
                logger.exception(OWN_ADAPTER_NAME,
                                 f'Error: couldn\'t get chart form file: {self.get_url()}. Error type: {e}.'
                                 f' Response: {response.status_code}',
                                 response=response)
                return None
            except Exception as e:
                logger.exception(OWN_ADAPTER_NAME,
                                 f'Error: couldn\'t get chart form file: {self.get_url()}. Error type: {e}',
                                 response=response)
                return None
        return chart

    def get_data_from_file(self, detail: str, additional_headers: Dict) -> Optional[Dict]:
        """
        Returns File data from board
        :param detail: Content-Type part in headers. Can be: chart, htmlReference...
        :param additional_headers: Dict with additional headers parameters
                For chart and htmlReference: { 'Content-Type': 'application/json' }
        :return: Dict with requested data or None if request broken
        """
        result = None
        if self.__identifier and self.__identifier != '0':
            response = None
            try:
                http_method = 'GET'
                values = {}
                headers = self.__platform_access.get_headers(http_method, self.get_url(), values, detail,
                                                             additional_headers=additional_headers)
                response = requests.get(self.get_url(), headers=headers)
                response.raise_for_status()

                result = json.loads(response.content)
            except requests.HTTPError as e:
                logger.exception(OWN_ADAPTER_NAME,
                                 f'Error: couldn\'t get {detail} form file: {self.get_url()}. Error type: {e}.'
                                 f' Response: {response.status_code}',
                                 response=response)
                return None
            except Exception as e:
                logger.exception(OWN_ADAPTER_NAME,
                                 f'Error: couldn\'t get {detail} form file: {self.get_url()}. Error type: {e}',
                                 response=response)
                return None
        return result

    def get_chart_data(self) -> Optional[Dict]:
        """
        Gets data from chart
        :return: dictionary with chart data:
        {
            'title': 'very interesting company chart',
            'type': 'BAR',
            'data': { 'series': [],
                      'xAxis{indicator}':{}, … specific to chart type
                      }
        }
        """
        chart = None
        additional_headers = {
            'Content-Type': 'application/json'
        }
        file_dict = self.get_data_from_file('chart', additional_headers)
        if file_dict:
            chart = file_dict['chart']
        return chart

    def get_link_data(self) -> Optional[Dict]:
        """
        Returns data from link
        :return: dictionary with link data:
        {
            "htmlReference" : {
                "url" : "http://www.spiegel.de",
                "date" : "2007-12-24T18:21Z",
                "summary" : "lorem ipsum ...",
                "thumbs" : [
                    { "url" : "http://www.spiegel.de/img1.jpg" },
                    { "url" : "http://www.spiegel.de/img2.jpg" }
                ],
                "_links":
                [
                    { "rel" : "self", "href": "/boards/211/elements/6327654/files/9755" },
                    { "rel" : "thumbnail", "href": "/boards/211/elements/6327654/files/9755/thumbnail" },
                    { "rel" : "boardThumbnail", "href": "/boards/211/elements/6327654/files/9755/boardThumbnail" },
                    { "rel" : "preview", "href": "/boards/211/elements/6327654/files/9755/preview" },
                    { "rel" : "downloadLink", "href": "/boards/211/elements/6327654/files/9755/download" },
                    { "rel" : "comments, "href" : "/boards/211/elements/6327654/files/9755/comments" }
                ]
            }
        }
        """
        link = None
        additional_headers = {
            'Content-Type': 'application/json'
        }
        file_dict = self.get_data_from_file('htmlReference', additional_headers)
        if file_dict:
            link = file_dict['htmlReference']
        return link

    def update_chart(self, title: str, chart_type: str, data: Dict) -> AdapterStatus:
        """
        Updates chart in current file
        :param title: chart title
        :param chart_type: [LINE, BAR, PIE, RADAR, SCATTER]
        :param data: new data for chart
        :return: -1 if update failed, 1 in case of partially update, 2 in case of success
        """
        old_chart_data = self.get_chart_data_from_file()
        new_series_data = {}
        if old_chart_data == None:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error: couldn\'t update chart {title} in file {self.get_identifier()}'
                             f' as couldn\'t get previos chart data')
            return AdapterStatus.FAIL

        if old_chart_data[TYPE_KEY] != chart_type:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error: couldn\'t update chart {title} in file {self.get_identifier()}'
                             f' as existing and update charts have different types')
            return AdapterStatus.FAIL
        if chart_type not in POSSIBLE_CHART_TYPES:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Wrong chart type: {chart_type}, cannot update in file {self.get_identifier()}')
            return AdapterStatus.FAIL

        new_series_data = {}
        existing_series_data = data
        if chart_type in CHARTS_TO_FORMAT:
            new_series_data, existing_series_data = format_chart_data(chart_type, data, old_chart_data)

        update_res = self.send_chart_update_request(title, chart_type, existing_series_data)
        status = AdapterStatus.FAIL
        if update_res == HTTPStatus.OK:
            status = AdapterStatus.PARTIAL_UPDATE
            if new_series_data:
                # send separate request to add new series
                update_res = self.send_chart_update_request(title, chart_type, new_series_data)
                if update_res != HTTPStatus.OK:
                    logger.exception(OWN_ADAPTER_NAME,
                                     f'Couldn\'t add new series to chart {title} in file {self.get_identifier()}. Response: {update_res}')
                status = AdapterStatus.SUCCESS
        else:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Couldn\'t update chart {title} in file {self.get_identifier()}. Response: {update_res}')
            return AdapterStatus.FAIL

        update_res = self.set_file_index(sys.maxsize)
        if update_res != HTTPStatus.OK:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Couldn\'t set chart {title} as first file in element. Response: {update_res}')

        return status

    def send_chart_update_request(self, title: str, chart_type: str, data: Dict) -> Union[int, AdapterStatus]:
        """
        Send request to update chart data in current file
        :param title: chart title
        :param chart_type: type of chart
        :param data: data to update chart
        :return: response status or adapterStatus.FAIL if failed
        """

        response = None
        try:
            http_method = 'PATCH'
            detail = 'chart'
            payload = json.dumps({
                'chart': {
                    'title': title,
                    'type': chart_type,
                    'data': data,
                }
            }, separators=(',', ':'), ensure_ascii=False)

            additional_headers = {'Content-Type': 'application/json; charset=UTF-8'}
            url = self.get_url()
            values = {}
            headers = self.__platform_access.get_headers(http_method, url, values, detail, payload=payload,
                                                         additional_headers=additional_headers)

            response = requests.patch(url, headers=headers, data=payload.encode())
            response_status = response.status_code
            response.raise_for_status()
            return response_status
        except requests.HTTPError as e:
            logger.exception(OWN_ADAPTER_NAME, f'Error: update chart {title} to {self.get_name()} failed. '
                                               f'Error type: {e}', response)
            return AdapterStatus.FAIL
        except Exception as e:
            logger.exception(OWN_ADAPTER_NAME, f'Error: update chart {title} to {self.get_name()} failed. '
                                               f'Error type: {e}', response or None)
            return AdapterStatus.FAIL

    def set_file_index(self, index: int) -> Union[int, AdapterStatus]:
        """
        Changes file order in element
        :param index: new file index in a pile of documents
        :return: adapterStatus.FAIL if failed, response_status otherwise
        """
        files = self.__element.get_files()
        index = max(0, index)
        index = min(index, len(files) - 1)
        response = None
        try:
            http_method = 'PATCH'
            detail = 'file'
            url = self.get_url()
            payload = json.dumps({
                'file': {
                    'index': index,
                }
            }, separators=(',', ':'), ensure_ascii=False)
            values = {}

            headers = self.__platform_access.get_headers(http_method, url, values, detail, payload=payload,
                                                         additional_headers={})

            response = requests.patch(url, headers=headers, data=payload)
            response_status = response.status_code
            response.raise_for_status()

            return response_status
        except requests.HTTPError as e:
            logger.exception(OWN_ADAPTER_NAME, f'Error: update chart {self.get_identifier()}'
                                               f' index to {self.get_name()} failed. '
                                               f'Error type: {e}', response)
            return AdapterStatus.FAIL
        except Exception as e:
            logger.exception(OWN_ADAPTER_NAME, f'Error: update chart {self.get_identifier()}'
                                               f' index to {self.get_name()} failed. '
                                               f'Error type: {e}', response or None)
            return AdapterStatus.FAIL
