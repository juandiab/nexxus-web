FROM nginx:1.25-alpine

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy SSL certificates (wildcard.nexxus-tech.com)
COPY ssl/ /etc/nginx/ssl/

# Remove default site config
RUN rm -f /etc/nginx/conf.d/default.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
