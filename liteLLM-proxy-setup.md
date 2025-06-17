# LiteLLM Proxy — Production Deployment (Render + S3 + Postgres)

## Architecture

- Render hosts LiteLLM Proxy in Docker
- AWS S3 stores litellm_config.yaml
- Render Postgres stores virtual keys and logging

## Setup Instructions

### 1️⃣ AWS

- Create private S3 bucket: `litellmproxy`
- Upload your config.yaml:
  aws s3 cp litellm_config.yaml s3://litellmproxy/litellm_config.yaml
- Create new IAM user with `s3:GetObject` and `s3:ListBucket` permissions.
- Generate Access Key + Secret.

### 2️⃣ Render

- Create Render Postgres database.
- Note your `DATABASE_URL`.

- Create new Web Service linked to this repo.
- Add environment variables:

| Key | Value |
| --- | --- |
| AWS_ACCESS_KEY_ID | *your key* |
| AWS_SECRET_ACCESS_KEY | *your secret* |
| AWS_DEFAULT_REGION | us-east-2 |
| OPENAI_API_KEY | *your OpenAI key* |
| DATABASE_URL | *your Postgres URL* |

### 3️⃣ Done!

Render builds and deploys automatically.

### 4️⃣ Virtual Key Setup

Use CLI or admin UI to create virtual keys as needed.