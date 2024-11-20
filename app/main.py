import streamlit as st
import httpx
from openai import OpenAI
from database import Database
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_openai_client():
    """Initialize OpenAI client with proper SSL handling"""
    try:
        return OpenAI(
            api_key=st.session_state.api_key or os.getenv("OPENAI_API_KEY"),
            http_client=httpx.Client(verify=True)  # Use verify=True for production
        )
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        return None

def initialize_session_state():
    """Initialize all session state variables"""
    # Dictionary of session state variables and their default values
    session_vars = {
        'api_key': os.getenv("OPENAI_API_KEY"),
        'chat_history': [],
        'db': None,
        'selected_agent': None,
        'openai_client': None,
        'user_name': None,
        'is_authenticated': False,
        'current_page': 'home',
        'error_message': None,
        'success_message': None,
    }
    
    # Initialize each variable if it doesn't exist
    for var, default_value in session_vars.items():
        if var not in st.session_state:
            st.session_state[var] = default_value

    # Special initialization for database and OpenAI client
    if st.session_state.db is None:
        try:
            st.session_state.db = Database()
        except Exception as e:
            st.error(f"Failed to initialize database: {str(e)}")
    
    if st.session_state.openai_client is None:
        st.session_state.openai_client = init_openai_client()

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('is_authenticated', False)

def main():
    st.set_page_config(
        page_title="AI Agent Management System",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    initialize_session_state()

    # Display any error or success messages
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = None
    
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None

    # Title and description
    st.title("AI Agent Management System")
    
    # Sidebar for authentication status and logout
    with st.sidebar:
        st.markdown("### System Status")
        st.markdown(f"🔌 Database: {'Connected' if st.session_state.db else 'Disconnected'}")
        st.markdown(f"🤖 OpenAI: {'Connected' if st.session_state.openai_client else 'Disconnected'}")
        
        if st.session_state.user_name:
            st.markdown(f"👤 User: {st.session_state.user_name}")
            if st.button("Logout"):
                for key in ['user_name', 'is_authenticated']:
                    st.session_state[key] = None
                st.rerun()

    # Main content
    st.write("Welcome to the AI Agent Management System!")
    st.write("Use the sidebar to navigate between different sections.")

if __name__ == "__main__":
    main()