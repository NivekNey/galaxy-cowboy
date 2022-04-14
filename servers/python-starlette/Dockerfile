FROM python:3

RUN pip install starlette uvicorn[standard] gunicorn

COPY servers /app/servers
COPY scripts /app/scripts
COPY models /app/models

WORKDIR /app/

ENTRYPOINT ["bash", "servers/python-starlette/serve.sh"]