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
        IWEBSERVER_LOG_FILENAME="mqtt_subscriber_service.log" python standalong/mqtt_subscriber_service/main.py
        sleep 5
    done
}

init_env
run_server
