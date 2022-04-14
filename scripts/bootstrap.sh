#!/usr/bin/env bash
#
# Bootstrap the remote
#
# Arguments:
#   Remote host, an IP or hostname

set -e

remote=$1
echo "remote=${remote}"

ssh "${remote}" '
    sudo apt-get update -y
    sudo apt-get install -y \
        rsync\
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update -y
    sudo apt-get install -y \
        docker-ce \
        docker-ce-cli \
        containerd.io
    sudo apt-get install -y \
        apache2-utils
'
