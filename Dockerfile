FROM python:3-alpine
MAINTAINER Edwin Matthijssen  <edwin.matthijssen@tno.nl>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt .

# https://stackoverflow.com/questions/46711990/error-pg-config-executable-not-found-when-installing-psycopg2-on-alpine-in-dock
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . .
ENV PYTHONPATH=.:/usr/src/app
EXPOSE 4002

CMD cd /usr/src/app && python3 boundaryservice.py