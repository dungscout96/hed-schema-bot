#!/bin/bash
# Download config from S3

echo "AWS_ACCESS_KEY_ID is: $AWS_ACCESS_KEY_ID"
echo "AWS_SECRET_ACCESS_KEY is: $AWS_SECRET_ACCESS_KEY"
echo "AWS_DEFAULT_REGION is: $AWS_DEFAULT_REGION"

echo "Downloading litellm_config.yaml from S3..."
aws s3 cp s3://litellmproxy/litellm_config.yaml /app/config.yaml --region us-east-2

# Run LiteLLM
litellm --config /app/config.yaml --detailed_debug