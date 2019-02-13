FROM python:3.7-alpine AS intelreaper

MAINTAINER Wyatt Roersma <wyatt@aucr.io>

COPY requirements.txt /opt/intelreaper
COPY intelreaper /opt/intelreaper

WORKDIR /opt/intelreaper

RUN apk update
RUN apk upgrade

COPY ircli.py /opt/intelreaper
COPY LICENSE /opt/aucr
COPY projectinfo.yml /opt/aucr
COPY intelreaper/config.py /opt/aucr

