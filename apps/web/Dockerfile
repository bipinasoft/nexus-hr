FROM node:22-alpine

ARG NEXT_PUBLIC_API_BASE_URL=http://localhost:8007

ENV CYPRESS_INSTALL_BINARY=0
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

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
