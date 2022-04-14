FROM debian:11

SHELL ["/bin/bash", "-c"] 

RUN apt-get update -y && \
    apt-get install -y curl unzip zip && \
    curl -o sdkman.sh https://get.sdkman.io && \
    bash sdkman.sh && \
    source "/root/.sdkman/bin/sdkman-init.sh" && \
    sdk install java && \
    sdk install maven

ENV PATH=/root/.sdkman/candidates/java/current/bin:$PATH
ENV PATH=/root/.sdkman/candidates/maven/current/bin:$PATH

COPY servers /app/servers
COPY models /app/models

RUN pushd /app/servers/java-jooby/ && \
    mvn clean package && \
    popd

WORKDIR /app/

ENTRYPOINT ["java", "-jar", "servers/java-jooby/target/java-jooby-1.0.jar", "server.port=9001"]