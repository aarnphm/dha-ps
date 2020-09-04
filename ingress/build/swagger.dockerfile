FROM swaggerapi/swagger-ui

COPY docs/swagger.yml /usr/share/nginx/html/swagger.yml
