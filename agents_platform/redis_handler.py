import os

import redis

from utils import logger


def get_redis_connection():
    try:
        address = os.environ['REDIS_ADDRESS']
        port = os.environ['REDIS_PORT']
    except KeyError as e:
        logger.exception('engine',
                         'REDIS_ADDRESS or REDIS_PORT variable is undefined. Error message: {}'.format(str(e)))
        raise Exception('Could not connect to Redis. Needed environment variables are not set.')

    try:
        connection = redis.StrictRedis(host=address, port=port, db=0, decode_responses=True)
        response = connection.client_list()  # execute query to check if redis is connected
    except Exception as e:
        logger.exception('engine', 'Could not connect to Redis. Exception message: {}'.format(str(e)))
        raise Exception('Could not connect to Redis. Please check logs.')
    return connection
