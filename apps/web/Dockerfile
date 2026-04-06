FROM node:22-alpine

ENV CYPRESS_INSTALL_BINARY=0

WORKDIR /app

COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
COPY apps/web/package.json /app/apps/web/package.json

RUN npm ci --include=dev

COPY apps/web /app/apps/web

WORKDIR /app/apps/web

RUN npm run build

ENV NODE_ENV=production

EXPOSE 3000

CMD ["npm", "run", "start"]
