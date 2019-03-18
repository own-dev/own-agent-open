"""
Helper functions to work with AgentData
"""
import json
from configparser import ConfigParser
from typing import Dict, List, Optional, Union

from requests import HTTPError, ConnectionError

from agents_platform.own_adapter.constants import OWN_ADAPTER_NAME
from agents_platform.own_adapter.platform_access import PlatformAccess
from agents_platform.util.networking import make_request
import utils.logger as logger


def put_agent_data(platform_access: PlatformAccess,
                   data: Union[Dict, str], agent_data_id: int) -> Optional[Dict]:
    """
    Updates the instance of AgentDataConfiguration on the back-end
    Reference: https://github.com/own-dev/own-agent-open/blob/master/docs/APIDescription.md#put-agentdataagentdataid

    :param platform_access: PlatformAccess for this Agent
    :param data: AgentData configuration in dictionary or JSON (str) format
    :param agent_data_id: ID of AgentData for the associated Agent on the back-end

    :return: Updated AgentData if request was successful, or None otherwise
    """
    http_method = 'PUT'
    detail = 'agentData'
    postfix = f'agentdata/{agent_data_id}'
    data['agentData']['agentsUserId'] = platform_access.get_user_id()
    if isinstance(data, str):
        data = json.loads(data)
    try:
        response = make_request(platform_access=platform_access,
                                http_method=http_method,
                                detail=detail,
                                url_postfix=postfix,
                                data=data)
        response.raise_for_status()
    except (HTTPError, ConnectionError) as excpt:
        logger.error(OWN_ADAPTER_NAME, f'Error while updating database: {excpt}', response)
        return None
    else:
        logger.debug(OWN_ADAPTER_NAME, f'Successfully updated the database: {response}', response)
        if response:
            return response.json()
        return None


def post_agent_data(platform_access: PlatformAccess, data: Dict) -> Optional[Dict]:
    """
    Creates new instance of  AgentDataConfiguration on the back-end

    :param platform_access:
    :param data: agentData-like dict TODO: Check if it is dict or str

    :return: New JSON-data (with IDs) if the request was successful, otherwise None
    """
    try:
        http_method = 'POST'
        detail = 'agentData'
        postfix = 'agentdata'
        data['agentData']['agentsUserId'] = platform_access.get_user_id()
        response = make_request(platform_access=platform_access,
                                http_method=http_method,
                                url_postfix=postfix,
                                detail=detail,
                                data=data)

        response.raise_for_status()
    except (HTTPError, ConnectionError) as excpt:
        logger.error(OWN_ADAPTER_NAME, f'Error while updating database: {excpt}', response)
    else:
        logger.debug(OWN_ADAPTER_NAME, f'Successfully updated the database: {response}', response)
        if response:
            return response.json()
        return None


def delete_agent_data(platform_access: PlatformAccess, agent_data_id: int) -> Optional[Dict]:
    """
    Removes AgentData on a back-end for the given AgentData ID
    Reference: https://github.com/own-dev/own-agent-open/blob/master/docs/APIDescription.md#delete-agentdataagentdataid

    :param platform_access:
    :param agent_data_id: Not to confuse with Agent/User ID!..

    :return: Request's response if it was successful, otherwise None
    """
    http_method = 'DELETE'
    detail = 'agentData'
    postfix = f'agentdata/{agent_data_id}'
    try:
        response = make_request(platform_access=platform_access,
                                http_method=http_method,
                                url_postfix=postfix,
                                detail=detail)
        response.raise_for_status()
    except (HTTPError, ConnectionError) as error:
        logger.error(OWN_ADAPTER_NAME, f'Error while updating database: {error}', response)
        return None
    else:
        logger.debug(OWN_ADAPTER_NAME,
                     f'Successfully removed agent-service from the database: {response}',
                     response)
        return response


def get_agent_data_by_id(platform_access: PlatformAccess, agent_data_id: int) -> Optional[Dict]:
    """
    Returns AgentData сonfiguration by the given AgentData ID
    Reference: https://github.com/own-dev/own-agent-open/blob/master/docs/APIDescription.md#put-agentdataagentdataid

    :param platform_access: PlatformAccess instance for this Agent/User
    :param agent_data_id: Not to confuse with User ID!..

    :return: AgentData from JSON if request was successful, otherwise, None
    """
    try:
        http_method = 'GET'
        detail = 'agentData'
        postfix = f'agentdata/{agent_data_id}'
        response = make_request(platform_access=platform_access,
                                http_method=http_method,
                                url_postfix=postfix,
                                detail=detail)
        response.raise_for_status()
    except (HTTPError, ConnectionError) as error:
        logger.error(OWN_ADAPTER_NAME, f'Error while updating database: {error}', response)
    else:
        logger.debug(OWN_ADAPTER_NAME, f'Successfully updated the database: {response}', response)
        if response:
            return response.json()
        return None


def get_agent_data_by_user_id(platform_access: PlatformAccess, user_id: int = None) -> Optional[Dict]:
    """
    Returns agent's data

    :param platform_access: User's PlatformAccess, generated with login/password tuple
    :param user_id: Not to confuse with AgentData ID!..

    :return: AgentData configuration if a request was successful, otherwise None
    """
    if not user_id:
        user_id = platform_access.get_user_id()
    try:
        http_method = 'GET'
        detail = 'agentData'
        postfix = f'user/{user_id}/agentdata'
        response = make_request(platform_access=platform_access,
                                http_method=http_method,
                                url_postfix=postfix,
                                detail=detail)
        response.raise_for_status()
    except (HTTPError, ConnectionError) as error:
        logger.error(OWN_ADAPTER_NAME, f'Error while updating database: {error}', response)
        return None
    else:
        logger.debug(OWN_ADAPTER_NAME, f'Successfully updated the database: {response}', response)
        if response:
            return response.json()
        return None


def get_all_agents_data(platform_access: PlatformAccess) -> Optional[List[Dict]]:
    """
    Returns AgentData for all agents
    Reference: https://github.com/own-dev/own-agent-open/blob/master/docs/APIDescription.md#get-agentdata
    :return:
    [
        {
          "id": int,
          "description": str,
          "salary": float,
          "capacity": int,
          "status": str,
          "agentsUser": {
            "id": int,
            "firstName": str,
            "lastName": str,
            "email": str
          },
          "_links": [
            {
              "rel": str,
              "href": str
            },
            {
              "rel": str,
              "href": str
            }
          ]
        }, ..
    ]
    """
    try:
        http_method = 'GET'
        detail = 'agentData'
        postfix = 'agentdata'
        response = make_request(platform_access=platform_access,
                                http_method=http_method,
                                url_postfix=postfix,
                                detail=detail)
        response.raise_for_status()
    except Exception as excpt:
        logger.error(OWN_ADAPTER_NAME, f'Error while updating database: {excpt}', response)
        return None
    else:
        logger.debug(OWN_ADAPTER_NAME, f'Successfully updated the database: {response}', response)
        if response:
            return response.json().get('agentsData', None)
        return []


def is_config_new(config: str) -> bool:
    """
    Checks whether config (as string data) has ID or not
    :param config: Absolute filepath to a config
    :return: Has 'id' field in 'meta' section = True, otherwise = False
    """
    if not config:
        # TODO: Log here
        return False

    parser = ConfigParser()
    parser.read(config)
    if parser.has_option('meta', 'id'):
        return True
    return False
