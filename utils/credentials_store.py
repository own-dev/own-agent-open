"""
Class to access credentials stored in Firestore
"""
import datetime
import os
from typing import Optional, Tuple, Dict

import pytz
import requests
from firebase_admin import firestore
from google.cloud.firestore_v1beta1 import DocumentSnapshot, Transaction, DocumentReference

from agents.agents_utils.utils_constants import AGENT_UTILS_NAME
from utils import logger
from utils.cloud_firestore_communication import Firestore

NAME_KEY = 'name'
LIMITED_UNTIL_KEY = 'limitedUntil'
LIMIT_PERIOD_KEY = 'limitPeriod'
IN_USE_KEY = 'inUse'
USED_BY_KEY = 'usedBy'
VALUE_KEY = 'value'
CREDENTIALS_APIS = ['epo', 'twitter', 'news']


def set_in_use_parameters_to_false():
    """
    Used to check all inUse parameters and set them to False
    :return: Nothing
    """

    def ping_agent_ip(ip: str) -> bool:
        """
        Pings an agent instance
        :param ip: an ip address of an agent with port for request
        :return: True if the request was successful, false otherwise
        """
        response = None
        try:
            response = requests.get(f'{ip}/ping')
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(f'Could not ping agent instance {ip}. Error {e}', response)
            return False
        return True

    credentials_key = os.environ['CREDENTIALS_DB_KEY']

    credential_db = Firestore(credentials_key)
    for api in CREDENTIALS_APIS:
        for doc in credential_db.db.collection(api).get():
            content = credential_db.get_doc_content(doc.reference)
            if content[IN_USE_KEY]:
                if not ping_agent_ip(content.get(USED_BY_KEY)):
                    credential_db.update_document(doc.reference, {IN_USE_KEY: False,
                                                                  USED_BY_KEY: None})


class CredentialsStore(Firestore):
    """
    Class for credentials management
    """

    def __init__(self, service_name: str):
        """
        Initialise a store
        :param service_name: a name of a service for which credentials are needed
        """
        try:
            credentials_key = os.environ['CREDENTIALS_DB_KEY']
        except KeyError as e:
            logger.error(AGENT_UTILS_NAME, f'CREDENTIALS_DB_KEY is undefined. Error message: {e}')
            raise Exception(f'CREDENTIALS_DB_KEY is undefined')
        super().__init__(credentials_key)
        self.db = self.db.collection(service_name)

    def get_credentials_for_service(self, used_by_id: str = '') -> Optional[Tuple[str, Dict]]:
        """
        Get an API credentials for a 3rd party service. Mark it as used
        
        You would need to create an index for each new service in Firestore
        :param used_by_id: ip address of agent which get credentials
        :return: id of credentials, credentials values
        """
        credentials_query = self.db \
            .where(LIMITED_UNTIL_KEY, '<=', datetime.datetime.now(pytz.UTC)) \
            .where(IN_USE_KEY, '==', False) \
            .limit(1)
        credentials_obj = [key for key in credentials_query.get()]

        if not credentials_obj:
            return None

        credentials_obj: DocumentSnapshot = credentials_obj[0]
        query_transaction = self.firestore.transaction()

        @firestore.transactional
        def update_in_transaction(transaction: Transaction, doc_ref: DocumentReference):
            credentials_doc = doc_ref.get(transaction=transaction)
            transaction.update(doc_ref, {
                IN_USE_KEY: True,
                USED_BY_KEY: used_by_id
            })

            return credentials_doc.id, credentials_doc.to_dict()[VALUE_KEY]

        try:
            return update_in_transaction(query_transaction, credentials_obj.reference)
        except Exception as e:
            logger.warning(AGENT_UTILS_NAME, f'Failed to update credentials in transaction. Error {e}')
            return None

    def release_credentials_for_service(self, credentials_id: str):
        """
        Make credentials available for usage
        :param credentials_id: an id of credentials
        :return: Nothing
        """
        self.db.document(credentials_id).update({
            IN_USE_KEY: False
        })

    def limit_credentials_for_service_usage(self, credentials_id: str):
        """
        Limit credentials usage for a period of time
        :param credentials_id: an id of the key
        :return: Nothing
        """
        credentials_ref = self.db.document(credentials_id)
        limit_period = credentials_ref.get().to_dict()[LIMIT_PERIOD_KEY]
        limited_until = datetime.datetime.now(pytz.UTC) + datetime.timedelta(seconds=limit_period)
        credentials_ref.update({
            LIMITED_UNTIL_KEY: limited_until,
        })
