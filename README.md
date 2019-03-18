# Hello world Agent

This a Hello world Agent that is meant to be used as a template in the OWN.space hackathon.
You can enhance it to implement your own functionality.

# Clone the source code
`git config user.name "Your Name"`
`git config user.email your@mail.com`

`cd` to the directory you want to clone own-agent code
`git clone https://github.com/own-dev/own-agent`

# Add necessary environment variables to .bashrc
! Note: if you are deploying the system for development and/or testing purposes,
please use test account credentials for all the agents
```
export OWN_AGENTS_PATH="/opt/own-agent" # where opt is the directory you cloned own-agent code to
export PYTHONPATH="$OWN_AGENTS_PATH:$OWN_AGENTS_PATH/agents_platform:$OWN_AGENTS_PATH/agents:$OWN_AGENTS_PATH/agents/news:$OWN_AGENTS_PATH/agents/ip:$OWN_AGENTS_PATH/agents/science:$OWN_AGENTS_PATH/agents_platform/own_adapter"
export OWN_AGENT_ADDRESS="http://alpha.own.space/" # Change to http://0.0.0.0:9002/ to test with local backend
export OWN_PLATFORM_PREFIX=""
export OWN_PLATFORM_PROTOCOL="ws"
export OWN_TEST_LOGIN="{SPECIFY_LOGIN_FROM_ALPHA.OWN.SPACE}"
export OWN_TEST_PASSWORD="{SPECIFY_PASSWORD_FROM_ALPHA.OWN.SPACE}"
export OWN_TEST_AGENT_LOGIN="{SPECIFY_LOGIN_FROM_ALPHA.OWN.SPACE}"
export OWN_TEST_AGENT_PASSWORD="{SPECIFY_LOGIN_FROM_ALPHA.OWN.SPACE}"
export REDIS_ADDRESS="127.0.0.1"
export REDIS_PORT="6379"
export USE_LOCAL_IP="True"
```

Authenticate to google cloud from your local machine:
https://googleapis.github.io/google-cloud-python/latest/core/auth.html

# Activate virtual environment

`source $OWN_AGENTS_PATH/ownenv/bin/activate`

# Deploy
`./own-agent/deployment.sh`

# Run
1. `cd own-agent`
2. Start all the agents in background
    1. by script, running `screen python3 agents_starter.py`
    2. manually, like `nohup python3 agents/{agent_name}/api.py &`
3. Start the agents platform engine (`python3 agents_platform/engine.py &`)
