# set arguments for the dockerfile
ARG PYTHON_VERSION=3.12
ARG ENV_ROOT_DIRECTORY="/app/core"
ARG ENV="TEST"

# set the base image for the container
# use an official Python runtime as a parent image as interpreter
FROM python:${PYTHON_VERSION}-alpine AS base
# add git to the image
RUN apk update && apk add git

# set the working directory in the container
WORKDIR /app/core

# copy files
COPY core/. .

# create a mount point for the volume
VOLUME /app/data

# install dependencies
RUN apk add gcc python3-dev musl-dev linux-headers

# load virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# install packages
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# install Chromium for testing webdrivers
# RUN apk update && apk add --no-cache chromium

# Setting Chromium as the default browser for compatibility with tools expecting "google-chrome" or similar
# RUN ln -s /usr/bin/chromium-browser /usr/bin/google-chrome

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