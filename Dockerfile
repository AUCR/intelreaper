FROM python:3.7-alpine AS intelreaper

MAINTAINER Wyatt Roersma <wyatt@aucr.io>
WORKDIR /opt/intelreaper

RUN apk update
RUN apk upgrade

COPY . /tmp/intelreaper

RUN apk add --no-cache -t build_req \
    gcc \
    g++ \
    && cd /tmp/intelreaper/ \
    && pip install -r requirements.txt \
    && python setup.py install \
    && apk del --purge build_req

RUN rm -rf /tmp/intelreaper
RUN adduser -DH -s /sbin/nologin intelreaper \
    && chown -R intelreaper:intelreaper /opt/intelreaper
USER intelreaper
CMD ["ircli.py", "--plugin", "json", "--volume", "/opt/intelreaper/inteljson/"]
