#!/usr/bin/env bash

set -e

gunicorn -w 4 -b 0.0.0.0:9001 app:app
