"""
REST-API for Jokes-agent.
"""
from http import HTTPStatus
from typing import Tuple

import flask
from flask import Flask
from flask import jsonify

from agents.base_agent_api import AgentAPI
from agents.jokes.apis.icanhazdadjoke import get_search_joke, get_random_joke
from agents.jokes.constants import *
from utils import logger as logger

APP = Flask(__name__)


class JokesAgentAPI(AgentAPI):
    """
    Agent API for Jokes-agent.
    """

    def __init__(self, name: str, app):
        super().__init__(name, app)
        app.add_url_rule('/', view_func=self.find_jokes, methods=['POST'])

    def find_jokes(self) -> Tuple:
        """
        Uses http://webknox.com/api for retrieving jokes.
        :return: A tuple with retrieved joke and status code.
        """
        query = ''
        result = {}
        try:
            # === Get the input parameters ===
            query = flask.request.form.get(REQ_QUERY_KEY, None)
            if not query:
                result = get_random_joke()
                return flask.make_response(jsonify(result), HTTPStatus.OK)

            result = get_search_joke(term=query)
            return flask.make_response(jsonify(result), HTTPStatus.OK)

        except ConnectionError as conn_err:
            logger.exception(JOKES_AGENT_NAME,
                             f'Connection error while retrieving the results: {conn_err}')
        except TimeoutError as timeout_err:
            logger.exception(JOKES_AGENT_NAME,
                             f'Timeout while retrieving the results: {timeout_err}')
        except Exception as excpt:
            logger.exception(JOKES_AGENT_NAME,
                             f'API error for \'{query}\'. Exception message: {excpt}')

            return flask.make_response(jsonify(result), HTTPStatus.INTERNAL_SERVER_ERROR)

        return flask.make_response(jsonify(result), HTTPStatus.OK)


if __name__ == '__main__':
    JokesAgentAPI(JOKES_AGENT_NAME, APP).start()
