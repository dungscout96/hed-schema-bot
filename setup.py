from setuptools import setup, find_packages

setup(
    name="hed-schema-bot",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "streamlit",
        "langchain",
        "langchain-openai",
        "langchain-community",
        "langchain-chroma",
        "python-dotenv",
        "beautifulsoup4",
        "lxml",
        "requests",
        "hed",
        "langgraph",
    ],
    python_requires=">=3.8",
    author="HED Schema Bot Team",
    description="A Streamlit app for HED schema tagging using LLMs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
) 