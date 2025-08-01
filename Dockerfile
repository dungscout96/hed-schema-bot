FROM ghcr.io/berriai/litellm:main-latest

# Install AWS CLI inside the container
RUN apk add --no-cache aws-cli

# Set working directory
WORKDIR /app

# Copy startup script
COPY start.sh /app/start.sh
COPY all_hed_tags.txt /app/all_hed_tags.txt

# Make sure the script is executable
RUN chmod +x /app/start.sh

# Default entrypoint
ENTRYPOINT ["/app/start.sh"]