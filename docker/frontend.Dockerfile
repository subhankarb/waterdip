FROM node:16.17.0

RUN set -ex; \
    apt-get update \
    && apt-get -y install --no-install-recommends build-essential=* python-dev=* make=* \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 4433
WORKDIR /app

COPY frontend/package*.json ./
RUN npm cache clean --force
RUN npm cache verify
RUN npm install --force

COPY ./frontend/src ./src
COPY ./frontend/public ./public
COPY ./frontend/babel.config.js ./babel.config.js
COPY ./frontend/tsconfig.json ./tsconfig.json

CMD ["sh","-c","npm run build && npm run serve"]
