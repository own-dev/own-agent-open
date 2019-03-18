"""
Module for interacting with an operating system
"""

import os

import agents_platform.logger as logger
from agents.agents_helper import get_size_from_path


# Utils
def check_cache_exceeded(name: str, cache_path: str, cache_quota: int) -> None:
    """
    Checks if cache exceeded quota, removes the oldes files if it does (until it fits)
    :param name: logger's name -- look for available names in agents_platform.logger.py
    :param cache_path: path to a cache
    :param cache_quota: cache size quota in Bytes to check for
    :return: None
    """
    while get_size_from_path(cache_path) >= cache_quota:
        # If it exceeds cache quota, remove the oldest file
        sorted_fullpaths = []
        for dirpath, dirnames, filenames in os.walk(cache_path):
            for file in filenames:
                sorted_fullpaths.append(os.path.join(dirpath, file))
        sorted_fullpaths.sort(key=os.path.getctime, reverse=False)
        try:
            os.remove(sorted_fullpaths[0])
            logger.debug(name, f'Removed {sorted_fullpaths[0]} to clear cache a bit.')
        except OSError as error:
            logger.debug(name, f'Couldn\'t remove file [{sorted_fullpaths[0]}]. Error: {error}')
