import streamlit as st
from dotenv import load_dotenv
from hed_schema_bot.core import create_hed_bot

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="HED Schema Bot",
    page_icon="🏷️",
    layout="wide"
)

# Initialize session state
if 'bot' not in st.session_state:
    st.session_state.bot, st.session_state.vocab, st.session_state.xml = create_hed_bot()

# App title and description
st.title("🏷️ HED Schema Bot")
st.markdown("""
This tool helps you tag events using the Hierarchical Event Description (HED) schema.
Enter your event description below, and the bot will suggest relevant HED tags.
""")

# Input area
user_input = st.text_area(
    "Describe the event you want to tag:",
    height=150,
    placeholder="Example: A person is walking in a park while birds are chirping..."
)

# Process button
if st.button("Recommend HED Tags"):
    if user_input:
        with st.spinner("Searching HED tags..."):
            # Get response from bot
            response = st.session_state.bot.invoke({
                "question": user_input,
                "vocab": st.session_state.vocab,
                "xml": st.session_state.xml
            })
            
            # Display the response
            st.markdown("### Generated HED Tags")
            st.write(response["answer"])
            
    else:
        st.warning("Please enter an event description first.")

# Add information about HED
with st.expander("About HED Schema"):
    st.markdown("""
    The Hierarchical Event Descriptor (HED) schema is a framework for systematically describing events in a dataset.
    It provides a standardized vocabulary for annotating events in neuroimaging and other time-series data.
    
    For more information, visit the [HED website](https://www.hedtags.org/).
    """)

# Add footer
st.markdown("---")
st.markdown("Built using Streamlit and LangChain") 