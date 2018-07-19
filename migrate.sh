#!/bin/bash

message=$1

export LC_ALL=en_US.utf8
export LANG=en_US.utf8
export FLASK_APP=run.py
export FLASK_DEBUG=1
flask db migrate -m "$message"
