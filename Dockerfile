# set arguments for the dockerfile
ARG PYTHON_VERSION=3.12
ARG ENV_ROOT_DIRECTORY="/usr/src/app"
ARG ENV="TEST"
# use an official Python runtime as a parent image as interpreter
FROM python:${PYTHON_VERSION}-alpine
# add git to the image
RUN apk update && apk add git

# create a mount point for the volume
VOLUME /app/data

# set the working directory in the container
WORKDIR /app/core

# copy files
COPY core/. .

# install dependencies
RUN apk add gcc python3-dev musl-dev linux-headers

# load virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# install packages
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# run the tests
ENV ENV_ROOT_DIRECTORY ${ENV_ROOT_DIRECTORY}
ENV ENV ${ENV}
CMD ["pytest"]

