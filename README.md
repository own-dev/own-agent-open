# OWN.space Agents Platform

This an open version of OWN.space agent platform,
with a demo Jokes Agent code that is meant to be used as a template during the development of other Agents.
You can enhance it to implement your own functionality.

Explanation of the repository structure, platforms operation, and of how to create an Agent can be found here:
https://docs.google.com/presentation/d/1GOfc-5S05ART9Z2lXqx2HKfQXpd-rfCxP65jW6tWLtM/edit?usp=sharing

# Set Up
## Clone the source code
`git config user.name "Your Name"`

`git config user.email your@mail.com`

`cd` to the directory you want to clone own-agent code

`git clone https://github.com/own-dev/own-agent`

`cd own-agent`

Agents use firestore as a data storage and as a mediator between different instances of agents.
Please, create a new firebase project at https://firebase.google.com/,
and activate firestore in `Database - Cloud Firestore` section.

Authenticate to google cloud from your local machine,
where project-name will be a name of a newly created firebase project:
https://googleapis.github.io/google-cloud-python/latest/core/auth.html

## Add necessary environment variables to .bashrc
**Note**: if you are deploying the system for development and/or testing purposes,
it is advised to use test account credentials for all the agents
```
export OWN_AGENTS_PATH="/opt/own-agent" # where opt is the directory you cloned own-agent code to
export PYTHONPATH="$OWN_AGENTS_PATH:$OWN_AGENTS_PATH/agents_platform:$OWN_AGENTS_PATH/agents:$OWN_AGENTS_PATH/agents/news:$OWN_AGENTS_PATH/agents/ip:$OWN_AGENTS_PATH/agents/science:$OWN_AGENTS_PATH/agents_platform/own_adapter"
export OWN_AGENT_ADDRESS="http://alpha.own.space:9000" # Change to http://0.0.0.0:9002/ to test with local backend
export OWN_PLATFORM_PREFIX=""
export OWN_PLATFORM_PROTOCOL="ws"
export OWN_TEST_LOGIN="{SPECIFY_LOGIN_FROM_ALPHA.OWN.SPACE}" # Login of a user registered at http://alpha.own.space
export OWN_TEST_PASSWORD="{SPECIFY_PASSWORD_FROM_ALPHA.OWN.SPACE}"
export OWN_TEST_AGENT_LOGIN="{SPECIFY_LOGIN_FROM_ALPHA.OWN.SPACE}"
export OWN_TEST_AGENT_PASSWORD="{SPECIFY_LOGIN_FROM_ALPHA.OWN.SPACE}"
export REDIS_ADDRESS="127.0.0.1"
export REDIS_PORT="6379"
export USE_LOCAL_IP="True"
export GOOGLE_CLOUD_PROJECT_NAME="{GOOGLE_CLOUD_PROJECT_NAME}" # name of the firebase project, created at https://firebase.google.com/
export CREDENTIALS_DB_KEY="credentials_test"
```

## Deploy
`./deployment.sh`

## Activate virtual environment

`source $OWN_AGENTS_PATH/ownenv/bin/activate`

## Run
1. Start all the agents in background
    1. by script, running `screen python3 agents_starter.py`
    2. manually, like `nohup python3 agents/{agent_name}/api.py &`
2. Start the agents platform engine (`python3 agents_platform/engine.py &`)