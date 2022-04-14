#!/usr/bin/env bash
#
# Builds one of the server Docker image on remote
#
# Arguments:
#   Remote host, an IP or hostname
#   Path to Dockerfile, a path

set -e

# parse input

remote=$1
echo "remote=${remote}"

server_name=$2
echo "server_name=${server_name}"

# create model artifacts

mkdir -p models
python3 scripts/generate_model.py

# scp

rsync -ar servers/ "${remote}:~/servers"
rsync -ar scripts/ "${remote}:~/scripts"
rsync -ar models/ "${remote}:~/models"

# build

ssh "${remote}" "
    sudo docker rm -f ${server_name}
    sudo docker build -t ${server_name} -f ~/servers/${server_name}/Dockerfile .
    sudo docker run -p 9001:9001 -d --name ${server_name} ${server_name}
    curl \
        --retry-all-errors \
        --connect-timeout 5 \
        --max-time 10 \
        --retry 5 \
        --retry-delay 0 \
        --retry-max-time 40 \
        -i "http://localhost:9001/"

    printf '%*s\n' "$(tput cols)" '' | tr ' ' -
    sudo docker logs ${server_name}
    printf '%*s\n' "$(tput cols)" '' | tr ' ' -

    ab \
        -p models/req.json \
        -T application/json \
        -c 2 \
        -n 10000 \
        -q \
        "http://localhost:9001/predict"
    sudo docker rm -f ${server_name}
"
