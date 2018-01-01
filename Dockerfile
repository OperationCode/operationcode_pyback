# Dockerfile
#FROM python:3
FROM python:3

ENV PYTHONUNBUFFERED 1

# Create app directory
RUN mkdir /code
WORKDIR /code

# Install app dependencies
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

EXPOSE 5000
