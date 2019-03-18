"""Utils constants"""
# 'production' env var is lead to send logs to google cloud platform
import os

PRODUCTION_ENVIRONMENT = 'production'
GOOGLE_LOGGER_NAME = 'agents-platform'

# Local logger's levels
DEBUG_LEVEL = 'Debug'
INFO_LEVEL = 'Info'
WARNING_LEVEL = 'Warning'
ERROR_LEVEL = 'Error'
EXCEPTION_LEVEL = 'Exception'

# Google logger has 'CRITICAL' level instead 'EXCEPTION'
# Mapping of local logger levels to the ones of Google's
google_logger_enums = {
    DEBUG_LEVEL: 'DEBUG',
    INFO_LEVEL: 'INFO',
    WARNING_LEVEL: 'WARNING',
    ERROR_LEVEL: 'ERROR',
    EXCEPTION_LEVEL: 'CRITICAL'
}

UTILS = 'utils'

AGENTS_PATH = os.environ['OWN_AGENTS_PATH']
ACTUAL_AGENTS_PATH = os.path.join(AGENTS_PATH, 'agents')

# Firestore constants
AGENTS_PLATFORM_KEY = 'agentsPlatform'
AVAILABLE_AGENT_PORTS = 'availableAgentPorts'
AVAILABLE_AGENT_HANDLER_PORTS = 'availableAgentHandlerPorts'
PORTS_KEY = 'ports'
AGENT_HANDLERS = 'agentHandlers'
AGENT_FEATURES = 'features'
AGENT_HANDLER_ADDRESS_KEY = 'address'
AGENT_HANDLER_NUM_AGENTS_KEY = 'currentNumberOfAgents'
AGENT_HANDLER_NUM_TASKS_KEY = 'numberOfTasks'
AGENT_HANDLER_MAX_TASKS_KEY = 'maxNumberOfTasks'
AGENT_TASKS_KEY = 'agentTasks'
AGENT_TASK_ELEMENT_KEY = 'agentTaskElement'
BOARD_IDENTIFIER_KEY = 'boardId'
MESSAGES_KEY = 'messages'
MESSAGE_KEY = 'message'
AGENT_HANDLER_NUM_FAILS_KEY = 'numberOfFails'
TASK_NAME_KEY = 'task'
CONSTANT_MONITORING_KEY = 'constant_monitoring'
DOC_LAYER_NAME = 'docBecauseFirestoreCantHandleNestedCollections'
LISTENER_SET_KEY = 'listener_set'
WORKER_SET_KEY = 'worker_set'
ELEMENT_ID_KEY = 'elementId'
QUERY_ID_KEY = 'queryId'
INDEX_KEY = 'index'
LAST_MESSAGE_READ_KEY = 'lastMessageRead'
UPDATE_PERIOD_KEY = 'updatePeriod'
TIME_TO_UPDATE_KEY = 'timeToUpdate'
AGENT_TASK_KEY = 'agentTask'
UPDATING_KEY = 'updating'
SOCIAL_MEDIA_ACTIVITY_CHART = 'socialMediaActivityChart'
FILE_ID_KEY = 'fileId'
CHART_UNTIL_DATE_KEY = 'chartUntilDate'
POSTS_UNTIL_DATE = 'postsUntilDate'
REPORT_KEY = 'report'

MAX_NUMBER_OF_HANDLER_FAILS = 3
DOWNLOADS_DIR = 'downloads'
