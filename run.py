import streamlit.web.cli as stcli
import sys
import os

if __name__ == "__main__":
    # Add the src directory to the Python path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
    
    # Run the Streamlit app
    sys.argv = ["streamlit", "run", "src/hed_schema_bot/app.py"]
    sys.exit(stcli.main()) 