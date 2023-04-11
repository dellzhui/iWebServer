#!/bin/bash

cd "`dirname $0`"
CURDIR="`pwd`"

init_env()
{
    export PYTHONPATH=/home/yang/data/libs:${PYTHONPATH}
}

run_server()
{
    cd "${CURDIR}"
    while [ 1 ];do
        python manage.py runserver --insecure "${IDMS_APP_LISTENER_ADDRESS}:${IDMS_APP_LISTENER_PORT}"
        sleep 5
    done
}

init_env
run_server
