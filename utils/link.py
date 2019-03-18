"""
This class is created to better support transferring links with their attributes among services via JSON
"""
import json
from typing import Dict, Optional

import requests

from agents_platform.own_adapter.constants import OWN_ADAPTER_NAME
from agents_platform.own_adapter.platform_access import PlatformAccess
from utils import logger


class Link:
    _url = ''
    _title = ''
    _description = ''
    _date = ''
    _media_url = ''
    _media_name = ''

    # TODO make sure Link uses with url everywhere and remove default value from constructor
    def __init__(self, url: str = '', title: str = '', description: str = '', date: str = '', media_url: str = '',
                 media_name: str = ''):
        """
        Contains link url and metadata; Can be used for containing video, image, web page, social network, etc link
        :param url: The main URL (the essential of Link class).
                    This is link to the web page with video, social network page, etc.
        :param title: The title of the link, news, video, etc.
                      F.e. %some_youtube_video_name%, or %some_news_title%, etc.
        :param description: The description of the link (the video, news or whatever description)
        :param date: The date of publication (video, news, etc.)
        :param media_url: URL path to preview image
        :param media_name: Can be used as preview description, news published media or how the user wants.
        """
        self._url = url if url else ''
        self._title = title if title else ''
        self._description = description if description else ''
        self._date = date
        self._media_url = media_url
        self._media_name = media_name

    def get_url(self) -> str:
        return self._url

    def get_title(self) -> str:
        return self._title

    def get_description(self) -> str:
        return self._description

    def get_date(self) -> str:
        return self._date

    def get_media_url(self) -> str:
        return self._media_url

    def get_media_name(self) -> str:
        return self._media_name

    def set_title(self, title: str) -> None:
        self._title = title

    def set_description(self, description: str) -> None:
        self._description = description

    def set_media_name(self, media_name: str) -> None:
        self._media_name = media_name

    def to_dictionary(self) -> Dict:
        """Returns the link serialized to a dictionary"""
        return {
            'url': self._url,
            'title': self._title,
            'description': self._description,
            'date': self._date,
            'media_name': self._media_name
        }

    @staticmethod
    def from_dictionary(link_data: Dict) -> Optional['Link']:
        """Deserializes the given dict and returns a new element"""
        if not link_data:
            return None

        url = link_data['url']
        title = link_data['title']
        description = link_data['description']
        media_url = link_data.get('media_url', '')

        link = Link(url, title, description, media_url=media_url)
        return link

    def put_comment(self, platform_access: PlatformAccess,
                    comment: str = '', link: str = '') -> Optional[int]:
        """
        Puts a comment to file
        :param platform_access:
        :param comment: comment text
        :param link: url of link, where to put comment
        :return: response status or none
        """
        try:
            http_method = 'POST'
            detail = 'commentCreationResponse'
            url = link + '/comments'
            additional_headers = {'Content-Type': 'application/json; charset=UTF-8'}
            payload = json.dumps({
                'fileComment': {
                    'message': comment
                }
            }, separators=(',', ':'), ensure_ascii=False)
            values = {}

            headers = platform_access.get_headers(http_method, url, values, detail, payload=payload,
                                                  additional_headers=additional_headers)
            response = requests.post(url=url, headers=headers, data=payload.encode())
            response_status = response.status_code
            response.raise_for_status()
            return response_status
        except requests.HTTPError as e:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error: put comment {self._title} to {self.get_title()} failed. Error type: {e}',
                             response)
            return None
        except Exception as e:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Error: put comment {self._title} to {self.get_title()} failed. Error type: {e}')
            return None
