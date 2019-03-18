"""
Code to restore important documents in Firestore:
>> AvailableAgentPorts
>> AvailableAgentHandlerPorts
>> credentials_{test/production} (can also be used to add new credentials easily)

For credentials: create file with credentials values.
"""

import copy
import datetime
import os

from utils import logger
from utils.cloud_firestore_communication import Firestore
from utils.constants import AVAILABLE_AGENT_HANDLER_PORTS, PORTS_KEY, AVAILABLE_AGENT_PORTS, UTILS
from utils.credentials_store import IN_USE_KEY, LIMIT_PERIOD_KEY, LIMITED_UNTIL_KEY, USED_BY_KEY, VALUE_KEY

MIN_AGENT_PORT = 8200
MIN_HANDLER_PORT = 8100
NUMBER_OF_AGENT_PORTS = 20
NUMBER_OF_HANDLER_PORTS = 21
SIZE_OF_TWITTER_CREDENTIALS_KIT = 4
SIZE_OF_EPO_CREDENTIALS_KIT = 3
TWITTER_TIME_BETWEEN_REQUESTS = 500000
EPO_TIME_BETWEEN_REQUESTS = 7000000
TWITTER_KEY = 'twitter'
EPO_KEY = 'epo'

credentials_doc = {IN_USE_KEY: False,
                   LIMIT_PERIOD_KEY: 60,
                   LIMITED_UNTIL_KEY: datetime.datetime.now() - datetime.timedelta(days=1),
                   USED_BY_KEY: ''}

CUSTOMER_ID_KEY = 'customer_id'
SECRET_API_KEY = 'secret_api'
ACCESS_TOKEN_SECRET_KEY = 'access_token_secret'
ACCESS_TOKEN_KEY = 'access_token'
TIME_BETWEEN_REQUESTS_KEY = 'time_between_requests'

APP_NAME_KEY = 'epo_org_app_name'
CONSUMER_KEY = 'epo_org_consumer_key'
SECRET_KEY = 'epo_org_secret_key'

db = Firestore('')


def create_agent_ports_doc():
    """
    Adds document with agent ports to Firebase
    :return:nothing
    """
    ports = [MIN_AGENT_PORT + i for i in range(NUMBER_OF_AGENT_PORTS)]
    ports = {PORTS_KEY: ports}
    doc_ref = db.common_db.document(AVAILABLE_AGENT_PORTS + '_test')
    doc_ref.set(ports)
    return doc_ref


def create_handler_ports_doc():
    """
    Adds document with handler ports to Firebase
    :return: nothing
    """
    ports = [MIN_HANDLER_PORT + i for i in range(NUMBER_OF_HANDLER_PORTS)]
    ports = {PORTS_KEY: ports}
    doc_ref = db.common_db.document(AVAILABLE_AGENT_HANDLER_PORTS + '_test')
    doc_ref.set(ports)
    return doc_ref


def create_twitter_credentials_doc(credentials_file_path: str):
    """
    Adds document with credentials(if it doesn't exists), adds twitter credentials collection (if it doesn't exist)
    adds credentials to twitter collection
    :param credentials_file_path: file with credentials that need to be created:
    place all values in this order:
        #first twitter credentials kit
        access_token (1)
        acces_token_secret (1)
        customer_id (1)
        ecret_api (1)
        #second twitter credentials kit
        access_token (2)
        acces_token_secret (2)
        customer_id (2)
        ecret_api (2)
        ...
    :return: nothing
    """
    credentials_key = os.environ['CREDENTIALS_DB_KEY'] + '_test'
    credentials_dict = copy.deepcopy(credentials_doc)
    if not os.path.isfile(credentials_file_path):
        logger.exception(UTILS, f'Wrong credentials file path: {credentials_file_path}')
        return None
    with open(credentials_file_path) as file:
        credentials_str = file.read()
        credentails_list = credentials_str.split('\n')
    for i in range(0, len(credentails_list), SIZE_OF_TWITTER_CREDENTIALS_KIT):
        credentials_kit = credentails_list[i:i + SIZE_OF_TWITTER_CREDENTIALS_KIT]
        credentials_value = {ACCESS_TOKEN_KEY: credentials_kit[0],
                             ACCESS_TOKEN_SECRET_KEY: credentials_kit[1],
                             CUSTOMER_ID_KEY: credentials_kit[2],
                             SECRET_API_KEY: credentials_kit[3],
                             TIME_BETWEEN_REQUESTS_KEY: TWITTER_TIME_BETWEEN_REQUESTS}
        credentials_dict[VALUE_KEY] = credentials_value
        db.common_db.document(credentials_key).collection(TWITTER_KEY).add(credentials_dict)


def create_epo_credentials_doc(credentials_file_path: str):
    """
    Adds doc with credentials(if it doesn't exists), adds epo credentials collection (if it doesn't exist)
    adds credentials to twitter collection
    :param credentials_file_path: file with credentials that need to be created:
    place all values in this order:
        # first epo credentials kit
        epo_org_app_name(1)
        epo_org_consumer_key(1)
        epo_org_secret_key(1)
        #second epo credentials kit
        epo_org_app_name(2)
        epo_org_consumer_key(2)
        epo_org_secret_key(2)
        ...
    :return: nothing
    """
    credentials_key = os.environ['CREDENTIALS_DB_KEY']
    credentials_dict = copy.deepcopy(credentials_doc)
    if not os.path.isfile(credentials_file_path):
        logger.exception(UTILS, f'Wrong credentials file path: {credentials_file_path}')
        return None
    with open(credentials_file_path) as file:
        credentials_str = file.read()
        credentails_list = credentials_str.split('\n')
    for i in range(0, len(credentails_list), SIZE_OF_EPO_CREDENTIALS_KIT):
        credentials_kit = credentails_list[i:i + SIZE_OF_EPO_CREDENTIALS_KIT]
        credentials_value = {APP_NAME_KEY: credentials_kit[0],
                             CONSUMER_KEY: credentials_kit[1],
                             SECRET_KEY: credentials_kit[2],
                             TIME_BETWEEN_REQUESTS_KEY: EPO_TIME_BETWEEN_REQUESTS}
        credentials_dict[VALUE_KEY] = credentials_value
        db.common_db.document(credentials_key).collection(EPO_KEY).add(credentials_dict)
