#!/usr/bin/env bash

set -e

uvicorn \
    --workers 1 \
    --host 0.0.0.0 \
    --port 9001 \
    --app-dir /app/servers/python-uvicorn/ \
    app:app
