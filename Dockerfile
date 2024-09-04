# syntax=docker/dockerfile:1
FROM python:3.12-alpine

ADD main.py /
ADD requirements.txt /

RUN pip3 install -r requirements.txt

RUN mkdir /data

CMD [ "python", "./main.py" ]