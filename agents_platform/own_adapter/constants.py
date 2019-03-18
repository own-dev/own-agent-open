"""
This module only contains global variables and platform config
"""

import os
from configparser import ConfigParser

# PATHS
from enum import Enum

from utils import logger

# NAMES
OWN_ADAPTER_NAME = 'own_adapter'
ENGINE_NAME = 'engine'

try:
    AGENTS_PATH = os.getenv('OWN_AGENTS_PATH')
    # TODO: Check if paths below exist
    ACTUAL_AGENTS_PATH = os.path.join(AGENTS_PATH, 'agents')
    AGENTS_PLATFORM_PATH = os.path.join(AGENTS_PATH, 'agents_platform')
    AGENTS_SERVICES_PATH = os.path.join(AGENTS_PLATFORM_PATH, 'services')
    OWN_ADAPTER_PATH = os.path.join(AGENTS_PLATFORM_PATH, 'own_adapter')
except KeyError as e:
    logger.exception(OWN_ADAPTER_NAME, f'OWN_AGENTS_PATH is undefined. Error message: {e}')

if 'AGENTS_ENVIRONMENT' in os.environ:
    AGENTS_ENVIRONMENT = os.environ['AGENTS_ENVIRONMENT']
else:
    AGENTS_ENVIRONMENT = 'test'
    logger.info(OWN_ADAPTER_NAME, f'AGENTS_ENVIRONMENT is not defined. Setting it to test.')

# OWN PLATFORM URL
try:
    ADDRESS = os.getenv('OWN_PLATFORM_ADDRESS')
    PROTOCOL = os.getenv('OWN_PLATFORM_PROTOCOL')
    PREFIX = os.getenv('OWN_PLATFORM_PREFIX')
    # ADDRESS = ADDRESS if not PREFIX else f'{ADDRESS}/{PREFIX}'
except KeyError as error:
    logger.exception(OWN_ADAPTER_NAME, f'Platform URL variables are not found: {error}')

PLATFORM_CONFIG = ConfigParser()
PLATFORM_CONFIG.read(f'{AGENTS_PATH}/platform.conf')

# VARIABLES
STATUS = {
    'ACTIVE': 0,
    'BEING_TESTED': 1,
    'INACTIVE': 2,
}
TOKEN_EXPIRE_DAYS = 29

# Element types
ELEM_TYPE_HTML_REFERENCE = 'application/vnd.uberblik.htmlReference'

#Chart constants
DATA_KEY = 'data'
X_AXIS_KEY = 'xAxis'
INDICATOR_KEY = 'indicator'
VALUE_KEY = 'value'
SERIES_KEY = 'series'
TOOLTIP_KEY = 'tooltip'
NAME_KEY = 'name'
# Chart types:
LINE_CHART_TYPE = 'LINE'
BAR_CHART_TYPE = 'BAR'
SCATTER_CHART_TYPE = 'SCATTER'
RADAR_CHART_TYPE = 'RADAR'
PIE_CHART_TYPE = 'PIE'
TYPE_KEY = 'type'

class AdapterStatus():
    """
    Class for own adapter status codes
    """
    SUCCESS = 2
    FAIL = -1
    PARTIAL_UPDATE = 1
    CONNECTION_ABORTED = 0
