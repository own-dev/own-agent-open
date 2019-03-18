# Pipeline
This document describes how Forms work from the agents' perspective.
Basically, AgentTask (the thing that has Form) looks like that (pic):
![AgentTask Structure](/docs/AgentTaskStructure.png)


## 0. LiveUpdate
Before agent-service receives any data to process, a User submits (or runs) specific AgentTask on some element.
Then _liveUpdateAgentTaskElementAnswersSaved_ is generated on the back-end and sent to specific agent-service (the one AgentTask belongs to).
What is important is we don't need to check if this very _liveUpdateAgentTaskElementAnswersSaved_ relates to our service-agent,
instead once we've got this LiveUpdate, we can start to work with right trough.


## 1. Agent-service
This section describes how agent-services interact with Forms

### Start-up
By the start of an agent-service, all the forms available are on the back-end.
To add new form either in run-time, or not, refer to [creation documentation](docs/FORMS_CREATION.md)

### Run-time
After our agent-service has received _liveUpdateAgentTaskElementAnswersSaved_, we can see the following data inside:
* **Board ID** on which a User submited the data using AgentTask for some element
* **Element ID** on which a User assigned AgentTask
* **AgentData ID**, i.e., the agent that is responsible for this AgentTask
* **AgentTask ID** of AgentTask a User assigned to the/an element


## 2. JSON Parsing
AgentTask's structure is described in [AgentTask's GET-request](https://own1.docs.apiary.io/#reference/agent-task-configurations/agentdataagentdataidagenttasksagenttaskidconfiguration/get).

### Extract LiveUpdate's Data
In `agents_platform/base_service.py::on_websocket_message()` agent-service receives these IDs from the web-socket message:
```python
def on_websocket_message(self, ws: websocket.WebSocketApp, message: str) -> None:
    """Processes web-socket's messages"""
    message_data = json.loads(message)
    message_type = message_data['contentType'].replace('application/vnd.uberblik.', '')

    if message_type == 'liveUpdateAgentTaskElementAnswersSaved+json':
        # Get the data from the
        agent_data_id = int(message_data['agentDataId'])
        agent_task_id = int(message_data['agentTaskId'])
        element_id = int(message_data['elementId'])
        board_id = int(message_data['boardId'])
```

### Grab User's Answers
In `on_websocket_message()` agent-service also gets User's answers for the AgentTask:
```python
    agent = self.get_agent()
    agent_task = get_agent_task_answers_by_id(agent.get_platform_access(),
                                              agent_data_id,
                                              agent_task_id,
                                              board_id,
                                              element_id)
```


## 3. Sending Data from Service to Agent
This part is unique for each agent.
In general, you need to know agent's (not agent-service's) URL and port to send a request in `agents_platform/base_service.py::run_on_element()`'s overriden function..
```python
from typing import List
import requests
from agent_platform.own_adapter.agent_task import get_answer_from_agent_task_answers

def _run_on_element(self, element: Element, agent_task: Dict = None) -> [Element, None]:
    # Get the data from some of IndexedInputFields:
    agent_task_answer_data = agent_task['agentTaskElement']['agentTask']
    answer: List = get_answer_from_agent_task_answers(agent_task_answers=agent_task_answer_data, answer_index=1)

    # Send the AgentTask data to get the results from an agent
    port = 5000
    response = requests.post(f'http://localhost:{port}/', data=answer[0])

    # Proceed the response from Agent, etc
```

## 4. Sending the Results Back to User
To send a file to the element you can use also in `_run_on_element()` something like:
```python
title = 'A Brand New File'
with open('absolute_or_relative_path_to_file', 'rb') as file:
    element.put_file(title, bytearray(file.read()))
```
or to send a message on the board:
```python
message = 'The task is done, Your Grace!'
element.get_board().put_message(message)
```
