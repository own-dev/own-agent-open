"""
Command-line interface representation of AgentsPlatform Engine
"""

import json
import os
from configparser import ConfigParser
from enum import Enum
from typing import List, Dict, Tuple, Optional

import agents_platform.constants as constants
from agents_platform.cli.menu import Menu
from agents_platform.constants import META_SECTION_KEY, SUBSCRIPTION_SECTION_KEY, SALARY_KEY, CAPACITY_KEY, \
    DAY_KEY, WEEK_KEY, MONTH_KEY, YEAR_KEY, CURRENCY_KEY, ID_KEY, CONTENT_SECTION_KEY, \
    SUBSCRIPTION_INTERVAL_COUNT_KEY, SUBSCRIPTION_PLANS_KEY, PLAN_PRICINGS_KEY, SUBSCRIPTION_INTERVAL_KEY, \
    DAY_CAPACITY_KEY, DAY_SALARY_KEY, DAY_INTERVAL_KEY, \
    WEEK_CAPACITY_KEY, WEEK_SALARY_KEY, WEEK_INTERVAL_KEY, \
    MONTH_CAPACITY_KEY, MONTH_SALARY_KEY, MONTH_INTERVAL_KEY, FILENAME_KEY, SUBSCRIPTION_PLAN_OWNER_TYPE_KEY, \
    OWNER_TYPE_USER, OWNER_TYPE_ORG
from agents_platform.engine import AgentsPlatformEngine
from agents_platform.own_adapter.agent_data import put_agent_data, post_agent_data, \
    get_all_agents_data, delete_agent_data, get_agent_data_by_user_id
from agents_platform.own_adapter.agent_task import remove_agent_task_by_id, \
    get_agent_task_by_id, upload_or_update_agent_task_from_file, update_agent_task_by_id
from agents_platform.own_adapter.constants import AGENTS_SERVICES_PATH
from agents_platform.own_adapter.platform_access import PlatformAccess
from agents_platform.util.networking import make_request


# Define periodical enum
class PeriodicalPlan(Enum):
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'


PERIODS = [PeriodicalPlan.DAY.value, PeriodicalPlan.WEEK.value, PeriodicalPlan.MONTH.value]


BACK = ('Back', Menu.CLOSE, None)  # "Shortcut" for back-menu
STATUS = {'0': 'ACTIVE', '1': 'BEING_TESTED', '2': 'INACTIVE'}  # AgentData status "enum"
CONFIG_PARSER = ConfigParser()

LOGIN = os.environ['OWN_TEST_LOGIN']
PASSWORD = os.environ['OWN_TEST_PASSWORD']


class EngineMenu(AgentsPlatformEngine):
    """
    Menu-based AgentsPlatform CLI
    """

    def __init__(self):
        super(EngineMenu, self).__init__()

        # ---------------------------------------
        # AGENT DATA CONFIGURATIONS
        # ---------------------------------------
        self.configs_menu_list = Menu(title='List of existing Agents',
                                      refresh=self.refresh_configs_menu_list,
                                      message='')
        self.configs_menu_create = Menu(title='Create a new Agent from file',
                                        refresh=self.refresh_configs_menu_create,
                                        message='')
        self.configs_menu_update = Menu(title='Update Agent from file',
                                        refresh=self.refresh_configs_menu_update_or_remove,
                                        message='')
        self.configs_menu_remove = Menu(title='Remove Agent',
                                        refresh=self.refresh_configs_menu_remove,
                                        message='')

        self.configs_menu_options = [
            ('List existing agents', self.configs_menu_list.open),
            ('Create a new agent', self.configs_menu_create.open),
            ('Update existing agent', self.configs_menu_update.open),
            ('Remove existing agent', self.configs_menu_remove.open),
            BACK
        ]
        self.configs_menu = Menu(options=self.configs_menu_options, title='Agent Configurations')
        # ---------------------------------------
        #

        # ---------------------------------------
        # AGENT SERVICES
        # ---------------------------------------
        self.services_menu_list = Menu(title='Agent Services List', refresh=self.refresh_services_menu_list)
        self.services_menu_options = [
            ('List existing AgentServices', self.services_menu_list.open),
            BACK
        ]
        self.services_menu = Menu(options=self.services_menu_options, title='Agent Services')
        # ---------------------------------------
        #

        # ---------------------------------------
        # AGENT TASKS
        # ---------------------------------------
        self.tasks_menu_list = Menu(title='Agent Tasks List', refresh=self.refresh_tasks_menu_list, message='')
        self.tasks_menu_create = Menu(title='Create Agent Task', refresh=self.refresh_tasks_menu_create, message=None)
        self.tasks_menu_update = Menu(title='Update Agent Task', refresh=self.refresh_tasks_menu_update, message='')
        self.tasks_menu_remove = Menu(title='Remove Agent Task', refresh=self.refresh_tasks_menu_remove, message='')
        self.tasks_menu_options = [
            ('List existing Agent Tasks', self.tasks_menu_list.open),
            ('Create new Agent Task', self.tasks_menu_create.open),
            ('Update Agent Tasks from local files', self.tasks_menu_update.open),
            ('Remove existing Agent Tasks', self.tasks_menu_remove.open),
            BACK
        ]
        self.tasks_menu = Menu(options=self.tasks_menu_options, title='Agent Tasks')
        # ---------------------------------------
        #

        self.main_menu_options = [
            ('Agent Configurations', self.configs_menu.open),
            ('Agent Services', self.services_menu.open),
            ('Agent Tasks', self.tasks_menu.open),
            ('Exit', Menu.CLOSE)
        ]
        self.main_menu = Menu(options=self.main_menu_options, title="AgentsPlatform Menu")

    def find_agent_credentials(self, name: str) -> Tuple[str, str]:
        """
        Find credentials from environment variables of an agent
        :param name: a name of the agent
        :return: a login, a password
        """
        try:
            login = os.environ[f'OWN_{name.upper()}_AGENT_LOGIN']
            password = os.environ[f'OWN_{name.upper()}_AGENT_PASSWORD']
        except KeyError as e:
            print(f'OWN_{name.upper()}_AGENT_LOGIN and/or OWN_{name.upper()}_AGENT_PASSWORD were not found. '
                  f'Error message: {e}')
            return '', ''
        if not (login or password):
            print(f'OWN_{name.upper()}_AGENT_LOGIN and/or OWN_{name.upper()}_AGENT_PASSWORD are/is empty.')
            return '', ''
        return login, password

    def _get_confirmation(self, promt: str = 'Are you sure? [y/N]') -> bool:
        """
        Asks for confirmation
        :param promt: a question to ask
        :return: True/False
        """
        answer = input(promt)
        return answer.lower() in ['y', 'yes']

    def get_agent_data_id_by_agent_name(self, agent_name: str) -> [Tuple[int, Tuple[str, str]],
                                                                   Tuple[None, Tuple[str, str]]]:
        """
        Get an agent data id from a config file of an agent
        :param agent_name: a name of the config file
        :return: the agent data id and credentials of the agent
        """

        credentials = self.find_agent_credentials(agent_name)
        if not credentials[0]:
            return None, credentials

        agent_data = get_agent_data_by_user_id(PlatformAccess(credentials[0], credentials[1]))
        if not agent_data:
            return None, credentials
        return agent_data['agentData']['id'], credentials

    def find_local_agent_name_by_id(self, agent_data_id: int,
                                    local_configs: Dict = None) -> Tuple[str, Tuple[str, str], Dict]:
        """
        Find an agent name by id from local configs
        :param agent_data_id: an agent data id
        :param local_configs: a list containing local configs
        :return: the agent name, credentials and a local config of that agent
        """
        if not local_configs:
            local_configs = self._get_agents_configs_local()
        # Different agents should have different credentials
        for config_filepath, config in local_configs.items():
            # Read the config
            local_agent_name = config['agentData']['name']
            credentials = self.find_agent_credentials(local_agent_name)
            if not credentials[0]:
                continue
            agent_data = get_agent_data_by_user_id(PlatformAccess(credentials[0], credentials[1]))
            if not agent_data:
                continue
            if agent_data['agentData']['id'] == agent_data_id:
                config['file_path'] = config_filepath
                return local_agent_name, credentials, config

        return '', ('', ''), {}

    # Configs
    # ---------------------------------------
    def refresh_configs_menu_list(self) -> None:
        """
        Lists all the agent-services on the local machine
        Allows to Run or Stop them
        :return: Nothing
        """
        # Get AgentData configs from the back-end
        agent_datas = get_all_agents_data(PlatformAccess(LOGIN, PASSWORD))

        # Generate all the menu-items
        menu_items = list()
        for agent in agent_datas:
            # Create a new menu-item
            agent_name = f"{agent['agentsUser']['firstName']}"
            new_entry_name = f"{agent_name:<16} (id={agent['id']:<4})\t{agent['status']}"
            backend_config_readable = self.config_to_readable(agent)
            if 'agentTasks' in backend_config_readable:
                backend_config_readable.pop('agentTasks', None)
            new_entry = Menu(title=new_entry_name,
                             options=[
                                 ('Set ACTIVE', self._change_config_status,
                                  {'agent_name': agent_name.lower(), 'agent_data': agent, 'new_status': 1}),
                                 ('Set BEING_TESTED', self._change_config_status,
                                  {'agent_name': agent_name.lower(), 'agent_data': agent, 'new_status': 2}),
                                 ('Set INACTIVE', self._change_config_status,
                                  {'agent_name': agent_name.lower(), 'agent_data': agent, 'new_status': 3}),
                                 (f'AGENT CONFIG: \n{json.dumps(backend_config_readable, indent=2)}',
                                  lambda: None, None),
                                 BACK
                             ])
            menu_items.append(new_entry)

        # Generate options for AgentTasks::List
        new_options = [(config_item.title, config_item.open, None) for config_item in menu_items]
        new_options.append(BACK)

        self.configs_menu_list.set_options(new_options)

    def refresh_configs_menu_create(self) -> None:
        """
        Refreshes AgentData::Create menu
        :return: None
        """
        local_configs = self._get_agents_configs_local()

        # Generate menu-items (options)
        new_options = list()
        for config_filepath, config in local_configs.items():
            agent_name = config['agentData']['name']
            credentials = self.find_agent_credentials(agent_name)
            if not (credentials[0] and credentials[1]):
                continue
            agent_data = get_agent_data_by_user_id(PlatformAccess(credentials[0], credentials[1]))
            if agent_data:
                continue

            # Create a new menu-item
            config_data = json.loads(self.config_to_json(config_filepath))
            new_options.append((f'{agent_name} agent',
                                self._add_new_config,
                                {'config_path': config_filepath, 'config_data': config_data}))

        new_options.append(BACK)

        # Set options for creation menu
        self.configs_menu_create.set_options(new_options)

    def refresh_configs_menu_update_or_remove(self, remove_flag: bool = False) -> None:
        """
        Refreshes either AgentDataConfigurations::Update or AgentDataConfigurations::Remove menu
        :param remove_flag: False - find configs to be updated, True - find configs to be removed
        :return: None
        """
        # Get the AgentData from the back-end
        local_configs = self._get_agents_configs_local()

        # To check if AgentData ID is unique; fool proof
        agent_data_ids = {}

        new_options = []
        for config_filepath, config in local_configs.items():
            local_agent_name = config['agentData']['name']
            credentials = self.find_agent_credentials(local_agent_name)
            if not (credentials[0] and credentials[1]):
                continue
            agent_data = get_agent_data_by_user_id(PlatformAccess(credentials[0], credentials[1]))
            if not agent_data:
                continue

            # Create a new menu-item
            if not remove_flag:
                # Create a new menu-item for Update
                new_options.append((local_agent_name, self._update_config,
                                    {'agent_data': agent_data,
                                     'agent_name': local_agent_name,
                                     'credentials': credentials,
                                     'config': config}))
            else:
                # Check if this AgentData ID is unique
                if agent_data['agentData']['id'] not in agent_data_ids:
                    # TODO: Log if it wasn't the unique ID
                    agent_data_ids[agent_data['agentData']['id']] = True

                    # Create a new menu-item for Remove
                    new_options.append((f'Id: {agent_data["agentData"]["id"]} :: Desc: '
                                        f'{agent_data["agentData"]["description"]}', self._remove_config,
                                        {'agent_data': agent_data, 'credentials': credentials}))

        new_options.append(BACK)

        # Add options to either menu
        if not remove_flag:
            self.configs_menu_update.set_options(new_options)
        else:
            self.configs_menu_remove.set_options(new_options)

    def refresh_configs_menu_remove(self) -> None:
        """
        Refreshes AgentConfigurations::Remove menu
        :return: None
        """
        self.refresh_configs_menu_update_or_remove(remove_flag=True)

    def config_to_readable(self, agent_data: Dict):
        """
        Remove unnecessary data from config
        :param agent_data: an agent data dict, without nested 'agentData'
        :return: a clear version of config
        """
        config_readable = agent_data.copy()
        config_readable.pop('id', None)
        config_readable.pop('agentsUser', None)
        config_readable.pop('_links', None)

        return config_readable

    def _add_new_config(self, kwargs: Dict) -> None:
        """
        Adds new AgentData to the back-end from the given config_data and config_path;
        later then updates the local configs with newly assigned IDs
        :param kwargs: {'config_data': Dict, 'config_path': str}
                       config_path -- absolute path to the config to add
                       config_data -- settings.conf as a dictionary
        :return: Nothing
        """
        # Check if data exists
        config_data: Dict = kwargs.get('config_data', None)
        config_path: str = kwargs.get('config_path', None)
        if not (config_data and config_path):
            return

        # Get new credentials from env. vars
        agent_name = config_data['agentData']['name']
        if not agent_name:
            return
        credentials = self.find_agent_credentials(agent_name)

        # Execute POST-request
        response = post_agent_data(platform_access=PlatformAccess(credentials[0], credentials[1]), data=config_data)
        if not response:
            return

        # Update local machine's config
        self._json_to_config(json_data=json.dumps(response), conf_filepath=config_path)

    def _update_config(self, data: Dict) -> None:
        """
        Updates AgentData on the back-end
        :param data: {'agent_data': Dict, 'agent_name': str, 'credentials': Tuple[str, str], 'config': Dict}
                       agent_data -- agent_data stored on the backend
                       agent_name -- a name of an agent to be updated
                       credentials -- a login and a password of that agent
                       config -- a local config to be uploaded
                       
        :return: None
        """
        backend_config = data['agent_data']['agentData']
        agent_name = data['agent_name']
        credentials = data['credentials']
        data = data['config']
        local_config_data = data['agentData']

        # Update the local config with IDs from the back-end
        new_config_data_with_ids = local_config_data
        new_config_data_with_ids[ID_KEY] = backend_config[ID_KEY]

        def find_subs_plan_by_period_name(subscription_plans: List[Dict], period_val: PeriodicalPlan) -> Optional[Dict]:
            """
            Searches for the needed subscription plan in the given ones by name
            Reference: See Agent Data section in docs/APIDescription.md
            :param subscription_plans: Subscription plans to search in
            :param period_val: "DAY", "WEEK", or "MONTH"
            :return: If found, returns a subscription plan data for the given period, otherwise, None
            """
            if not (subscription_plans and period_val):
                return None

            required_subscription_plan = None
            for plan in subscription_plans:
                if plan[SUBSCRIPTION_INTERVAL_KEY] == period_val:
                    required_subscription_plan = plan
                    break
            return required_subscription_plan

        # Adds IDs for the new config parsed from the one form back-end
        # TODO: After production server's updated for Organization payments, add its handling
        backend_subscriptions = backend_config[SUBSCRIPTION_PLANS_KEY]
        for idx, period in enumerate(PERIODS):
            back_subs_plan = find_subs_plan_by_period_name(backend_subscriptions, period)
            if not back_subs_plan:
                continue

            # Update subscription interval ID
            back_interval_id = back_subs_plan[ID_KEY]
            new_config_data_with_ids[SUBSCRIPTION_PLANS_KEY][idx][ID_KEY] = \
                back_interval_id

            # Update subscription plan pricing ID
            back_plan_pricing_id = back_subs_plan[PLAN_PRICINGS_KEY][0][ID_KEY]  # For euro-currency
            new_config_data_with_ids[SUBSCRIPTION_PLANS_KEY][idx][PLAN_PRICINGS_KEY][0][ID_KEY] = \
                back_plan_pricing_id

        # Get confirmation to do the operation
        backend_config_readable = self.config_to_readable(backend_config)
        old_config = json.dumps(backend_config_readable, indent=2)
        new_config = json.dumps(local_config_data, indent=2)
        
        if not self._get_confirmation(f'Current configuration: \n {old_config}\n'
                                      f'New configuration: \n {new_config}\n'
                                      f'Update {agent_name}\'s configuration on the back-end?.. [y/N]\n'):
            return

        # Actually update it
        res = put_agent_data(platform_access=PlatformAccess(credentials[0], credentials[1]),
                             data=data, agent_data_id=backend_config['id'])
        if not res:
            print('Agent was not updated')

    def _remove_config(self, dict_with_data: Dict) -> None:
        """
        Removes AgentData from the back-end
        :param dict_with_data: {'agent_data': Dict, 'credentials': Tuple[str, str]}
                       agent_data -- agent_data stored on the backend
                       credentials -- a login and a password of that agent
        :return: None
        """
        agent_data = dict_with_data['agent_data']['agentData']
        credentials = dict_with_data['credentials']
        agent_data_id = agent_data['id']

        backend_config_readable = self.config_to_readable(agent_data)
        if not self._get_confirmation(f'Agent config to be removed: \n {backend_config_readable}'
                                      f' \nAre you sure you want to '
                                      f'remove Agent with ID = {agent_data_id}? [y/N]'):
            return

        res = delete_agent_data(platform_access=PlatformAccess(credentials[0], credentials[1]),
                                agent_data_id=agent_data_id)
        if not res:
            print('Agent was not deleted')

    def _change_config_status(self, kwargs: Dict) -> None:
        """
        Changes config's status on the back-end
        :param kwargs: {'agent_name': str, 'new_status': str, 'agent_data': Dict}
                        agent_name -- a name of an agent
                        credentials -- a login and a password of that agent
                        agent_data -- agent data of the agent
        :return: Nothing
        """
        agent_name = kwargs.get('agent_name', None)
        new_status = kwargs.get('new_status', None)
        agent_data = kwargs.get('agent_data', None)

        if not (agent_name and new_status and agent_data):
            return

        agent_data_id = agent_data['id']
        # Fix the status to its real value
        # Input parameter can be 1, or 2, or 3
        # to escape "if not new_status:" when it's 0 (and not None)
        new_status -= 1

        agent_name, credentials, config = self.find_local_agent_name_by_id(agent_data_id)
        if not agent_name:
            print(f'You don\'t have access to that agent')
            return
        # Firstly, get confirmation to do te operation
        if not self._get_confirmation():
            return

        agent_data['status'] = new_status
        # Update the back-end
        response = put_agent_data(platform_access=PlatformAccess(credentials[0], credentials[1]),
                                  data={'agentData': agent_data}, agent_data_id=agent_data_id)
        if response:
            print(f'{agent_name}\'s status was set to {STATUS[str(new_status)]}.')
        else:
            print(f'{agent_name}\'s status was not updated.')

    @staticmethod
    def config_to_json(conf_filepath: str, json_filepath: str = None) -> Optional[str]:
        """
        Converts config file to a JSON-string
        :param conf_filepath: Absolute path to a config to convert..
        :param json_filepath: (Optional) Absolute path to a file where to write the result
        :return: Config in as a JSON-like string
        """
        if not conf_filepath:
            return None

        # Read config-file
        CONFIG_PARSER.clear()
        with open(conf_filepath, 'r') as file:
            CONFIG_PARSER.read_file(file)

        # Generate the data
        currency = CONFIG_PARSER.get(SUBSCRIPTION_SECTION_KEY, CURRENCY_KEY)
        data = {
            'name': CONFIG_PARSER.get(META_SECTION_KEY, 'name'),
            'description': CONFIG_PARSER.get(META_SECTION_KEY, 'description'),
            'status': CONFIG_PARSER.get(META_SECTION_KEY, 'status'),
            'greetingMessage': CONFIG_PARSER.get(CONTENT_SECTION_KEY, 'hello_message'),
            SUBSCRIPTION_PLANS_KEY:
                [
                    {
                        SUBSCRIPTION_INTERVAL_KEY: DAY_KEY,
                        SUBSCRIPTION_INTERVAL_COUNT_KEY: CONFIG_PARSER.getint(SUBSCRIPTION_SECTION_KEY,
                                                                              DAY_INTERVAL_KEY),
                        CAPACITY_KEY: CONFIG_PARSER.getint(SUBSCRIPTION_SECTION_KEY, DAY_CAPACITY_KEY),
                        PLAN_PRICINGS_KEY: [
                            {
                                CURRENCY_KEY: currency,
                                SALARY_KEY: CONFIG_PARSER.getfloat(SUBSCRIPTION_SECTION_KEY, DAY_SALARY_KEY)
                            }
                        ],
                        SUBSCRIPTION_PLAN_OWNER_TYPE_KEY: OWNER_TYPE_USER
                    },
                    {
                        SUBSCRIPTION_INTERVAL_KEY: WEEK_KEY,
                        SUBSCRIPTION_INTERVAL_COUNT_KEY: CONFIG_PARSER.getint(SUBSCRIPTION_SECTION_KEY,
                                                                              WEEK_INTERVAL_KEY),
                        CAPACITY_KEY: CONFIG_PARSER.getint(SUBSCRIPTION_SECTION_KEY, WEEK_CAPACITY_KEY),
                        PLAN_PRICINGS_KEY: [
                            {
                                CURRENCY_KEY: currency,
                                SALARY_KEY: CONFIG_PARSER.getfloat(SUBSCRIPTION_SECTION_KEY, WEEK_SALARY_KEY)
                            }
                        ],
                        SUBSCRIPTION_PLAN_OWNER_TYPE_KEY: OWNER_TYPE_USER
                    },
                    {
                        SUBSCRIPTION_INTERVAL_KEY: MONTH_KEY,
                        SUBSCRIPTION_INTERVAL_COUNT_KEY: CONFIG_PARSER.getint(SUBSCRIPTION_SECTION_KEY,
                                                                              MONTH_INTERVAL_KEY),
                        CAPACITY_KEY: CONFIG_PARSER.getint(SUBSCRIPTION_SECTION_KEY, MONTH_CAPACITY_KEY),
                        PLAN_PRICINGS_KEY: [
                            {
                                CURRENCY_KEY: currency,
                                SALARY_KEY: CONFIG_PARSER.getfloat(SUBSCRIPTION_SECTION_KEY, MONTH_SALARY_KEY)
                            }
                        ],
                        SUBSCRIPTION_PLAN_OWNER_TYPE_KEY: OWNER_TYPE_USER
                    },
                    {
                        SUBSCRIPTION_INTERVAL_KEY: MONTH_KEY,
                        SUBSCRIPTION_INTERVAL_COUNT_KEY: CONFIG_PARSER.getint(SUBSCRIPTION_SECTION_KEY,
                                                                              WEEK_INTERVAL_KEY),
                        CAPACITY_KEY: CONFIG_PARSER.getint(SUBSCRIPTION_SECTION_KEY, WEEK_CAPACITY_KEY),
                        PLAN_PRICINGS_KEY: [
                            {
                                CURRENCY_KEY: currency,
                                SALARY_KEY: CONFIG_PARSER.getfloat(SUBSCRIPTION_SECTION_KEY, WEEK_SALARY_KEY)
                            }
                        ],
                        SUBSCRIPTION_PLAN_OWNER_TYPE_KEY: OWNER_TYPE_ORG
                    },
                    {
                        SUBSCRIPTION_INTERVAL_KEY: YEAR_KEY,
                        SUBSCRIPTION_INTERVAL_COUNT_KEY: CONFIG_PARSER.getint(SUBSCRIPTION_SECTION_KEY,
                                                                              MONTH_INTERVAL_KEY),
                        CAPACITY_KEY: CONFIG_PARSER.getint(SUBSCRIPTION_SECTION_KEY, MONTH_CAPACITY_KEY),
                        PLAN_PRICINGS_KEY: [
                            {
                                CURRENCY_KEY: currency,
                                SALARY_KEY: CONFIG_PARSER.getfloat(SUBSCRIPTION_SECTION_KEY, MONTH_SALARY_KEY)
                            }
                        ],
                        SUBSCRIPTION_PLAN_OWNER_TYPE_KEY: OWNER_TYPE_ORG
                    },
                ]
        }

        # Convert to a JSON-string
        json_data: str = json.dumps({'agentData': data}, indent=4)

        # Write to a file if needed
        if json_filepath and os.path.exists(json_filepath):
            # TODO: Create a file if there it doesn't exist
            with open(json_filepath, 'w') as file:
                file.write(json_data)

        return json_data

    @staticmethod
    def _json_to_config(json_data: str, conf_filepath: str) -> None:
        """
        Updates config with a JSON-string's data
        :param json_data: JSON-like string with 'id',
        :param conf_filepath: Absolute path to a config to rewrite
        :return: Nothing
        """
        if not (json_data and conf_filepath):
            return

        # TODO: Check if config-file exists

        # Read the old config
        CONFIG_PARSER.clear()
        with open(conf_filepath, 'r') as file:
            CONFIG_PARSER.read_file(file)

        # Turn JSON-string to a dictionary
        data: Dict = json.loads(json_data).get('agentData', None)
        if not data:
            print(f'Data was not found during converting JSON to config ({conf_filepath})')
            return

        def update_time_subscriptions(time_key: str, data_items: Tuple) -> None:
            # Get the keys' values from constants' names
            keys = (getattr(constants, f'{time_key.upper()}_INTERVAL_KEY'),
                    getattr(constants, f'{time_key.upper()}_CAPACITY_KEY'),
                    getattr(constants, f'{time_key.upper()}_SALARY_KEY'))

            # Set all the options (keys) with the given data
            for idx in range(len(keys)):
                CONFIG_PARSER.set(SUBSCRIPTION_SECTION_KEY, keys[idx], str(data_items[idx]))
        subscription_plans = data['agentSubscriptionPlans']

        # TODO: Refactor all the config-depended pipeline
        # Update the data for each of the subscriptions
        for idx, period in enumerate(PERIODS):
            update_time_subscriptions(period, (subscription_plans[idx][SUBSCRIPTION_INTERVAL_COUNT_KEY],
                                               subscription_plans[idx][CAPACITY_KEY],
                                               subscription_plans[idx][PLAN_PRICINGS_KEY][0][SALARY_KEY]))

        status = data['status']
        if status not in STATUS.keys():
            for key, status_item in STATUS.items():
                if status == status_item:
                    status = str(key)
        CONFIG_PARSER.set('meta', 'status', status)

        # Write data to a file
        with open(conf_filepath, 'w') as file:
            CONFIG_PARSER.write(file)

    @staticmethod
    def _json_file_to_config(json_filepath: str, conf_filepath: str) -> None:
        """
        Converts a JSON file to a config
        :param json_filepath: Absolute path to a JSON file to read from
        :param conf_filepath: Absolute path to a config file to write to
        :return: Nothing
        """
        # Check if data is correct
        if not (conf_filepath and json_filepath):
            return
        if not (os.path.exists(conf_filepath) and os.path.exists(json_filepath)):
            return

        # Read the old config
        CONFIG_PARSER.clear()
        with open(conf_filepath, 'r') as file:
            CONFIG_PARSER.read_file(file)

        # Open JSON-file
        with open(json_filepath, 'r') as file:
            data = json.load(file).get('agentData', None)
        if not data:
            return

        # Update the data
        CONFIG_PARSER.set('meta', 'description', data['description'])
        CONFIG_PARSER.set('meta', 'salary', data['salary'])
        CONFIG_PARSER.set('meta', 'status', data['status'])

        # Write data to a file
        with open(conf_filepath, 'w') as file:
            CONFIG_PARSER.write(file)

    def _get_agents_configs_local(self) -> Dict:
        """
        Grabs all the agent-services' configs, converting all of them to a dictionaries
        :return: Structure is: {'abs_config_path_1': {}, .., 'abs_config_path_N': {}}
        """
        result: Dict[str, Dict] = dict()
        for service_folder_item in os.listdir(self.services_abs_path):
            # Check if it's a service folder
            if service_folder_item.endswith('_service'):
                config_path = os.path.join(self.services_abs_path, service_folder_item, 'settings.conf')
                config_data = json.loads(EngineMenu.config_to_json(config_path))
                result[config_path] = config_data
        return result

    # ---------------------------------------

    # Services
    # ---------------------------------------
    def refresh_services_menu_list(self) -> None:
        """Refreshes AgentServices::List with local configs"""
        new_options = list()

        # Generate menu-items
        for config_path, config in self._get_agents_configs_local().items():
            # Get service name from the config
            service_name = config['agentData']['name']
            service_status = 'STOPPED' if service_name in self.blacklist else 'RUNNING'

            # Change status menu-item
            menu_item = Menu(title=f'{service_name}, {service_status}',
                             options=[
                                 (f'Run {service_name}-service', self._run_service, f'{service_name.lower()}'),
                                 (f'Stop {service_name}-serivce', self._stop_service, f'{service_name.lower()}'),
                                 BACK
                             ])
            new_options.append((f'{service_name:<12} {service_status}', menu_item.open, None))
        new_options.append(BACK)

        # Set header-message
        self.services_menu_list.set_message('   {:<12} {}'.format('Agent-name', 'Status'))
        # Set them as options
        self.services_menu_list.set_options(new_options)

    def _run_service(self, service_name: str) -> bool:
        """Runs the serivce by the given name if it's correct and not running already"""
        return False

    def _stop_service(self, service_name: str) -> bool:
        """Runs the serivce by the given name if it's correct and not running already"""
        return False

    # ---------------------------------------

    # Tasks
    # ---------------------------------------
    def refresh_tasks_menu_list(self) -> None:
        """
        Refreshes AgentTasks::List menu
        :return: None
        """

        message = '{0:>5} {1}'.format('ID', 'Description')

        # Get all the AgentsData (to extract IDs) from the back-end
        all_agent_tasks: Dict = self._get_remote_agent_tasks()

        menu_items = []
        for agent_data_id, agent_tasks in all_agent_tasks.items():
            for agent_task in agent_tasks[0]:
                new_entry = Menu(title=f"{agent_task['id']} {agent_task['description']}",
                                 options=[(json.dumps(agent_task, indent=2), lambda: None, None), BACK])
                menu_items.append(new_entry)

        new_options = [(config_item.title, config_item.open, None) for config_item in menu_items]

        new_options.append(BACK)
        # Set the parameters for the menu
        self.tasks_menu_list.set_message(message)
        self.tasks_menu_list.set_options(new_options)

    def refresh_tasks_menu_create(self) -> None:
        """
        Refreshes AgentTask::Create menu
        Retrieves all the forms w/o IDs from the local machine, and then generates menu-items
        :return: Nothing
        """
        new_options = list()

        # Find all the NEW (w/o IDs) AgentTasks on the local machine
        found_new_agent_tasks: Dict = self._get_new_local_agent_tasks_paths()

        for task_filepath in found_new_agent_tasks:
            # Generate new menu-item's title
            with open(os.path.join(AGENTS_SERVICES_PATH, task_filepath), 'r') as file:
                task_data = json.load(file)
                new_option_name = task_data['agentTask']['description']

            # Add new menu-item tuple
            new_options.append((new_option_name, self._create_new_agent_task, task_filepath))

        new_options.append(BACK)
        self.tasks_menu_create.set_options(new_options)

    def refresh_tasks_menu_update(self) -> None:
        """
        Refreshes AgentTasks::Update menu with a list of AgentTasks that persist on the back-end
        :return: None
        """
        self.tasks_menu_update.set_message('{:>6} {} :: {}'.format('TaskID', 'AgentTitle', 'Description'))
        new_options = list()

        # Get the local tasks with IDs
        agent_tasks = self._get_old_local_agent_tasks()

        for form in agent_tasks:
            agent_task_data = form['agentTask']
            new_option_title = f"{agent_task_data['id']} {agent_task_data['input']['title']} :: " \
                               f"{agent_task_data['description']}"
            new_options.append((new_option_title, self.update_agent_task, form))

        # Add back option
        new_options.append(BACK)

        self.tasks_menu_update.set_options(new_options)

    def update_agent_task(self, form: Dict) -> None:
        """
        Upload an agent task to backend
        :param: form: an agent task to be uploaded
        :return None
        """
        if not form:
            return None
        agent_task = form.get('agentTask', None)
        if not agent_task:
            return None
        agent_task_id = agent_task.get('id', None)

        agent_name = form['filename'].split('/')[0].split('_service')[0]
        agent_data_id, credentials = self.get_agent_data_id_by_agent_name(agent_name)
        if not agent_data_id:
            print(f'Agent id of {agent_name} is not found')
            return None

        backend_agent_task = get_agent_task_by_id(PlatformAccess(credentials[0], credentials[1]),
                                                  agent_data_id=agent_data_id,
                                                  agent_task_id=agent_task_id)

        if not backend_agent_task:
            backend_agent_task = "Wasn't found"

        # Get confirmation to do the operation
        if not self._get_confirmation(f'Current configuration: \n {json.dumps(backend_agent_task, indent=2)}\n'
                                      f'New configuration: \n {json.dumps(agent_task, indent=2)}\n'
                                      f'Update AgentTask configuration on the back-end?.. [y/N]\n'):
            return None

        # Update task
        update_agent_task_by_id(PlatformAccess(credentials[0], credentials[1]), agent_data_id=agent_data_id, task_file_name=form[FILENAME_KEY], agent_task_id=agent_task_id)

    def refresh_tasks_menu_remove(self) -> None:
        """
        Refreshes AgentTasks::Remove menu
        :return: None
        """
        all_agent_tasks: Dict = self._get_remote_agent_tasks()

        # Set header-message
        self.tasks_menu_remove.set_message('{0:<10} {1} {2}'.format('AgentID', 'AgentTaskID', 'Description'))

        # Generate the list of tuples like: AgentTaskID :: AgentDataID AgentTaskDescription
        new_options = list()

        if all_agent_tasks:
            for agent_data_id, agent_tasks in all_agent_tasks.items():
                credentials = agent_tasks[1]
                for task in agent_tasks[0]:
                    agent_task_id = task['id']

                    new_task_option = (f"{agent_data_id:<4} :: {agent_task_id:<11} {task['description']}",
                                       self._remove_agent_task, {'data_id': agent_data_id,
                                                                 'task_id': agent_task_id,
                                                                 'credentials': credentials,
                                                                 'agent_name': agent_tasks[2]})
                    new_options.append(new_task_option)
        new_options.append(BACK)

        self.tasks_menu_remove.set_options(new_options)

    def _remove_agent_task(self, data: Dict) -> None:
        """
        Removes the AgentTask by the given AgentDataID and AgentTaskID
        :param data: {'data_id': int, 'credentials': Tuple[str, str], 'task_id': int}
                       data_id -- agent_data_id
                       credentials -- a login and a password of an agent of the task
                       task_id -- agent_task_id
                       agent_name -- a name of the agent name
        :return None
        """
        agent_data_id = data.get('data_id', None)
        agent_task_id = data.get('task_id', None)
        credentials = data.get('credentials', None)
        agent_name = data.get('agent_name', None)

        if not agent_task_id or not agent_data_id or not credentials:
            return

        # Get confirmation to do the operation
        if not self._get_confirmation():
            return

        # Execute DELETE-request
        response = remove_agent_task_by_id(platform_access=PlatformAccess(credentials[0], credentials[1]),
                                           agent_data_id=agent_data_id,
                                           agent_task_id=agent_task_id)
        if not response:
            return

        # TODO: Remove IDs for the local file, if it persist on the machine
        def remove_local_form_of_agent_task():
            """Removes AgentTask file from the local machine"""
            # Read the configs
            service_abs_path = os.path.join(self.services_abs_path, f'{agent_name}_service')

            agent_tasks_abs_path = os.path.join(service_abs_path, 'agent_tasks')
            for form in os.listdir(agent_tasks_abs_path):
                if not form.endswith('.json'):
                    continue

                # Read AgentTask
                form_abs_path = os.path.join(agent_tasks_abs_path, form)
                with open(form_abs_path, 'r') as file:
                    form_data: Dict = json.load(file).get('agentTask', None)

                # Check if it has ID
                current_form_id = form_data.get('id', None)
                if current_form_id and current_form_id == agent_task_id:
                    form_data.pop('id')
                    with open(form_abs_path, 'w') as file:
                        json.dump({'agentTask': form_data}, file, indent=2)
                    return

        remove_local_form_of_agent_task()

    def _create_new_agent_task(self, task_filepath: str) -> None:
        """
        Creates a new AgentTask on the back-end
        
        :param task_filepath: a path to a file with a task
        :return: None
        """
        # Check if data persists
        if not task_filepath:
            return

        # Get confirmation to do the operation
        if not self._get_confirmation():
            return

        agent_name = task_filepath.split('/')[0].split('_service')[0]

        agent_data_id, credentials = self.get_agent_data_id_by_agent_name(agent_name)
        if not agent_data_id:
            print(f'Agent id of {agent_name} is not found')
            return
        # Execute POST-request
        upload_or_update_agent_task_from_file(platform_access=PlatformAccess(credentials[0], credentials[1]),
                                              agent_data_id=agent_data_id, file_name=task_filepath, force_update=True)

    def _get_all_local_agent_tasks(self) -> List[Dict]:
        """
        Returns all task stored locally
        :return: a list of tasks
        """
        result = list()

        # For every _service folder
        for entity in os.listdir(self.services_abs_path):
            if not entity.endswith('_service'):
                continue

            # Generate forms absolute path
            forms_abs_path = os.path.join(self.services_abs_path, entity, 'agent_tasks')

            if not os.path.exists(forms_abs_path):
                continue
            # Add every form to the result
            for form in os.listdir(forms_abs_path):
                if not form.endswith('.json'):
                    continue

                # Add the form to the result list
                form_abs_path = os.path.join(forms_abs_path, form)
                with open(form_abs_path, 'r') as file:
                    form_data: Dict = json.load(file)
                    form_data['filename'] = os.path.join(entity, 'agent_tasks', form)
                    result.append(form_data)

        return result

    def _get_old_local_agent_tasks(self) -> List[Dict]:
        """
        Returns all the AgentTasks with IDs from all the agent-services
        :return: a list of tasks
        """
        result = list()
        all_tasks = self._get_all_local_agent_tasks()

        for form in all_tasks:
            # Check if form has ID
            if form.get('agentTask', None) and form['agentTask'].get('id', None):
                result.append(form)

        return result

    def _get_new_local_agent_tasks(self) -> List[Dict]:
        """
        Returns all the AgentTasks without IDs from all the agent-services
        :return: a list of tasks
        """
        result = list()
        all_tasks = self._get_all_local_agent_tasks()

        for form in all_tasks:
            # Check if form has no ID
            if form.get('agentTask', None) and not form['agentTask'].get('id', None):
                result.append(form)

        return result

    def _get_new_local_agent_tasks_paths(self) -> List[str]:
        """
        Returns absolute paths of all new (without IDs) AgentTasks
        :return: a list of paths
        """
        filepaths = []

        # For every _service folder
        for entity in os.listdir(self.services_abs_path):
            if not entity.endswith('_service'):
                continue

            service_folder = os.path.join(self.services_abs_path, entity)

            # Get agent's AgentDataID
            CONFIG_PARSER.clear()
            CONFIG_PARSER.read(os.path.join(service_folder, 'settings.conf'))

            # Generate forms absolute path
            forms_abs_path = os.path.join(self.services_abs_path, entity, 'agent_tasks')

            if not os.path.exists(forms_abs_path):
                continue

            # Add every form to the result
            for form in os.listdir(forms_abs_path):
                if not form.endswith('.json'):
                    continue

                # Add the form to the result list
                form_abs_path = os.path.join(forms_abs_path, form)
                with open(form_abs_path, 'r') as file:
                    form_data: Dict = json.load(file)
                    if not form_data['agentTask'].get('id', None):
                        filepaths.append(os.path.join(entity, 'agent_tasks', form))

        return filepaths

    def _get_remote_agent_tasks(self) -> [Dict, None]:
        """
        Returns all the AgentTasks a user has access to
        :return: None or a dict where a key is an agent_data_id and a value is a list of tasks
        """
        agent_tasks = dict()

        local_configs = self._get_agents_configs_local()
        platform_access = PlatformAccess(LOGIN, PASSWORD)
        user_id = platform_access.get_user_id()

        # Execute GET-request to get AgentData
        response = make_request(platform_access=platform_access,
                                http_method='GET',
                                url_postfix='agentdata',
                                detail='agentsData')
        if not response:
            return None
        data = response.json()
        if 'agentsData' in data:
            for agent in data['agentsData']:
                if user_id != str(agent['agentsUser']['id']):
                    continue
                for config in local_configs.values():
                    agent_name = config['agentData']['name']
                    credentials = self.find_agent_credentials(agent_name)
                    if not credentials[0]:
                        continue

                    # Add AgentTasks to the dictionary
                    agent_tasks[f'{agent["id"]}'] = agent['agentTasks'], credentials, agent_name

        return agent_tasks

    # ---------------------------------------

    def run(self) -> None:
        """Runs CLI"""

        # Open the menu
        self.main_menu.open()


if __name__ == "__main__":
    EngineMenu().run()
