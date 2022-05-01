FROM nodered/node-red:2.2.2-12

LABEL maintainer="yuruto"

USER root
WORKDIR /usr/src/node-red

RUN    npm install node-red-contrib-alexa-home-skill \
    && npm audit fix \
    && rm -f /data/flows.json

CMD ["npm", "start", "--cache", "/data/.npm", "--", "--userDir", "/data"]
