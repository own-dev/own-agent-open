#!/usr/bin/env bash

# apt installation
sudo apt-get install -y python-virtualenv
sudo apt-get install -y python-pip
sudo apt-get install -y libcurl4-openssl-dev
sudo apt-get install -y python-dev
sudo apt-get install -y build-essential
sudo apt-get install -y libpq-dev
sudo apt-get install -y python-tk
sudo apt-get install -y redis-server
sudo apt install python3-distutils
# libs for matplotlib
sudo apt-get install -y libfreetype6-dev
sudo apt-get install -y libpng12-dev
# uncomment the next string if you want to use redis-cli
# sudo apt-get install -y redis-tools
sudo apt-get install -y python3-tk
# GCC is required for building the wordcloud module
sudo apt-get install -y gcc
# Required for chromium in funding agent
sudo apt-get install libasound2 libasound2-plugins libnss3-dev
# To install Twisted
sudo apt install python3.6-dev build-essential libssl-dev libffi-dev

# locale to eliminate problems with installing virtual environment
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales

# install virtual environment
virtualenv -p python3 ownenv

# pip requirements
source ownenv/bin/activate
sudo pip install --upgrade setuptools
pip install -r own-agent/pip-requirements.txt

# if there are problems with installing the Pillow or wordcloud modules, please refer to
# https://stackoverflow.com/questions/34631806/fail-during-installation-of-pillow-python-module-in-linux
# also can try to run "sudo apt-get install python3-dev"

echo "add next lines to your ~/.bashrc file"
echo "export OWN_AGENTS_PATH=\"/srv/own-agent\" # where srv is the directory you cloned own-agent code to"
echo "export PYTHONPATH=\"$OWN_AGENTS_PATH:$OWN_AGENTS_PATH/agents_platform:$OWN_AGENTS_PATH/agents:$OWN_AGENTS_PATH/agents/news:$OWN_AGENTS_PATH/agents/ip:$OWN_AGENTS_PATH/agents/science:$OWN_AGENTS_PATH/agents_platform/own_adapter\""
echo "export OWN_AGENT_ADDRESS=\"http://alpha.own.space\" # Change to http://0.0.0.0:9002/ to test with local backend
echo "export OWN_PLATFORM_PREFIX=\"\""
echo "export OWN_PLATFORM_PROTOCOL=\"ws\""
echo "export OWN_TEST_LOGIN=\"{SPECIFY_LOGIN_FROM_ALPHA.OWN.SPACE}\""
echo "export OWN_TEST_PASSWORD=\"{SPECIFY_PASSWORD_FROM_ALPHA.OWN.SPACE}\""
echo "export OWN_TEST_LOGIN=\"{SPECIFY_LOGIN_FROM_ALPHA.OWN.SPACE}\""
echo "export OWN_TEST_PASSWORD=\"{SPECIFY_PASSWORD_FROM_ALPHA.OWN.SPACE}\""
echo "export REDIS_ADDRESS=\"127.0.0.1\""
echo "export REDIS_PORT=\"6379\""
echo "export USE_LOCAL_IP=\"True\""