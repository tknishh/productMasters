import streamlit as st
from database import Database
from utils import process_agent_query

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

# Get all agents
agents = st.session_state.db.get_agents()
if not agents:
    st.info("No agents found. Create one first!")
    st.stop()

# Log available agents
st.sidebar.write("Available Agents:", [agent[1] for agent in agents])

# Agent selection
selected_agent = st.selectbox(
    "Select Agent",
    options=agents,
    format_func=lambda x: x[1]
)

if selected_agent:
    st.sidebar.write("Selected Agent:", selected_agent[1])
    st.subheader(f"Chatting with {selected_agent[1]}")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Your message")
    
    if user_input:
        # Log user input
        st.sidebar.write("User Input:", user_input)
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = process_agent_query(
                        st.session_state.api_key,
                        selected_agent,
                        user_input
                    )
                    st.sidebar.write("Response received:", bool(response))
                    st.write(response)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": response}
                    )
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
                    st.sidebar.error(f"Full error: {repr(e)}")

# Add a clear chat history button
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun() 