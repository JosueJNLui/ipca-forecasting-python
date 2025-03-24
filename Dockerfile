# [Choice] python version
ARG VARIANT="3.12"
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# Poetry
ARG POETRY_VERSION="none"
RUN if [ "${POETRY_VERSION}" != "none" ]; then su root -c "umask 0002 && pip3 install poetry==${POETRY_VERSION}"; fi
