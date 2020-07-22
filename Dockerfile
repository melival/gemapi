FROM python:3.7-alpine3.12

ENV PUTHONUNBUFFERED=1

ADD . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt
