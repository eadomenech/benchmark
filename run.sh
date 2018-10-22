#!/bin/bash

source env/bin/activate
pip install -r src/requirements.txt
#lessc src/less/style.less > src/static/css/style.css
cd src
python manage.py runserver
deactivate
