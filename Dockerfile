FROM alpine:3.10
ENV PYTHONUNBUFFERED=1
RUN apk add py3-pip py3-psycopg2
ADD . /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
