"""
Agents' platform core lifecycle
"""

import importlib
import importlib.util
import os
import threading
import time
from string import Template
from typing import List, Dict

from agents_platform.own_adapter.constants import AGENTS_PLATFORM_PATH, ENGINE_NAME, AGENTS_ENVIRONMENT
from utils import logger
from utils.credentials_store import set_in_use_parameters_to_false

SERVICES_PATH = 'services'
SERVICES_ABS_PATH = os.path.join(AGENTS_PLATFORM_PATH, SERVICES_PATH)
SERVICES_ALIVE_CHECK_TIME = 60


class AgentsPlatformEngine:
    """Agent-services engine"""

    def __init__(self):
        self.name = 'engine'
        self._blacklist = []
        self._services = {}
        self.services_folder_name = 'services'
        self.services_abs_path = os.path.join(AGENTS_PLATFORM_PATH, self.services_folder_name)
        if not os.path.exists(self.services_abs_path):
            os.mkdir(self.services_abs_path)

        self.class_name_template = '{name_titled}AgentService'  # Don't put f'' before! It will be used later

        # Engine's main loop
        self.services_thread = threading.Thread(target=self.start_services, args=(), daemon=True)
        self._run_event = threading.Event()

        if AGENTS_ENVIRONMENT == 'production':
            set_in_use_parameters_to_false()

    def is_running(self) -> bool:
        return self._run_event.is_set()

    def _toggle_engine(self):
        """Toggles the engine's main services loop"""
        print("TOGGLE")
        if self.is_running():
            self._stop_engine()
        else:
            self._run_engine()

    def _stop_engine(self):
        """Stops self.start_services"""
        print('Stopping the engine')
        self._run_event.clear()
        self.services_thread.join()

    def _run_engine(self):
        """Allows to run self.start_services"""
        logger.debug(ENGINE_NAME, 'Starting the engine')
        self._run_event.set()
        self.services_thread.start()

    # -------------
    # Blacklist
    def add_list_to_blacklist(self, service_names: List[str]) -> None:
        """Adds list of service names to a blacklist"""
        for service_name in service_names:
            self._blacklist.append(service_name)

    def add_to_blacklist(self, service_name: str) -> None:
        """Adds new service to a blacklist"""
        self._blacklist.append(service_name)

    def remove_from_blacklist(self, service_name: str) -> None:
        """Removes service from a blacklist"""
        self._blacklist.remove(service_name)

    @property
    def blacklist(self) -> List:
        """Getter"""
        return self._blacklist

    @blacklist.setter
    def blacklist(self, value: List) -> None:
        self._blacklist = value
    # -------------

    # -------------
    # Services
    def add_new_service(self, service_name: str, port: int) -> None:
        """Generates new agent-service with respect to the file structure"""
        if not (service_name and port):
            return None

        package_name = f'{service_name}_service'
        new_package_path = os.path.join(self.services_abs_path, package_name)

        if not os.path.exists(new_package_path):
            # Create service directory
            os.mkdir(new_package_path)

            # Create __init__.py
            with open(os.path.join(new_package_path, '__init__.py'), 'w') as init_file:
                init_file.write('\n')

            # Create config
            with open(os.path.join(new_package_path, 'settings.conf'), 'w') as config_file:
                with open('settings_template', 'r') as template_file:
                    src = Template(template_file.read())
                    data = {'name': service_name, 'redis_name': service_name + '_agent', 'port': port}
                    config_file.write(src.substitute(data))

            # Create *_service.py
            with open(os.path.join(new_package_path, package_name + '.py'), 'w') as service_file:
                with open('service_template', 'r') as template_file:
                    src = Template(template_file.read())
                    data = {'class_name': self.class_name_template.format(name_titled=service_name.title())}
                    service_file.write(src.substitute(data))

            # Create agent_tasks folder with default Form
            agent_tasks_path = os.path.join(new_package_path, 'forms')
            os.mkdir(agent_tasks_path)
            with open(os.path.join(new_package_path, 'default_agent_task.json'), 'w') as default_form_file:
                with open('default_agent_task.json', 'r') as template_file:
                    src = Template(template_file.read())
                    data = {'name': service_name, 'redis_name': f'{service_name}_agent', 'port': port}
                    default_form_file.write(src.substitute(data))

            logger.info(self.name, f'{service_name}-agent is successfully added.')
            logger.info(self.name,
                        'Do not forget to add environment variables: '
                        'OWN_{name}_AGENT_LOGIN and OWN_{name}_AGENT_PASSWORD'
                        .format(name=service_name.upper()))
        else:
            # TODO: Generate files if some of them are missing?
            pass

    def get_services(self) -> Dict:
        """
        Reads all the services from the file system,
        :return:
        """
        imported_services = {}
        services = {}

        for entity in os.listdir(self.services_abs_path):
            # Find *_service directories
            if entity.endswith('_service'):
                service_path = os.path.join(self.services_abs_path, entity)

                # Get all the service-modules
                for file in os.listdir(service_path):
                    # Find *_service module
                    if file.endswith('_service.py'):
                        # Import service module
                        path_to_module = os.path.join(service_path, file)
                        service_name = file.split('_')[0]
                        if service_name not in self._blacklist:
                            new_module_spec = importlib.util.spec_from_file_location(service_name,
                                                                                     path_to_module)
                            new_module = importlib.util.module_from_spec(new_module_spec)
                            new_module_spec.loader.exec_module(new_module)
                            imported_services[service_name] = {'module': new_module,
                                                               'path': path_to_module}
        # Generate all the agent-services
        for name, service in imported_services.items():
            try:
                module = service['module']
                class_name = self.class_name_template.format(name_titled=name.title())
                new_class = getattr(module, class_name)
                new_config_path = os.path.join(os.environ['OWN_AGENTS_PATH'],
                                               'agents_platform',
                                               service['path']
                                               ).replace(f'{name}_service.py', 'settings.conf')
                services[name] = (new_class(new_config_path))
            except Exception as excpt:
                logger.error(self.name,
                             f'Importing {name}-agent-service module is failed: {excpt}')
                continue

        self._services = services
        return services

    def start_services(self) -> None:
        """Starts all the agent-services"""
        # Prepare separate threads for each agent-service
        threads = {}
        for service in self._services:
            threads[service] = None

        # Run them each minute
        while True:
            for key, service in self._services.items():
                # Check it in run-time
                if service.name in self.blacklist:
                    continue

                if threads[key] is None or not threads[key].is_alive():
                    try:
                        threads[key] = threading.Thread(target=service.run,
                                                        name=service.thread_names['service'],
                                                        args=[], daemon=True)
                        threads[key].start()
                    except Exception as excpt:
                        logger.exception(self.name,
                                         'Could not start {} service. Exception message: {}'
                                         .format(service, str(excpt)))
            time.sleep(SERVICES_ALIVE_CHECK_TIME)

    # -------------


def main():
    engine = AgentsPlatformEngine()

    # Reads the local services from file system
    engine.get_services()

    # Starts all the found services
    engine.start_services()


if __name__ == '__main__':
    main()
