#!/bin/bash

source env/bin/activate
cd src
celery -A dwm worker --loglevel=info -f log.txt
deactivate
