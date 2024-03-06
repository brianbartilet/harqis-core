# Use an official Python runtime as a parent image as interpreter
FROM python:3.10-alpine

# Create a mount point for the volume
VOLUME /app/data

# Set the working directory in the container
WORKDIR /app

# run command if interpreter is installed on windows machine
COPY requirements.txt .

RUN apk add gcc python3-dev musl-dev linux-headers

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install  --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt