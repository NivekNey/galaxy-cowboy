#!/usr/bin/env bash

set -e

PYTHONPATH=servers/python-fastapi gunicorn \
    -w 1 \
    -b 0.0.0.0:9001 \
    --worker-class uvicorn.workers.UvicornWorker \
    app:app
