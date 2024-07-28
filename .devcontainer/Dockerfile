ARG VARIANT=3.12-bookworm
ARG VESPA_CLI_VERSION=8.367.14
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

ENV PYTHONUNBUFFERED 1
ENV TZ Asia/Tokyo

# vespa-cliのインストール
RUN curl -L -o .bin/vespa-cli.tar.gz https://github.com/vespa-engine/vespa/releases/download/v${VESPA_CLI_VERSION}/vespa-cli_${VESPA_CLI_VERSION}_linux_amd64.tar.gz \
    tar -xvf .bin/vespa-cli.tar.gz -C .bin \
    mv .bin/vespa-cli_${VESPA_CLI_VERSION}_linux_amd64/bin/vespa .bin/vespa \
    rm .bin/vespa-cli.tar.gz \
    rm -rf .bin/vespa-cli_${VESPA_CLI_VERSION}_linux_amd64