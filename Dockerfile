# set arguments for the dockerfile
ARG PYTHON_VERSION=3.12
ARG ENV_ROOT_DIRECTORY="/app/core"
ARG ENV="TEST"

# set the base image for the container
# use an official Python runtime as a parent image as interpreter
FROM python:${PYTHON_VERSION}-slim AS base
RUN apt-get update && apt-get install -y git

# set the working directory in the container
WORKDIR /app/core

# copy files
COPY core/. .

# create a mount point for the volume
VOLUME /app/data

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    linux-headers-generic \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# l=Load virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python packages
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# run the tests
RUN sh /app/core/demo/scripts/set_env.sh
ENV GH_TOKEN ${GH_TOKEN}
ENV ENV_ROOT_DIRECTORY ${ENV_ROOT_DIRECTORY}
ENV ENV ${ENV}

ENV PATH="/app:${PATH}"
ENV PYTHONPATH="/app:/app/core:app/core/demo"

# ENV WDM_LOCAL=1

CMD ["pytest"]


FROM base as apps
WORKDIR /app/core/apps
RUN sh ../demo/scripts/set_env.sh
ENV WORKFLOW_CONFIG="demo.workflows.__tpl_workflow_builder.config"
CMD ["pytest"]


ARG WORKFLOW_CONFIG="demo.workflows.__tpl_workflow_builder.config"
FROM base as scheduler
COPY core/demo/workflows .
VOLUME /app
WORKDIR /app/core/demo/workflows

ENV WORKFLOW_CONFIG=${WORKFLOW_CONFIG}
CMD ["python", "run_tasks.py", "scheduler"]


ARG WORKFLOW_CONFIG="demo.workflows.__tpl_workflow_builder.config"
FROM base as worker
COPY core/demo/workflows .
VOLUME /app
WORKDIR /app/core/demo/workflows

ENV WORKFLOW_CONFIG=${WORKFLOW_CONFIG}
CMD ["python", "run_tasks.py", "worker"]