#!/bin/bash
# Download config from S3
echo "Downloading litellm_config.yaml from S3..."
aws s3 cp s3://litellmproxy/litellm_config.yaml /app/config.yaml --region us-east-2

# Run LiteLLM
litellm --config /app/config.yaml --detailed_debug