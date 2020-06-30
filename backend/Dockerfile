# pull official base image
FROM python:3.8.3-alpine

# set work directory
RUN mkdir /code
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# adding main packages
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libjpeg
RUN pip install --upgrade pip
RUN pip install --upgrade Pillow

# install dependencies
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# copy(add) script
COPY ./backend/scripts/start.sh /

# copy(add) project
ADD . /code/
