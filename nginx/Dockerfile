FROM nginx:stable-alpine

# Copy Nginx configuration (certs mounted at runtime — see docker-compose.yml)
COPY nginx.conf /etc/nginx/nginx.conf

# Remove default site config
RUN rm -f /etc/nginx/conf.d/default.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
