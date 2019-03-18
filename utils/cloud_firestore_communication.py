"""
Method to access Cloud Firestore
"""
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

import firebase_admin
import pytz
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1beta1 import DocumentReference, DocumentSnapshot, Transaction

from utils import logger
from utils.constants import *


def get_cloud_firestore_db():
    """
    Get an instance of cloud firestore db
    :return: the instance
    """
    google_cloud_project_name = None
    try:
        google_cloud_project_name = os.environ[f'GOOGLE_CLOUD_PROJECT_NAME']
    except KeyError as e:
        logger.error(UTILS, f'GOOGLE_CLOUD_PROJECT_NAME environment variable is not set up,'
        f' or the project by the given name was not set up correctly.')

    ops = {
        'databaseURL': f'https://{google_cloud_project_name}.firebaseio.com',
        'projectId': f'{google_cloud_project_name}'
    }
    if not len(firebase_admin._apps):
        firebase_admin.initialize_app(options=ops)

    return firestore.client()


class Firestore:
    """
    A base service to communicate with DB
    """

    def __init__(self, collection_key: str):
        """
        Initialise DB connection
        :param collection_key: a key to collection in DB
        """
        self.firestore = get_cloud_firestore_db()
        self.common_db = self.firestore.collection(AGENTS_PLATFORM_KEY)
        self.db = self.common_db.document(collection_key)

    def get_available_agent_ports(self) -> List[int]:
        """
        Get available ports for agents to run on
        :return: a list of ports
        """
        return self.common_db.document(AVAILABLE_AGENT_PORTS).get().to_dict()[PORTS_KEY]

    def get_available_agent_handler_ports(self) -> List[int]:
        """
        Get available ports for agent handlers to run on
        :return: a list of ports
        """
        return self.common_db.document(AVAILABLE_AGENT_HANDLER_PORTS).get().to_dict()[PORTS_KEY]

    def get_all_agent_handlers(self) -> List[Tuple[str, Dict]]:
        """
        Get all agent handlers for this agent 
        :return: List of handler id, handler info
        """
        return [(doc.id, doc.to_dict()) for doc in self.db.collection(AGENT_HANDLERS).get()]

    def get_least_busy_agent_handler(self) -> Optional[Tuple[str, Dict]]:
        """
        Get an agent handler with a least number of agents associated to it
        :return: an agent handler id and its info
        """
        res = [(doc.id, doc.to_dict())
               for doc in self.db.collection(AGENT_HANDLERS).order_by(AGENT_HANDLER_NUM_AGENTS_KEY).limit(1).get()]
        return res[0] if res else None

    def increase_handler_number_of_fails(self, handler_id: str):
        """
        Increase number of times handler did not respond
        :return: Nothing
        """
        try:
            handler_ref = self.db.collection(AGENT_HANDLERS).document(handler_id)
        except Exception as e:
            logger.info(UTILS, f'Handler is already deleted. Error {e}')
            return None
        query_transaction = self.firestore.transaction()

        @firestore.transactional
        def update_in_transaction(transaction: Transaction, doc_ref: DocumentReference):
            try:
                current_num_of_fails = doc_ref.get(transaction=transaction).get(AGENT_HANDLER_NUM_FAILS_KEY)
            except Exception as e:
                logger.info(UTILS, f'Handler is already deleted. Error {e}')
                return None

            if current_num_of_fails >= MAX_NUMBER_OF_HANDLER_FAILS:
                transaction.delete(doc_ref)
            else:
                transaction.update(doc_ref, {
                    AGENT_HANDLER_NUM_FAILS_KEY: current_num_of_fails + 1,
                })

        update_in_transaction(query_transaction, handler_ref)

    def get_agent_handler_with_least_amount_of_tasks(self, black_list: List[str]) -> Optional[Tuple[str, Dict]]:
        """
        Get an agent handler with a least number of tasks running on it
        :param black_list: a list of ids of handler which are not suitable
        :return: an agent handler id and its info
        """
        res = [(doc.id, doc.to_dict())
               for doc in self.db.collection(AGENT_HANDLERS).order_by(AGENT_HANDLER_NUM_TASKS_KEY).limit(
                1 + len(black_list)).get()]

        if not res:
            return None

        for handler in res:
            if handler[0] not in black_list:
                return handler

    def get_agent_handler(self, handler_id: str) -> Dict:
        """
        Get all agent handlers for this agent 
        :return: handler
        """
        try:
            return self.db.collection(AGENT_HANDLERS).document(handler_id).to_dict()
        except Exception as e:
            logger.warning(UTILS, f'Doc with id {handler_id} was not found in Firestore. Exception {e}')
            return {}

    def get_agent_feature(self) -> Dict:
        """
        Get agent feature
        :return: agent feature
        """
        try:
            return self.db.collection(AGENT_FEATURES).document(AGENT_FEATURES).get().to_dict()
        except Exception as e:
            logger.warning(UTILS, f'Feature document was not found in Firestore. Exception {e}')
            return {}

    def add_new_agent_handler(self, address: str) -> Tuple[str, Dict]:
        """
        Add new agent handler to db
        :return: an id of the handler
        """
        doc = self.db.collection(AGENT_HANDLERS).add({
            AGENT_HANDLER_ADDRESS_KEY: address,
            AGENT_HANDLER_NUM_AGENTS_KEY: 0,
            AGENT_HANDLER_NUM_TASKS_KEY: 0,
            AGENT_HANDLER_MAX_TASKS_KEY: 10,
            AGENT_HANDLER_NUM_FAILS_KEY: 0,
        })[1].get()
        return doc.id, doc.to_dict()

    def change_number_of_agents_in_agent_handler(self, handler_id: str, number_of_agents: int) -> None:
        """
        Change a number of agents in an agent handler
        :return: Nothing
        """
        try:
            self.db.collection(AGENT_HANDLERS).document(handler_id).update({
                AGENT_HANDLER_NUM_AGENTS_KEY: number_of_agents,
            })
        except Exception as e:
            logger.exception(UTILS, f'Could not update number of agents in'
            f' agent handler {handler_id}. Error {e}')

    def change_number_of_tasks_in_agent_handler(self, handler_id: str, number_of_tasks: int) -> None:
        """
        Change a number of tasks in an agent handler
        :return: Nothing
        """
        try:
            self.db.collection(AGENT_HANDLERS).document(handler_id).update({
                AGENT_HANDLER_NUM_TASKS_KEY: number_of_tasks,
            })
        except Exception as e:
            logger.exception(UTILS, f'Could not update number of tasks in'
            f' agent handler {handler_id}. Error {e}')

    def delete_agent_handler(self, handler_id: str) -> None:
        """
        Delete an agent handler by id 
        :param handler_id: an id of the handler
        :return: Nothing
        """
        try:
            self.db.collection(AGENT_HANDLERS).document(handler_id).delete()
        except Exception as e:
            logger.warning(UTILS, f'An error while deleting agent handler {handler_id}. Error {e}')

    def create_new_doc_for_task(self, board_identifier: str, element_id: str, query_id: str, task_name: str,
                                update_period: int, constant_monitoring: bool = False,
                                agent_task: Dict = None) -> DocumentReference:
        """
        Create a new document to handle information necessary for an agent task execution
        :param agent_task: an agent task info
        :param update_period: time in seconds for periodical update of the task
        :param query_id: an id of agent task query
        :param element_id: an id of an element where agent task was called
        :param task_name: a name of the task
        :param constant_monitoring: if this requires constant monitoring
        :param board_identifier: a board identifier to post a message
        :return: reference to the document
        """
        doc_ref = self.db.collection(AGENT_TASKS_KEY).document()
        doc_ref.set({
            TASK_NAME_KEY: task_name,
            BOARD_IDENTIFIER_KEY: board_identifier,
            ELEMENT_ID_KEY: element_id,
            QUERY_ID_KEY: query_id,
            MESSAGES_KEY: [],
            CONSTANT_MONITORING_KEY: constant_monitoring,
            LISTENER_SET_KEY: True,
            WORKER_SET_KEY: True,
            LAST_MESSAGE_READ_KEY: 0,
            UPDATE_PERIOD_KEY: update_period,
            TIME_TO_UPDATE_KEY: datetime.now(pytz.UTC) + timedelta(seconds=update_period),
            AGENT_TASK_KEY: agent_task,
            UPDATING_KEY: False,
        })
        return doc_ref

    def delete_old_agent_tasks(self, element_id: str, board_id: Optional[int] = None):
        """
        Delete agent task which where previously run on an element
        :param board_id: an id of a board where agent task was called
        :param element_id: an id of an element where agent task was called
        :return: Nothing
        """
        if element_id:
            for doc in self.db.collection(AGENT_TASKS_KEY).where(ELEMENT_ID_KEY, '==', element_id).get():
                doc.reference.delete()
        elif board_id:
            for doc in self.db.collection(AGENT_TASKS_KEY).where(BOARD_IDENTIFIER_KEY, '==', board_id).get():
                doc.reference.delete()

    def get_agent_task_from_firestore(self, task_name: str, runners_dict: Dict, listener: bool = None,
                                      worker: bool = None, update=None,
                                      constant_monitoring: bool = True) \
            -> Optional[DocumentReference]:
        """
        Return a task by a name which should be run by agent
        :param runners_dict: a dict to store doc references and clear them on process exit
        :param update: find a task for update
        :param constant_monitoring: whether a task is a constant monitoring one
        :param worker: if a task asked for worker
        :param listener: if a task asked for listener
        :param task_name: a name of an agent task to get
        :return: a document reference of this task
        """
        field_name = None
        if listener:
            field_name = LISTENER_SET_KEY
        if worker:
            field_name = WORKER_SET_KEY
        if update:
            field_name = UPDATING_KEY
        if not field_name:
            raise Exception('Either listener, worker or update param should be set for get_constant_monitoring_task')

        query_transaction = self.firestore.transaction()

        while True:
            if listener:
                #  We don't need to check TIME_TO_UPDATE_KEY here, as listener should check for new messages
                #  independently of that parameter
                task = [
                    doc for doc in self.db.collection(AGENT_TASKS_KEY)
                        .where(TASK_NAME_KEY, '==', task_name)
                        .where(CONSTANT_MONITORING_KEY, '==', constant_monitoring)
                        .where(MESSAGES_KEY, '>', [])
                        .where(field_name, '==', False)
                        .limit(1).get()
                ]
            else:
                task = [
                    doc for doc in self.db.collection(AGENT_TASKS_KEY)
                        .where(TASK_NAME_KEY, '==', task_name)
                        .where(CONSTANT_MONITORING_KEY, '==', constant_monitoring)
                        .where(TIME_TO_UPDATE_KEY, '<=', datetime.now(pytz.UTC))
                        .where(field_name, '==', False)
                        .limit(1).get()
                ]

            if not task:
                return None
            task_ref: DocumentSnapshot = task[0]

            @firestore.transactional
            def update_in_transaction(transaction: Transaction, doc_ref: DocumentReference):
                already_processed = doc_ref.get(transaction=transaction).to_dict()[field_name]
                if already_processed:
                    return None

                transaction.update(doc_ref, {
                    field_name: True
                })
                runners_dict[doc_ref.id] = doc_ref
                return doc_ref

            res = update_in_transaction(query_transaction, task_ref.reference)
            if res:
                return res

    def finish_monitoring_task(self, doc_ref: DocumentReference, listener: bool = None,
                               worker: bool = None, update: bool = None):
        """
        Set proper keys after finishing work with a task
        :param update: set update key to false
        :param worker: release a task from worker
        :param listener: release a task from listener
        :param doc_ref: a reference to the document
        :return: Nothing
        """
        try:
            if not listener:
                doc_ref.update({
                    TIME_TO_UPDATE_KEY: datetime.now(pytz.UTC) +
                                        timedelta(seconds=doc_ref.get().to_dict()[UPDATE_PERIOD_KEY])
                })
            if listener:
                doc_ref.update({
                    LISTENER_SET_KEY: False,
                })
            if worker:
                doc_ref.update({
                    WORKER_SET_KEY: False,
                })
            if update:
                doc_ref.update({
                    UPDATING_KEY: False,
                })
        except Exception as e:
            # Document doesn't exist
            logger.warning(UTILS, f'Unsuccessful finish to task monitoring. Error: {e}')
            return None

    def get_task_doc_ref_by_id(self, doc_id: str) -> DocumentReference:
        """
        Return a document reference of document by its id and task name
        :param doc_id: an id of the document
        :return: a reference to the document
        """
        return self.db.collection(AGENT_TASKS_KEY).document(doc_id)

    def get_doc_content(self, doc_ref: DocumentReference) -> Optional[Dict]:
        """
        Return a dict with values from a Firestore document
        :param doc_ref: a reference to the document
        :return: the dict
        """
        try:
            return doc_ref.get().to_dict()
        except Exception as e:
            # Document doesn't exist
            return None

    def update_document(self, doc_ref: DocumentReference, update_dict: Dict):
        """
        Update a Firestore document
        :param doc_ref: a reference to the document
        :param update_dict: a dict with keys to be created/updated and values for them
        :return: Nothing
        """
        doc_ref.update(update_dict)

    def add_new_message_to_doc_ref(self, agent_task_doc_ref: DocumentReference, message: str):
        """
        Add a message to agentTask document
        :param agent_task_doc_ref: a reference to the document
        :param message: a message to add
        :return: Nothing
        """
        query_transaction = self.firestore.transaction()

        @firestore.transactional
        def update_in_transaction(transaction: Transaction, doc_ref: DocumentReference):
            content = doc_ref.get(transaction=transaction).to_dict()
            messages = content[MESSAGES_KEY]
            messages.append({
                INDEX_KEY: max(content[LAST_MESSAGE_READ_KEY] + 1, messages[-1][INDEX_KEY] + 1 if messages else 0),
                MESSAGE_KEY: message,
            })
            transaction.update(doc_ref, {
                MESSAGES_KEY: messages,
            })

        try:
            update_in_transaction(query_transaction, agent_task_doc_ref)
        except Exception as e:
            #  This is only a warning, as usually it happens when doc was deleted while running
            #  two same tasks in parallel
            logger.warning(UTILS, f'Failed to add new messages. Error: {e}')

    def get_lambda_to_put_message_on_board(self, doc_ref: DocumentReference):
        """
        Get a function to put a message to a specified document. It will be posted on a board by listener from
        service side
        :param doc_ref: a reference to the document
        
        :return: the function
        """
        return lambda message, db=self, agent_doc_ref=doc_ref: db.add_new_message_to_doc_ref(agent_doc_ref, message)

    def delete_doc(self, doc_ref: DocumentReference):
        """
        Deletes a document from Firestore
        :param doc_ref: a reference to the document
        :return: Nothing
        """
        try:
            doc_ref.delete()
        except Exception as e:
            logger.exception(UTILS, f'Error while trying to delete document. Error {e}')

    def get_doc_id(self, doc_ref: DocumentReference) -> str:
        """
        Get an if of a document from Firestore
        :param doc_ref: a reference to the document
        :return: the id
        """
        return doc_ref.id

    def get_current_content_and_update(self, doc_ref: DocumentReference, values: Dict):
        """
        Method for getting a content of a document and updating it with new values.
        :param doc_ref: reference on document to update
        :param values: dict with values to update
        :return: initial content of a document
        """

        query_transaction = self.firestore.transaction()

        @firestore.transactional
        def update_doc_in_transaction(transaction, doc_ref):
            """
            Method for update document
            :param transaction: transaction to transactional update\
            :param doc_ref: reference to a document to update
            :return: initial doc content
            """
            doc_content = doc_ref.get(transaction=transaction).to_dict()
            transaction.update(doc_ref, values)
            return doc_content

        return update_doc_in_transaction(query_transaction, doc_ref)

    def get_content_from_snapshot(self, doc: DocumentSnapshot) -> Dict:
        """
        Method for getting document content from snapshot of document
        :param doc: Snapshot of document
        :return: dict with document's content
        """
        return doc.to_dict()

### CODE TO TRANSFER TASKS TO NEW STRUCTURE, DELETE IT WHEN TASKS ARE TRANSFERED IN PRODUCTION

# doc_names = ['company_test_ihar']
# task_names = ['regional', 'report', 'word_cloud']
# x = get_cloud_firestore_db()
# db: firestore.firestore.CollectionReference = x.collection(AGENTS_PLATFORM_KEY)
# for doc_name in doc_names:
#     tasks = db.document(doc_name).collection(AGENT_TASKS_KEY)
#     doc = tasks.document(DOC_LAYER_NAME)
#     for task_name in task_names:
#         for task in doc.collection(task_name).where(ELEMENT_ID_KEY, '>=', '').get():
#             task_dict = task.to_dict()
#             if isinstance(task_dict[BOARD_IDENTIFIER_KEY], str):
#                 task_dict[BOARD_IDENTIFIER_KEY] = int(task_dict[BOARD_IDENTIFIER_KEY].split('/')[-1])
#             tasks.document(task.id).set({
#                 TASK_NAME_KEY: task_name,
#                 **task_dict,
#             })
