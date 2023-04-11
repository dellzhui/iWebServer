#!/bin/bash

cd "`dirname $0`"
CURDIR="`pwd`"

run_server()
{
    cd "${CURDIR}"
    while [ 1 ];do
        python manage.py runserver --insecure "${IDMS_APP_LISTENER_ADDRESS}:${IDMS_APP_LISTENER_PORT}"
        sleep 5
    done
}

run_server
