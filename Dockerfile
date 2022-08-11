# syntax=docker/dockerfile:1
FROM python:3.9-alpine

ADD main.py /

RUN pip3 install httpx beautifulsoup4

RUN mkdir /data


CMD [ "python", "./main.py" ]