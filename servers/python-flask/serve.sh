#!/usr/bin/env bash

set -e

PYTHONPATH=servers/python-flask gunicorn \
    -w 1 \
    -b 0.0.0.0:9001 \
    app:app
