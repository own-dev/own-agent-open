"""
Provides a basic layer to ICanHazDadJoke-API;
doesn't require any API keys...
Reference: https://icanhazdadjoke.com/api
"""
from random import randrange
from typing import Optional

from requests import get, HTTPError, ConnectionError

from agents.jokes.constants import JOKES_AGENT_NAME, ICHDJ_API_URL, ICHDJ_DEFAULT_HEADERS, \
    ICHDJ_DEFAULT_NUM_JOKES_PER_PAGE
from utils import logger as logger

TERM_KEY = 'term'
PAGE_KEY = 'page'
LIMIT_KEY = 'limit'
JOKE_DATA_KEY = 'joke'


def get_random_joke() -> Optional[str]:
    """
    Retrieves a random joke...
    :return: Retrieved joke if request was successful, otherwise None...
    """
    url = ICHDJ_API_URL
    request_params = {}
    try:
        response = get(url=url, headers=ICHDJ_DEFAULT_HEADERS, params=request_params)
        response.raise_for_status()
    except HTTPError as http_error:
        logger.exception(JOKES_AGENT_NAME,
                         f'Could not retrieve data from server: {http_error}')
        return None
    except ConnectionError as con_error:
        logger.exception(JOKES_AGENT_NAME,
                         f'Connection lost while getting a joke: {con_error}')
        return None

    data = response.json()
    joke = data.get(JOKE_DATA_KEY, None)
    return joke


def get_search_joke(term: Optional[str] = None,
                    page: Optional[int] = None,
                    limit: Optional[int] = None) -> Optional[str]:
    """
    Retrieves a joke on the given query...
    :param term: A query/category/keyword to look upon...
    :param page: A page number to retrieve from; think of a pagination.
     Example: 100 jokes, 20 jokes/per --> 5 pages; to get 21-th joke, get 2-nd page...
    :param limit: Maximum number of jokes to retrieve, server's default is 20...

    :return: Retrieved joke if the request was successful, otherwise None...
    """
    # Compose URL out of the given parameters...
    data = {
        TERM_KEY: term,
        PAGE_KEY: page,
        LIMIT_KEY: limit
    }
    url = f'{ICHDJ_API_URL}/search'
    if data.values():
        url_query = '&'.join([
            f'{key}={val}' for key, val in data.items()
            if val
        ])
        url += f'?{url_query}'

    request_params = None
    try:
        response = get(url=url, headers=ICHDJ_DEFAULT_HEADERS, params=request_params)
        response.raise_for_status()
    except HTTPError as http_error:
        logger.exception(JOKES_AGENT_NAME,
                         f'Could not retrieve data from server: {http_error}')
        return None
    except ConnectionError as con_error:
        logger.exception(JOKES_AGENT_NAME,
                         f'Connection lost while getting a joke: {con_error}')
        return None

    # Get the retrieved jokes...
    data = response.json()
    jokes = data.get('results', [])
    if not jokes:
        return None

    # Randomly choose one of them...
    max_ind = len(jokes) or ICHDJ_DEFAULT_NUM_JOKES_PER_PAGE
    rand_ind = randrange(max_ind - 1)
    joke = jokes[rand_ind].get(JOKE_DATA_KEY, None)

    return joke
