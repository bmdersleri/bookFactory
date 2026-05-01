FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PUPPETEER_CACHE_DIR=/usr/local/share/puppeteer \
    BOOKFACTORY_MERMAID_CLI_VERSION=10.9.1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        git \
        graphviz \
        openjdk-17-jdk \
        pandoc \
        nodejs \
        npm \
        zip \
        unzip \
    && npm config set fund false \
    && npm config set audit false \
    && npm install -g @mermaid-js/mermaid-cli@${BOOKFACTORY_MERMAID_CLI_VERSION} puppeteer \
    && npx puppeteer browsers install chrome-headless-shell \
    && chmod -R a+rX /usr/local/share/puppeteer \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/BookFactory
