FROM python:3

RUN pip install fastapi uvicorn[standard] gunicorn

COPY servers /app/servers
COPY models /app/models

WORKDIR /app/

ENTRYPOINT ["bash", "servers/python-fastapi/serve.sh"]
