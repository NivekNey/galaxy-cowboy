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
python scripts/generate_model.py

# scp

rsync -ar servers/ "${remote}:~/servers"
rsync -ar scripts/ "${remote}:~/scripts"
rsync -ar models/ "${remote}:~/models"

# build

ssh "${remote}" "
    sudo docker build -t ${server_name} -f ~/servers/${server_name}/Dockerfile .
    sudo docker run -p 9001:9001 --name ${server_name} ${server_name} &> log &
    timeout 10 grep -q 'Model loaded' <(tail -f log)
    ab \
        -p models/req.json \
        -T application/json \
        -c 8 \
        -n 10000 \
        "http://${remote}:9001/predict"
    sudo docker rm -f ${server_name}
"
