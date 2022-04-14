#!/usr/bin/env bash

set -e

PYTHONPATH=servers/pypy-falcon gunicorn \
    -w 1 \
    -b 0.0.0.0:9001 \
    app:app
