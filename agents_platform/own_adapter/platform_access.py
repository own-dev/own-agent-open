"""
This module's responsible for accessing the back-end's platform
Basically, access tokens, and headers generation
"""

import base64
import datetime
import os
import sys
from typing import Dict

from requests import request

from agents_platform.own_adapter.constants import OWN_ADAPTER_NAME, PREFIX, TOKEN_EXPIRE_DAYS
from utils import logger


class PlatformAccess:
    """
    Answers for accessing to the platform,
    i.e., generating all the access and secret tokens for the given login/password

    Basic usage:
    platform_access = PlatformAccess(agent_login, agent_password)

    """
    __platform_url = ''
    __access_token = ''
    __secret_token = ''
    __login = ''
    __password = ''
    __user_id = ''

    def __init__(self, login: str, password: str):
        """
        :param login: User's login
        :param password: User's password
        Note that Agent is a User with AgentData "assigned" to it
        """
        self.__login = login
        self.__password = password
        self.__token_creation_time = None
        self.__access_token_request()

    def get_access_token(self) -> str:
        """Returns current access token"""
        if not self.__token_creation_time or \
                (datetime.datetime.now() - self.__token_creation_time).days >= TOKEN_EXPIRE_DAYS:
            self.__access_token_request()

        return self.__access_token

    def get_platform_url(self) -> str:
        """Returns current back-end's URL"""
        return self.__platform_url

    def get_user_id(self) -> str:
        """Returns User's ID"""
        return str(self.__user_id)

    def get_headers(self, method: str, url: str, values,
                    detail: str, environment: str = 'development',
                    payload: str = '', additional_headers: Dict = None) -> Dict:
        """
        Compose headers for a back-end

        :param method:
        :param url:
        :param values:
        :param detail: A semantic name of the requested functionality for
                       accept-header or contentType-header
                Example: 'accept': f'application/vnd.uberblik.accesstokens+json'
        :param environment: Environment's name (stated orally?);
               note that for testing, it shouldn't be 'production'
        :param payload:
        :param additional_headers:

        :return:
        """
        return self.__generate_headers(method, url, datetime.datetime.utcnow(),
                                       values, detail, environment, payload,
                                       additional_headers)

    def __access_token_request(self) -> None:
        """
        Updates:
            self.__platform_url
            self.__access_token
            self.__secret_token
            self.__user_id
        according to the given parameters

        Reference: https://github.com/own-dev/own-agent-open/blob/master/docs/APIDescription.md#group-access-tokens

        :return: Nothing. However, could execute sys.exit(1) if:
                                                * no OWN_AGENT_ADDRESS is found
                                                * or authorization failed
        """
        try:
            address = os.environ['OWN_AGENT_ADDRESS']
        except KeyError as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'OWN_AGENT_ADDRESS is not defined. Error message: {error}')
            sys.exit(1)

        http_method = 'POST'
        values = """
              {
                "accessTokenRequest": {
                  "clientId": "we2$%6etetertef",
                  "grantType": "password"
                }
              }
            """.encode()

        auth = base64.b64encode(f'{self.__login}:{self.__password}'.encode())
        detail = 'accessTokenRequest'
        url_postfix = 'accesstokens'

        if PREFIX:
            address += f'/{PREFIX}'

        headers = {
            'Accept': f'application/vnd.uberblik.{detail}+json',
            'Authorization': f'Basic {auth.decode()}'
        }

        try:
            token_response = request(url=f'{address}/{url_postfix}',
                                     method=http_method,
                                     data=values, headers=headers)
            token_response.raise_for_status()
        except Exception as error:
            logger.exception(OWN_ADAPTER_NAME,
                             f'Authorization failed.\n'
                             f'URL: {address}/{url_postfix}\n'
                             f'Headers: {headers}\n'
                             f'Exception message: {error}')
            sys.exit(1)
        else:
            response_data = token_response.json()

            self.__platform_url = address
            self.__token_creation_time = datetime.datetime.now()
            self.__access_token = response_data['accessToken']['token']
            self.__secret_token = response_data['accessToken']['secret']
            self.__user_id = int(response_data['accessToken']['_links'][1]['href'].split('/')[-1])

    def __generate_headers(self, method: str, url: str, now, values, detail: str,
                           environment, payload: str = '',
                           additional_headers: Dict = None) -> Dict:
        """

        :param method: HTTP method to generate the headers for;
                       basically, it's {GET|POST|PUT|DELETE}
        :param url: URL-postfix for the required functionality?..
        :param now: Present time in UTC format like datetime.datetime.utcnow()
        :param values:
        :param detail: A semantic name of the requested functionality for
                       accept-header or contentType-header
                Example: 'accept': f'application/vnd.uberblik.accesstokens+json'
        :param environment: Environment's name (stated orally?);
               note that for testing, it shouldn't be 'production'
        :param payload:
        :param additional_headers:

        :return: Authorization-complete, signed headers for a back-end
        """
        # timestamp = 'yyyy-mm-ddThh:mm:ss.055Z'
        timestamp = now.isoformat()[:-3] + "Z"  # ISO8601 formatted timestamp

        headers = {
            'Accept': f'application/vnd.uberblik.{detail}+json',
            'access-token': self.__access_token,
            'x-uberblik-timestamp': timestamp
        }
        if additional_headers:
            headers.update(additional_headers)

        return headers
