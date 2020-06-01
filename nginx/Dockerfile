##########################
###### BUILD STAGE #######
##########################

FROM node:14.3.0-alpine as build-stage
WORKDIR /app/
COPY frontend/package*.json /app/
RUN npm install
COPY frontend /app/
RUN npm run build


##########################
#### PRODUCTION STAGE ####
##########################

FROM nginx:1.18.0-alpine as production-stage
COPY nginx/nginx_prod.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/dist /dist/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
