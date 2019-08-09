FROM node:8.15.0-alpine

WORKDIR /opt/app

RUN npm install http-server -g

COPY package.json yarn.lock /tmp/

RUN if [ ! diff -q yarn.lock /tmp/yarn.lock > /dev/null  2>&1 ]; then cp /tmp/yarn.lock yarn.lock; fi

RUN cd /tmp && yarn
RUN mkdir -p /opt/app && cd /opt/app && ln -s /tmp/node_modules

COPY . /opt/app
RUN rm -rf /opt/app/dist