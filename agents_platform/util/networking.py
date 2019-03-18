"""
This module is responsible for requests
"""
import json
import sys
from typing import Dict, Optional
from urllib.error import URLError

from requests import request, Response, HTTPError, ConnectionError

from agents_platform.own_adapter.constants import OWN_ADAPTER_NAME
from agents_platform.own_adapter.platform_access import PlatformAccess
from utils.logger import exception, debug


def make_request(platform_access: PlatformAccess,
                 http_method: str,
                 url_postfix: Optional[str],
                 detail: str,
                 data: Dict = None,
                 values: Dict = None,
                 logger_name: str = None) -> Optional[Response]:
    """
    Makes request according the given parameters

    :param platform_access:
    :param http_method: {GET|POST|PUT|DELETE}
    :param url_postfix:
    :param detail:
    :param data: Actual payload
    :param values: # TODO: Check PlatformAccess::get_headers()
    :param logger_name: Name for logging, default is OWN_ADAPTER_NAME
    :return: requests.Response
    """
    # Set default values
    if values is None:
        values = dict()
    if not logger_name:
        logger_name = OWN_ADAPTER_NAME

    try:
        # Generate the payload
        payload = json.dumps(data, separators=(',', ':'), sort_keys=True, ensure_ascii=False).encode('utf-8') if data else ''

        # Generate URL
        url = f'{platform_access.get_platform_url()}'
        if url_postfix:
            url += f'/{url_postfix}'

        debug(logger_name, f'URL: ({http_method}) {url}')

        # Generate headers
        if http_method != 'DELETE':
            headers = platform_access.get_headers(method=http_method,
                                                  url=url,
                                                  values=values,
                                                  detail=detail,
                                                  payload=payload,
                                                  additional_headers={})
        else:
            headers = platform_access.get_headers(method=http_method,
                                                  url=url,
                                                  values=values,
                                                  detail=detail)
    except ConnectionError as con_error:
        errno, strerror = con_error.args
        exception(logger_name, f'Connection error ({errno}): {strerror}')
        return None
    except Exception:
        exception(logger_name,
                  f'Unexpected error while getting headers: {sys.exc_info()[0]}')
        return None
    else:
        debug(logger_name, f'Successfully generated headers:\n{headers}')

    try:
        # Make a request
        if http_method != 'DELETE':
            response = request(url=url, method=http_method, headers=headers,
                               data=payload)
        else:
            response = request(url=url, method=http_method, headers=headers)

    except HTTPError as http_error:
        exception(logger_name, f'HTTP error ({http_error.errno}) while making request: {http_error}')
        return None
    except ConnectionError as con_error:
        exception(logger_name, f'HTTP error ({con_error.errno}) while making request: {con_error}')
        return None
    except URLError as url_error:
        exception(logger_name, f'URL error, failed to reach server: {url_error.reason}')
        return None
    else:
        debug(logger_name, f'Successfully made a request, code {response.status_code}, {response}')
        return response


def compose_path(*path_pieces) -> str:
    """
    Composes path pieces in one part
    Pieces can contain a slash in the start and/or in the end of a string
    :param path_pieces: pieces in appropriate order
    :return: Result path in format: 'piece0/piece1/piece2'
    """
    list_pieces = []
    for piece in path_pieces:
        if not piece:
            continue
        modified_piece = str(piece)
        if modified_piece.startswith('/'):
            modified_piece = modified_piece[1:]
        if modified_piece.endswith('/'):
            modified_piece = modified_piece[:-1]
        list_pieces.append(modified_piece)

    return '/'.join(list_pieces)
