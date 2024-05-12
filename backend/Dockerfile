FROM python:3.10-alpine3.17
ARG packages
ARG ENVIRONMENT

RUN apk --update add ${packages} \
    && rm -rf /var/cache/apk/* \
    && pip3 install --upgrade pip pipenv wheel virtualenv

COPY . /app
WORKDIR /app

# -- Install dependencies:
RUN addgroup --system bracket && adduser --system bracket --ingroup bracket \
    && chown -R bracket:bracket /app
USER bracket

RUN set -ex \
    && pipenv install --deploy

ENV ENVIRONMENT=${ENVIRONMENT}

CMD pipenv run uvicorn bracket.app:app --host=0.0.0.0 --port=8400
