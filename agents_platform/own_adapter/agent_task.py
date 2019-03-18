"""
Form's replication
"""

import json
import os
from typing import Dict, List, Optional

from requests import ConnectionError, RequestException, Response, HTTPError

import utils.logger as logger
from agents_platform.own_adapter.constants import OWN_ADAPTER_NAME, AGENTS_SERVICES_PATH
from agents_platform.own_adapter.platform_access import PlatformAccess
from agents_platform.util.networking import make_request, compose_path


def get_all_agent_tasks(platform_access: PlatformAccess,
                        agent_data_id: int) -> Optional[List[Dict]]:
    """
    Retrieves all the agent tasks for each agent-service
    :param platform_access:
    :param agent_data_id:
    :return:
    """
    if not (platform_access and agent_data_id):
        return None

    http_method = 'GET'
    detail = 'agentTask'
    postfix = f'agentdata/{agent_data_id}/agenttasks'
    response = make_request(platform_access=platform_access,
                            http_method=http_method,
                            url_postfix=postfix,
                            detail=detail)
    if response:
        return response.json()
    return None


def get_agent_task_by_id(platform_access: PlatformAccess, agent_task_id: int,
                         agent_data_id: int) -> Optional[Dict]:
    """
    Returns JSON from the given AgentDataID and AgentTaskID
    :param agent_task_id: an agent task id
    :param agent_data_id: an agent data id
    :param platform_access: a platform access
    :return: Response's data from a back-end if no error occurred, otherwise None
    """
    if not (agent_task_id and agent_data_id):
        return None
    try:
        # Prepare request-data
        url = f'agentdata/{agent_data_id}/agenttasks/{agent_task_id}/configuration'
        detail = 'agentTaskConfiguration'
        response = make_request(platform_access=platform_access,
                                http_method='GET',
                                url_postfix=url,
                                detail=detail)

        response.raise_for_status()
        return response.json()
    except ConnectionError as con_err:
        logger.exception(OWN_ADAPTER_NAME, f'Connection error for Form: {con_err}')
    except RequestException as req_excpt:
        logger.exception(OWN_ADAPTER_NAME, f'During getting the data for Form, occurred: '
                                           f'{req_excpt}')
    except KeyError as key_excpt:
        logger.exception(OWN_ADAPTER_NAME, f'Could not find data inside JSON: {key_excpt}')
    except Exception as error:
        logger.exception(OWN_ADAPTER_NAME, f'Could not prepare a request for Form: {error}')
    return None


def get_agent_task_answers_by_id(platform_access: PlatformAccess, agent_task_id: int,
                                 board_id: int, element_id: int,
                                 agent_data_id: int) -> Optional[Dict]:
    """
    Returns JSON from the given AgentDataID and AgentTaskID
    :param element_id: an agent task id
    :param board_id: an agent board id
    :param agent_task_id: an agent task id
    :param agent_data_id: an agent data id
    :param platform_access: a platform access
    :return: a dict containing response from the server
    """
    try:
        # Prepare request-data
        url = f'agentdata/{agent_data_id}/agenttasks/' \
              f'{agent_task_id}/boards/{board_id}/elements/{element_id}/answers'
        detail = 'agentTaskElement'
        response = make_request(platform_access=platform_access,
                                http_method='GET',
                                url_postfix=url,
                                detail=detail)
        response.raise_for_status()
        return response.json()
    except ConnectionError as con_err:
        logger.exception(OWN_ADAPTER_NAME, f'Connection error for Form: {con_err}')
    except RequestException as req_excpt:
        logger.exception(OWN_ADAPTER_NAME, f'During getting the data for Form, occurred: '
                                           f'{req_excpt}')
    except KeyError as key_excpt:
        logger.exception(OWN_ADAPTER_NAME, f'Could not find data inside JSON: {key_excpt}')
    except Exception as error:
        logger.exception(OWN_ADAPTER_NAME, f'Could not prepare a request for Form: {error}')
    return None


def get_answer_from_agent_task_answers(agent_task_answers: Dict, answer_index: int) -> List:
    """
    A helper function to return a list of answers for a given index of a question
    :param agent_task_answers: a dict containg AgentTaskAnswers object
    :param answer_index: an index of a question you want to find answers for
    :return: a list with answers
    """
    answers = []
    for question in agent_task_answers['input']['indexedInputFields']:
        if question['index'] == answer_index:
            for answer in question['inputElementAnswers']:
                if 'agentTaskTextboxAnswer' in answer:
                    if answer['agentTaskTextboxAnswer']:
                        if answer.get('agentTaskTextboxAnswer', {}).get('answer', None):
                            answers.append(answer['agentTaskTextboxAnswer']['answer'])
                elif 'agentTaskQuestionAnswers' in answer:
                    for sub_answer in answer['agentTaskQuestionAnswers']:
                        if sub_answer.get('questionAnswer', {}).get('answer', None):
                            answers.append(sub_answer['questionAnswer']['answer'])
    return answers


def upload_agent_task(platform_access: PlatformAccess, agent_data_id: int,
                      agent_task: Dict) -> Optional[Dict]:
    """
    Upload an agent task

    :param agent_task: an agent task
    :param agent_data_id: an id of an agent_data
    :param platform_access: a platform access
    :return: a dict containing response from the server
    """
    try:
        # Prepare request data for retrieving Input
        detail = 'agentTaskConfiguration'
        url = f'agentdata/{agent_data_id}/agenttasks/configuration'
        response = make_request(platform_access=platform_access,
                                http_method='POST',
                                url_postfix=url,
                                data=agent_task,
                                detail=detail)
        response.raise_for_status()
        logger.debug(OWN_ADAPTER_NAME, 'Form-request data has been successfully retrieved).')
        return response.json()
    except HTTPError as http_error:
        logger.exception(OWN_ADAPTER_NAME, f'HTTPError: {http_error}')
    except ConnectionError as con_err:
        logger.exception(OWN_ADAPTER_NAME, f'Connection error for {url}: {con_err}')
    except RequestException as req_excpt:
        logger.exception(OWN_ADAPTER_NAME, f'During getting the data from {url}, '
                                           f'{req_excpt.__class__} occurred: {req_excpt}')
    except Exception as error:
        logger.exception(OWN_ADAPTER_NAME, f'Could not retrieve data from {url}: {error}')
    return None


def upload_changed_agent_task(platform_access: PlatformAccess, agent_data_id: int,
                              agent_task: Dict) -> Optional[Dict]:
    """
    Update an agent task

    :param agent_task: New AgentTask's data
    :param agent_data_id: an id of agent_data
    :param platform_access: a platform access

    :return: Complete updated AgentTask if request was successful, otherwise None
    """
    try:
        # Prepare request data for retrieving Input
        detail = 'agentTaskConfiguration'
        url = f'agentdata/{agent_data_id}/agenttasks/configuration'
        response = make_request(platform_access=platform_access,
                                http_method='PUT',
                                url_postfix=url,
                                data=agent_task,
                                detail=detail)
        logger.debug(OWN_ADAPTER_NAME, 'Form-request data has been successfully retrieved).')
        response.raise_for_status()
        return response.json()
    except ConnectionError as con_err:
        logger.exception(OWN_ADAPTER_NAME, f'Connection error for {url}: {con_err}')
    except RequestException as req_excpt:
        logger.exception(OWN_ADAPTER_NAME, f'During getting the data from {url}, '
                                           f'{req_excpt.__class__} occurred: {req_excpt}')
    except Exception as error:
        logger.exception(OWN_ADAPTER_NAME, f'Could not retrieve data from {url}: {error}')
    return None


def upload_or_update_agent_task_from_file(platform_access: PlatformAccess,
                                          agent_data_id: int, file_name: str,
                                          force_update: bool = False) -> Optional[Dict]:
    """
    Upload or update an agent task

    :param force_update: just post a task without checking for ids
    :param file_name: a file containing an agent task, file name should be relative to services path
    :param agent_data_id: an id of agent_data
    :param platform_access: a platform access
    :return: a dict containing response from the server
    """
    file_location = os.path.join(AGENTS_SERVICES_PATH, file_name)
    try:
        with open(file_location, 'r') as file:
            agent_task = json.load(file)

    except Exception as error:
        logger.exception(OWN_ADAPTER_NAME, f'Could not get an agent task from file {file_location}. '
                                           f'Exception: {error}')
        return None
    if not force_update and 'agentTask' in agent_task and 'id' in agent_task['agentTask']:
        response = upload_changed_agent_task(platform_access=platform_access,
                                             agent_task=agent_task,
                                             agent_data_id=agent_data_id)
    else:
        response = upload_agent_task(platform_access=platform_access,
                                     agent_task=agent_task,
                                     agent_data_id=agent_data_id)

    if response and 'agentTask' in response:
        if 'agentTasks' in response['agentTask']['agentData']:
            response['agentTask']['agentData'].pop('agentTasks', None)

        agent_input = response['agentTask'].get('input', {}).get('indexedInputFields')
        if agent_input:
            response['agentTask']['input']['indexedInputFields'].sort(key=lambda k:
                                                                      k['index'] if 'index' in k else k['id'])
        with open(file_location, 'w') as file:
            json.dump(response, file, indent=2)

    return response


def remove_agent_task_by_id(platform_access: PlatformAccess, agent_task_id: int,
                            agent_data_id: int = None) -> Optional[Response]:
    """
    Removes AgentTask by the given IDs if it persist on the back-end
    :param platform_access:
    :param agent_data_id:
    :param agent_task_id:
    :return: Response from delete-request
    """
    try:
        # Prepare request-data
        url = f'agentdata/{agent_data_id}/agenttasks/{agent_task_id}'
        detail = 'agentTaskConfiguration'
        response = make_request(platform_access=platform_access,
                                http_method='DELETE',
                                url_postfix=url,
                                detail=detail)
        response.raise_for_status()
        return response
    except ConnectionError as con_err:
        logger.exception(OWN_ADAPTER_NAME, f'Connection error for Form: {con_err}')
    except RequestException as req_excpt:
        logger.exception(OWN_ADAPTER_NAME, f'During getting the data for Form, occurred: '
                                           f'{req_excpt}')
    except KeyError as key_excpt:
        logger.exception(OWN_ADAPTER_NAME, f'Could not find data inside JSON: {key_excpt}')
    except Exception as error:
        logger.exception(OWN_ADAPTER_NAME, f'Could not prepare a request for Form: {error}')
    return None


def update_agent_task_by_id(platform_access: PlatformAccess, agent_data_id: int, agent_task_id: int, task_file_name: str = '') -> Optional[Dict]:
    """
    Updates agent task with given ID
    :param platform_access:
    :param agent_task_id:
    :param agent_task_data:
    :return: response or nothing
    """
    if not task_file_name:
        return None
    file_location = os.path.join(AGENTS_SERVICES_PATH, task_file_name)
    try:
        with open(file_location, 'r') as file:
            agent_task = json.load(file)
    except Exception as e:
        logger.exception(OWN_ADAPTER_NAME, f'Could not get an agent task from file {file_location}. Exception: {e}')
        return None

    try:
        # Prepare request data for retrieving Input...
        detail = 'agentTaskConfiguration'
        url = compose_path('agentdata', agent_data_id, 'agenttasks', agent_task_id, 'configuration')
        response = make_request(platform_access=platform_access,
                                http_method='PUT',
                                url_postfix=url,
                                data=agent_task,
                                detail=detail)
        logger.debug(OWN_ADAPTER_NAME, 'Form-request data has been successfully updated).')

        response.raise_for_status()

        response_data = response.json()
        if response_data and 'agentTask' in response_data:
            agent_data = response_data['agentTask'].get('agentData')
            if 'agentTasks' in agent_data:
                response_data['agentTask']['agentData'].pop('agentTasks', None)

            agent_input = response_data['agentTask'].get('input', {}).get('indexedInputFields')
            if agent_input:
                response_data['agentTask']['input']['indexedInputFields'].sort(key=lambda k:
                                                                               k['index'] if 'index' in k else k['id'])
            with open(file_location, 'w') as file:
                json.dump(response_data, file, indent=2)

        return response_data

    except HTTPError as http_err:
        logger.exception(OWN_ADAPTER_NAME, f'HTTP error ({http_err}) while making request')
    except ConnectionError as con_err:
        logger.exception(OWN_ADAPTER_NAME, f'Connection error for {url}: {con_err}')
    except RequestException as req_excpt:
        logger.exception(OWN_ADAPTER_NAME, f'During getting the data from {url}, {req_excpt.__class__} occurred:'
                                           f' {req_excpt}')
    except Exception as e:
        logger.exception(OWN_ADAPTER_NAME, f'Could not retrieve data from {url}: {e}')
    return None
