FROM node:22-alpine AS web-build
WORKDIR /app
COPY package.json package-lock.json ./
COPY frontend/package.json ./frontend/package.json
RUN npm ci --workspace @quanta/frontend
COPY frontend ./frontend
COPY content/catalog ./content/catalog
RUN npm run build

FROM nginxinc/nginx-unprivileged:stable-alpine AS web
COPY frontend/deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=web-build /app/frontend/dist /usr/share/nginx/html
EXPOSE 8080
HEALTHCHECK --interval=20s --timeout=3s CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
