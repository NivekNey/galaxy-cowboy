FROM rust:1

COPY servers /app/servers
COPY models /app/models

RUN cd /app/servers/rust-actix/ && \
    cargo build

WORKDIR /app/

ENTRYPOINT ["/app/servers/rust-actix/target/debug/rust-actix"]
