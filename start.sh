#!/bin/bash

export APP_CONFIG_FILE=/home/fabian-b/metadata-initiative.cs.fiu.edu/config/development.py
export LC_ALL=en_US.utf8
export LANG=en_US.utf8
export FLASK_APP=run.py
export FLASK_DEBUG=1
export FLASK_ENV=development
flask run --host=0.0.0.0
