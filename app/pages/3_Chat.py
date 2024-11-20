import streamlit as st
from database import Database
from utils import process_agent_query
from openai import OpenAI

# Initialize session state if needed
if 'db' not in st.session_state:
    st.session_state.db = Database()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.header("Chat with Agent")

# Debug information in sidebar
st.sidebar.write("Debug Information:")
st.sidebar.write(f"OpenAI Client initialized: {st.session_state.openai_client is not None}")
st.sidebar.write(f"API Key present: {st.session_state.api_key is not None}")

# Check for API key at the start of chat
if 'api_key' not in st.session_state or not st.session_state.api_key:
    st.warning("OpenAI API key is required to chat with agents.")
    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    if api_key:
        st.session_state.api_key = api_key
        # Initialize OpenAI client
        st.session_state.openai_client = OpenAI(api_key=api_key)
        st.success("API key saved! You can now chat with agents.")
        st.rerun()
    st.stop()

# Get all agents
agents = st.session_state.db.get_agents()
if not agents:
    st.info("No agents found. Create one first!")
    st.stop()

# Agent selection
selected_agent = st.selectbox(
    "Select Agent",
    options=agents,
    format_func=lambda x: x[1]  # Display agent name
)

if selected_agent:
    agent_id, name, expertise, description, agent_type, prompt_template, parameters = selected_agent
    
    # Display agent info
    with st.expander("Agent Information"):
        st.write(f"**Expertise:** {expertise}")
        st.write(f"**Description:** {description}")
        st.write(f"**Type:** {agent_type}")
        if parameters:
            st.write("**Required Parameters:**", parameters)
    
    st.subheader(f"Chatting with {name}")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Your message")
    
    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Add to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Process and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Get agent details for better context
                    agent_details = st.session_state.db.get_agent_details(agent_id)
                    
                    # Prepare agent data with full context
                    agent_data = {
                        'id': agent_id,
                        'name': name,
                        'expertise': expertise,
                        'description': description,
                        'prompt': prompt_template,
                        'parameters': parameters.split(',') if parameters else [],
                        'type': agent_type,
                        'configs': agent_details.get('configs', {})
                    }
                    
                    # Get response
                    response = process_agent_query(
                        st.session_state.api_key,
                        agent_data,  # Pass full agent data
                        user_input
                    )
                    
                    # Display response
                    st.markdown(response)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.sidebar.error(f"Full error: {repr(e)}")

# Chat controls
with st.sidebar:
    st.write("Chat Controls")
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun() 