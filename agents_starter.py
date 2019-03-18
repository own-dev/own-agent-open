import atexit
import datetime
import os
import subprocess
import threading
from _signal import SIGINT
from time import sleep

from agents.agents_utils.agents_helper import execute_function_in_parallel
from utils.constants import ACTUAL_AGENTS_PATH, AGENTS_PATH, DOWNLOADS_DIR

HANDLER_COUNT_KEY = 'handler_count'
AGENTS_COUNT_KEY = 'agents_count'
agents_to_start = {
    'jokes': {
        HANDLER_COUNT_KEY: 1,
        AGENTS_COUNT_KEY: 1,
    }
}

processes = []


def start_agents():
    """
    Start agent and agent handlers APIs 
    :return: Nothing
    """
    for agent_name, agent_props in agents_to_start.items():
        for i in range(agent_props.get(AGENTS_COUNT_KEY, 0)):
            processes.append(subprocess.Popen(['python3', os.path.join(ACTUAL_AGENTS_PATH, agent_name,
                                                                       'api.py')]))
        for i in range(agent_props.get(HANDLER_COUNT_KEY, 0)):
            processes.append(subprocess.Popen(['python3', os.path.join(ACTUAL_AGENTS_PATH, agent_name,
                                                                       'agent_handler_api.py')]))


@atexit.register
def stop_agents():
    """
    Stop all agents at exit
    :return: Nothing
    """

    def stop_process(process):
        SLEEP_TIME = 10
        num_tries = 3

        process.send_signal(SIGINT)
        sleep(SLEEP_TIME)

        # while process is still alive and number of tries > 0
        while not process.poll() and num_tries > 0:
            process.send_signal(SIGINT)
            sleep(SLEEP_TIME)
            num_tries -= 1

        process.kill()

    execute_function_in_parallel(stop_process, [(process,) for process in processes])


def delete_old_files_from_downloads(max_file_age: int = 60 * 60 * 3):
    """
    Deletes old files from agents download directory
    :param max_file_age: max amount of seconds allowed between file modification time and current time
    :return: Nothing
    """
    SLEEP_TIME = 60

    while True:
        path_to_the_downloads_dir = os.path.join(AGENTS_PATH, DOWNLOADS_DIR)
        if os.path.exists(path_to_the_downloads_dir):
            for file in os.listdir(path_to_the_downloads_dir):
                file_path = os.path.join(path_to_the_downloads_dir, file)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    age_seconds = (datetime.datetime.now() -
                                   datetime.datetime.fromtimestamp(stat.st_mtime)).total_seconds()

                    if age_seconds > max_file_age:
                        os.unlink(file_path)
        sleep(SLEEP_TIME)


if __name__ == '__main__':
    # Remove files from agents downloads directory
    threading.Thread(target=delete_old_files_from_downloads, daemon=True).start()
    start_agents()
    threading.Event().wait()
