import streamlit as st
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langgraph.graph import START, StateGraph

# Load environment variables
load_dotenv()

def get_hed_xml_content() -> str:
    """Fetch the latest HED XML schema."""
    url = "https://raw.githubusercontent.com/hed-standard/hed-schemas/main/standard_schema/hedxml/HEDLatest.xml"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to retrieve data from the URL. Status code: {response.status_code}")

def get_hed_description_tag_pairs() -> List[Tuple[str, str]]:
    """Get pairs of HED tag descriptions and names."""
    url = "https://raw.githubusercontent.com/hed-standard/hed-schemas/main/standard_schema/hedxml/HEDLatest.xml"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        all_nodes = soup.find_all('node')
        hed_description_tag_pairs = []
        for node in all_nodes:
            name = node.find('name', recursive=False).string
            description = node.find('description', recursive=False)
            description_text = description.string if description else ""
            hed_description_tag_pairs.append((description_text, name))
        return hed_description_tag_pairs
    else:
        raise Exception(f"Failed to retrieve data from the URL. Status code: {response.status_code}")

class State(TypedDict):
    """Type definition for the application state."""
    question: str
    context: List[Document]
    answer: str

def create_hed_bot():
    """Create and return a configured HED bot instance."""
    # Initialize components
    llm = ChatOpenAI(model="gpt-4o-mini")
    vocab = [tag for _, tag in get_hed_description_tag_pairs()]
    xml = get_hed_xml_content()

    # Create prompt template
    template = """Hierarchical Event Description (HED) schema expert.
You have access to the HED schema provided in the XML:
{xml} 
You take a tagging request and analyze it to find the most relevant HED tags. You will then give a summary of the tag names you found relevant, along with explanations for why you chose those tags.
You will then give an example of complete HED annotation using the tags you found. An example of a HED annotation is: (Foreground-view, (Square)), (Background-view, ((Human, Body), Outdoors, Urban))

Tagging request: {question}

Annotation:"""
    custom_rag_prompt = PromptTemplate.from_template(template)

    # Define application steps
    def generate(state: State):
        messages = custom_rag_prompt.invoke({
            "question": state["question"],
            "vocab": vocab,
            "xml": xml
        })
        response = llm.invoke(messages)
        return {"answer": response.content}

    # Compile application
    graph_builder = StateGraph(State)
    graph_builder.add_node("generate", generate)
    graph_builder.add_edge(START, "generate")
    graph = graph_builder.compile()

    return graph, vocab, xml

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
        with st.spinner("Searching for HED tags..."):
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