"""
Jokes-agent's service to work with agents_platform
"""
from http import HTTPStatus
from random import randint
from typing import List, Dict, Optional

import utils.logger as logger
from agents_platform.base_service import AgentService
from agents_platform.own_adapter.agent_task import get_answer_from_agent_task_answers
from agents_platform.own_adapter.element import Element
from agents_platform.services.jokes_service.constants import *


class JokesAgentService(AgentService):
    """Jokes-agent service. Will post random jokes at your will."""

    def __upload_jokes(self, element: Element, query: str) -> Optional[List]:
        """
        Uploads the metadata for the given query
        __it uses REST-API__
        :param query: Query to find jokes about
        :return: Plain or None
        """
        logger.debug(self.name, 'Privately started to upload jokes')

        board = element.get_board()
        if not board:
            logger.error(self.name, f'Couldn\'t get the board of element [{element}].')
            return None

        response = None
        try:
            logger.debug(self.name, f'Connecting to {self.redis_name} via REST for [{query}]')

            self.update_element_caption(element, query)

            # Compose the data to be sent to the agent.
            data = {
                REQ_QUERY_KEY: query,
            }

            # Get the result-data from Jokes-agent's REST-API.
            request_method = 'POST'
            request_flask_endpoint = ''
            jokes_response = self.send_request_to_agent_handler(method=request_method,
                                                                url=request_flask_endpoint,
                                                                params={}, data=data)

            # Check if we get successful response.
            if not jokes_response or jokes_response.status_code != HTTPStatus.OK:
                logger.exception(self.name,
                                 f'Error: upload jokes about {query} failed.'
                                 f' Skipped. Response: {response.status_code if response else None}',
                                 response)
                return None

            # Parse the received data.
            logger.debug(self.name, 'Success. Parsing the data')
            response_data = jokes_response.json()

            # Return the results.
            logger.info(self.name, 'Success, returning the data', response)
            return response_data

        except Exception as excpt:
            logger.exception(self.name, f'Error: upload of query [{query}; {year}] is failed. '
                                        f'Skipped. Error type: {excpt}', response)
            return None

    def get_jokes(self, element: Element, agent_task: Dict) -> Optional[Element]:
        """
        Run on element which requested jokes.

        :param element: own_adapter.element.Element on which Jokes-agent should run.
        :param agent_task: An agent task to get details from.

        :return: Target element or None if something gone wrong
        """
        board = element.get_board()

        # Extract the topic for the joke.
        topic = get_answer_from_agent_task_answers(agent_task, answer_index=1)
        topic = str(topic[0]) if topic else ''

        # Put start-message on the board.
        start_msg = f'Time to find a joke for thee.'
        if topic:
            start_msg += f' "{topic}" you say? Let\'s see...'
        board.put_message(start_msg)

        try:
            # Get the jokes from the agent.
            uploaded_jokes = self.__upload_jokes(element=element, query=topic)
            if not uploaded_jokes:
                # No jokes for you.
                message = f'I could not find any jokes on "{topic}".' \
                    if topic \
                    else 'There are no more jokes in this world.'
                board.put_message(message)
                return None

            # Compose successful report message.
            message = f'"{uploaded_jokes}"'
            # Make a joke in a joke from time to time.
            if randint(-3, 10) < 0:
                prefix = 'I haven\'t found a thing. Just joking, here you go:\n'
                message = prefix + message
            board.put_message(message)

        except AttributeError as attr_err:
            logger.exception(self.name,
                             f'Some attribute was incorrect while running Jokes-agent on element: {attr_err}')
            return None

        return element

    def identify_and_pass_task(self, element: Element, agent_task: Dict,
                               update: bool = False, doc_id: str = None) -> Optional[Element]:
        """
        Identify a task and pass it to appropriate method

        :param element: own_adapter.element.Element on which Jokes-agent should run
        :param agent_task: an agent task to get details from
        :param update: not used here
        :param doc_id: not used here

        :return: Target element
        """
        if not agent_task:
            return None

        agent_task_answers = agent_task['agentTaskElement']['agentTask']
        agent_task_config_id = agent_task_answers['id']

        # Get all the agent-tasks
        possible_files = self.get_agent_tasks_names()

        # Find the AgentTask to run
        for filename in possible_files:
            if self.get_agent_task_config_from_file(filename)['agentTask']['id'] == agent_task_config_id:
                return self.get_jokes(element, agent_task_answers)

        return None
