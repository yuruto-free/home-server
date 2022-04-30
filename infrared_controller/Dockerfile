FROM node:16-alpine3.11
ARG TZ="Asia/Tokyo"

ENV PYTHONUNBUFFERED=1 \
    APP_ROOT_PATH=/infrared_controller

LABEL maintainer="yuruto"

# setup python
RUN    apk update \
    && apk add --no-cache bash tzdata python3 py3-smbus \
    && cp /usr/share/zoneinfo/${TZ} /etc/localtime \
    && ln -sf python3 /usr/bin/python \
    && python3 -m ensurepip \
    && rm -r /usr/lib/python*/ensurepip \
    && pip3 install --no-cache --upgrade pip setuptools wheel \
    && ln -sf pip3 /usr/bin/pip \
    && mkdir -p ${APP_ROOT_PATH} \
    && rm -rf /root/.cache /var/cache/apk/*

WORKDIR ${APP_ROOT_PATH}

CMD ["python", "-u", "/infrared_controller/irc.py"]
