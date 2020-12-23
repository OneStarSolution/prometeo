# pull official base image
FROM python:3.9-slim-buster

# Create and set the working directory to /app
RUN mkdir -p /app
WORKDIR /app

# set environment variables

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc gnupg1 firefox-esr wget\
  && apt-get clean

RUN apt-get install -y libxml2-dev libxslt-dev python-dev

# Install geckodriver for Firefox
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.24.0-linux64.tar.gz -C /usr/local/share/ \
    && chmod +x /usr/local/share/geckodriver
    # && ln -s /usr/local/share/geckodriver /app

# install python dependencies
# RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app