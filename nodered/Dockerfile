FROM nodered/node-red:2.2.2-12

LABEL maintainer="yuruto"

USER root
WORKDIR /usr/src/node-red

RUN    apk update \
    && apk add --no-cache shadow su-exec \
    && npm install node-red-contrib-alexa-home-skill \
    && rm -f /data/flows.json \
    && rm -rf /root/.cache /var/cache/apk/*

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENV NODE_UID=1000 \
    NODE_GID=20

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["npm", "start", "--cache", "/data/.npm", "--", "--userDir", "/data"]
