# use an official Python runtime as a parent image as interpreter
FROM python:3.10-alpine

# create a mount point for the volume
VOLUME /app/data

# set the working directory in the container
WORKDIR /app

# run command if interpreter is installed on windows machine
COPY requirements.txt .

# install dependencies
RUN apk add gcc python3-dev musl-dev linux-headers

# load virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# install packages
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt