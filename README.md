# HED Schema Bot

A Streamlit application that helps users tag events using the Hierarchical Event Description (HED) schema. The application uses LLMs to suggest relevant HED tags based on user input.

## Installation

### Using uv (Recommended)

1. Install uv if you haven't already:
```bash
pip install uv
```

2. Create and activate a virtual environment using uv's built-in Python:
```bash
uv venv --python 3.11
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

### Using pip

```bash
pip install -e .
```

## Usage

1. Set up your environment variables in a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

2. Run the Streamlit app:
```bash
streamlit run src/hed_schema_bot/app.py
```

## Deployment

The easiest way to deploy this app is using Streamlit Community Cloud (free for public apps):

1. Push your code to a GitHub repository:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file path (`src/hed_schema_bot/app.py`)
6. Add your secrets (environment variables) in the "Secrets" section:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
7. Click "Deploy"

Your app will be available at `https://your-username-hed-schema-bot-app-xxxx.streamlit.app`

## Features

- Interactive interface for HED schema tagging
- LLM-powered tag suggestions
- Real-time validation of HED annotations
- Access to the complete HED vocabulary

## Development

To set up the development environment:

1. Clone the repository
2. Create a virtual environment using uv's built-in Python:
```bash
uv venv --python 3.11
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```
3. Install development dependencies:
```bash
uv pip install -r requirements.txt
``` 