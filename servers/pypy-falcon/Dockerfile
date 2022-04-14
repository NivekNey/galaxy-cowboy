FROM pypy:3

RUN pip install falcon gunicorn

COPY servers /app/servers
COPY models /app/models

WORKDIR /app/

ENTRYPOINT ["bash", "servers/pypy-falcon/serve.sh"]