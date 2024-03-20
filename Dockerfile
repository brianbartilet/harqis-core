# use an official Python runtime as a parent image as interpreter
FROM python:3.10-alpine
RUN apt-get update && apt-get install -y git

# create a mount point for the volume
VOLUME /app/data

# set the working directory in the container
WORKDIR /app/core

# run command if interpreter is installed on windows machine
COPY core/. .

# install dependencies
RUN apk add gcc python3-dev musl-dev linux-headers

# load virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# install packages
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# expose port 80
EXPOSE 80

# run the tests
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
CMD ["pytest"]