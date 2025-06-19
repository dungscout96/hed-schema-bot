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
    initial_generation: str

def create_hed_bot():
    """Create and return a configured HED bot instance."""
    # Initialize components
    llm = ChatOpenAI(model="gpt-4o-mini",
                    api_key="sk-1234",
                    temperature=0,
                    base_url="https://litellm-proxy-production-c44d.up.railway.app/")
    xml = get_hed_xml_content()

    # Define application steps
    def generate(state: State):
        # Create prompt template
        template = """Hierarchical Event Description (HED) schema expert.
You have access to the HED schema provided in the XML:
{xml} 

You take a tagging request and analyze it to find the most relevant HED tags. You will then give a summary of the tag names you found relevant, along with explanations for why you chose those tags.
Take into account the hierarchy of the schema so you can use the most specific tags.
You will then give an example of complete HED annotation using the tags you found. 


Then since this schema has is-a relationship, an annotation the appearance of children and parent together is redundant.
You will simplify the annotation if there's redundant, keeping only the most specific term, since it implies all its ancestors.

An example of a HED annotation with only specific tags: (Foreground-view, (Square)), (Background-view, ((Human, Body), Outdoors, Urban))

Tagging request: {question}

Annotation:"""
        custom_rag_prompt = PromptTemplate.from_template(template)
        messages = custom_rag_prompt.invoke({
            "question": state["question"],
            "xml": xml
        })
        response = llm.invoke(messages)
        return {"answer": response.content, "initial_generation": response.content}

    def review(state: State):
        # get the answer from the generate node
        answer = state["answer"]
        initial_generation = state["initial_generation"]
        # review the answer
        # Create prompt template
        template = """You are given a HED annotation. Revise it to be maximally concise while still preserve semantic grouping. Here are the revision rules:
1.	Remove Redundant Parent Tags:
	•	If a child tag fully implies its parent, drop the parent.
	•	Examples:
	•	2D-shape, Square → Square
	•	Color, Red → Red 
2.	Keep Event Type Tags:
	•	Always retain the top-level event type (e.g., Visual-presentation, Sensory-presentation).
3.	Preserve Leaf Tags:
	•	Always retain specific value or leaf tags like Square, Red.

Original annotation: {annotation}

Revised annotation:"""
        prompt = PromptTemplate.from_template(template)
        messages = prompt.invoke({
            "annotation": answer,
        })
        response = llm.invoke(messages)
        return {"answer": response.content, "initial_generation": initial_generation}

    # Compile application
    graph_builder = StateGraph(State)
    graph_builder.add_node("generate", generate)
    # graph_builder.add_node("review", review)
    graph_builder.add_edge(START, "generate")
    # graph_builder.add_edge("generate", "review")
    graph = graph_builder.compile()

    return graph, xml

# Set page config
st.set_page_config(
    page_title="HED Schema Bot",
    page_icon="🏷️",
    layout="wide"
)

# Initialize session state
if 'bot' not in st.session_state:
    st.session_state.bot, st.session_state.xml = create_hed_bot()

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
                "xml": st.session_state.xml,
                "initial_generation": "",  # Initialize with empty string
                "answer": ""  # Initialize with empty string
            })
            
            # Display both the initial generation and reviewed output
            # st.markdown("### Initial HED Tags")
            # st.write(response["initial_generation"])
            
            # st.markdown("### Response")
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