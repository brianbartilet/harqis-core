# use an official Python runtime as a parent image as interpreter
FROM python:3.10-alpine
RUN apk update && apk add git

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


# run the tests
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
ENV ENV_ROOT_DIRECTORY "/usr/src/app"
ENV ENV "SYS"

CMD ["git", "--version"]
CMD ["pytest"]

# expose port 80
EXPOSE 80
