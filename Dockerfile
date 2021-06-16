FROM python:3-alpine
MAINTAINER Edwin Matthijssen  <edwin.matthijssen@tno.nl>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt .

# https://stackoverflow.com/questions/62343455/use-asyncpg-python-module-in-alpine-docker-image
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps build-base postgresql-dev && \
 pip3 install asyncpg && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . .
ENV PYTHONPATH=.:/usr/src/app
EXPOSE 4002

CMD cd /usr/src/app && python3 boundaryservice.py
