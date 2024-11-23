from openai import OpenAI
import streamlit as st
import httpx

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")

def validate_api_key(api_key):
    try:
        client = OpenAI(api_key=api_key)
        client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Test"}]
        )
        print("API key validated successfully!", client)
        return True
    except Exception:
        return False

def process_agent_query(api_key, agent_data, user_input):
    """
    Process a user query using the specified agent
    
    Args:
        api_key: OpenAI API key
        agent_data: Dictionary containing agent information
        user_input: User's message
    """
    try:
        # Add debug logging
        st.sidebar.info("Initializing OpenAI client...")
        
        # Create new client with explicit timeout
        client = OpenAI(
            api_key=api_key,
            http_client=httpx.Client(verify=False)
        )
        
        # Store client in session state for reuse
        st.session_state['openai_client'] = client
        
        # Add debug logging
        st.sidebar.info("Making API call...")
        
        # Construct system prompt using agent data
        system_prompt = f"""You are an AI assistant specialized in {agent_data['expertise']}.
Role: {agent_data['name']}
Type: {agent_data['type']}
Description: {agent_data['description']}

Your task is to provide information based on the following parameters:
{', '.join(agent_data['parameters'])}

{agent_data['prompt']}

Please provide detailed and accurate responses while staying within your defined expertise and parameters."""

        # Make API call
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract and return response
        return response.choices[0].message.content
        
    except Exception as e:
        # More detailed error handling
        error_msg = f"Error details: {str(e)}"
        if "Connection" in str(e):
            error_msg += "\nPlease check your internet connection and try again."
        elif "Authentication" in str(e):
            error_msg += "\nPlease verify your API key is correct."
            
        st.sidebar.error(error_msg)
        raise Exception(f"Failed to process query: {error_msg}")