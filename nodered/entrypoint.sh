#!/bin/bash

# get node user information
uid=$(id node-red -u)
gid=$(id node-red -g)

# change GID
if [ ${NODE_GID} -ne ${gid} ]; then
    groupmod -g ${NODE_GID} dialout
    usermod -g dialout node-red
fi
# change UID
if [ ${NODE_UID} -ne ${uid} ]; then
    usermod -u ${NODE_UID} node-red &
    sleep 3
    pkill usermod
fi

# update owner
chown node-red:root /usr/src/node-red
chown node-red:root /usr/src/node-red/*
chown node-red:root /data
chown node-red:dialout /data/*
# execute process by node-red user
exec su-exec node-red:dialout "$@"
