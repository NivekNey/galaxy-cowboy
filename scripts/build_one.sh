#!/usr/bin/env bash
#
# Builds one of the server Docker image on remote
# I use colima + containerd
# `colima start --cpu 4 --memory 8`
#
# Arguments:
#   Remote host, an IP or hostname
#   Path to Dockerfile, a path

set -e

# parse input

name=$1
echo "name=${name}"

# create model artifacts

mkdir -p models
python3 scripts/generate_model.py

# build

nerdctl rm -f ${name} || true
nerdctl network remove foo || true
nerdctl network create foo
nerdctl build -t ${name} -f servers/${name}/Dockerfile .
nerdctl run --net=foo -p 9001:9001 -d --name ${name} ${name}
nerdctl run --net=foo -v ./scripts:/scripts -v ./models:/models --rm python:3 python3 -u /scripts/measure.py ${name}
nerdctl rm -f ${name}
