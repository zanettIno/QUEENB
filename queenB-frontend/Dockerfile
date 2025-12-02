# Build Angular
FROM node:20-alpine AS build

WORKDIR /app

COPY QueenB-Front/package*.json ./

RUN npm install

COPY QueenB-Front/ .

RUN npm run build -- --configuration=production

FROM nginx:alpine

# Desativa o envsubst responsável por quebrar as variáveis do nginx
RUN rm /docker-entrypoint.d/20-envsubst-on-templates.sh

RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /app/dist/queen-b/browser /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]