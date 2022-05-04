FROM node:16-alpine3.11
ARG TZ="Asia/Tokyo"

ENV WORK_ROOT_DIR=/home/node/app

LABEL maintainer="yuruto"

# install basic software
RUN    apk update \
    && apk add --no-cache bash tzdata \
    && cp /usr/share/zoneinfo/${TZ} /etc/localtime \
    && mkdir -p ${WORK_ROOT_DIR} \
    && mkdir -p /var/log/express \
    && mkdir -p /home/node/src \
    && rm -rf /root/.cache /var/cache/apk/*

WORKDIR ${WORK_ROOT_DIR}

COPY ./package.json ${WORK_ROOT_DIR}/package.json
RUN npm install

CMD ["npm", "start"]
