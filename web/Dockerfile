FROM python:3.9.1-alpine3.12 as build-image

WORKDIR '/app'

RUN apk add --no-cache linux-headers g++ git

COPY webapp/requirements.txt ./

RUN pip wheel --wheel-dir=/root/wheels -r requirements.txt



FROM python:3.9.1-alpine3.12 as production-image

WORKDIR '/app'

RUN apk add git

COPY --from=build-image /root/wheels /root/wheels

COPY --from=build-image /app/requirements.txt ./

RUN pip install --no-index --find-links=/root/wheels -r requirements.txt

COPY ./ ./

RUN addgroup -S uwsgi && adduser -S uwsgi -G uwsgi

USER uwsgi