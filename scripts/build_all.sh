#!/usr/bin/env bash
#
# Build all the servers

set -e

ls -1 servers | xargs -I {} bash scripts/build_one.sh {} | tee log
