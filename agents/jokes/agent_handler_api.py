"""
REST-API router for Jokes-agent
"""
from flask import Flask

from agents.base_agent_handler_api import AgentHandlerAPI
from agents.jokes.constants import JOKES_AGENT_NAME

app = Flask(__name__)


class JokesAgentHandlerAPI(AgentHandlerAPI):
    """
    Jokes-agent handler API implementation.
    """

    def __init__(self, name: str, app):
        super().__init__(name, app)
        app.add_url_rule('/', view_func=self.default_handler_to_transfer_request_to_agent,
                         methods=['POST'])


if __name__ == '__main__':
    JokesAgentHandlerAPI(JOKES_AGENT_NAME, app).start()
