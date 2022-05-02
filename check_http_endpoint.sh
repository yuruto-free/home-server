#!/bin/bash

{
    echo light        on
    echo light        off
    echo light        night
    echo light        up
    echo light        down
    echo light        all
    echo electric-fan on
    echo electric-fan off
    echo electric-fan up
    echo cooler       on
    echo cooler       off
    echo heater       on
    echo heater       off
    echo dry          on
    echo dry          off
} | while read linkName command; do
    data='{"payload":"'${command}'"}'
    url="http://raspberrypi.local:1880/${linkName}"
    option='" status code:%{http_code}\n"'
    cmd="curl -X POST -H 'Content-Type: application/json' -d '${data}' ${url} -w ${option}"
    echo link name: ${linkName}, command: ${command}
    eval ${cmd}
    echo
    sleep 1
done
