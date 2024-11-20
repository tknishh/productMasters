import streamlit as st
from database import Database
import time

# Initialize session state if needed
if 'db' not in st.session_state:
    st.session_state.db = Database()

# Check if we're editing an existing agent
is_editing = st.session_state.get('selected_agent') is not None
agent_to_edit = st.session_state.get('selected_agent')

if is_editing:
    st.header(f"Edit Agent: {agent_to_edit[1]}")
else:
    st.header("Create New Agent")

# Form for agent details
with st.form("agent_form"):
    name = st.text_input(
        "Agent Name", 
        value=agent_to_edit[1] if is_editing else ""
    )
    
    expertise = st.text_input(
        "Expertise",
        value=agent_to_edit[2] if is_editing else ""
    )
    
    description = st.text_area(
        "Description",
        value=agent_to_edit[3] if is_editing else "",
        height=100
    )
    
    prompt = st.text_area(
        "Agent Prompt",
        value=agent_to_edit[4] if is_editing else "",
        height=300,
        help="Use markdown formatting. Use {param} for parameters."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        agent_type = st.text_input(
            "Agent Type",
            value=agent_to_edit[5] if is_editing else ""
        )
    
    with col2:
        required_params = st.text_input(
            "Required Parameters (comma-separated)",
            value=agent_to_edit[6] if is_editing else "",
            help="Example: sector,region,timeframe"
        )
    
    submitted = st.form_submit_button("Save Agent")

if submitted:
    if all([name, expertise, description, prompt, agent_type, required_params]):
        agent_data = {
            "name": name,
            "expertise": expertise,
            "description": description,
            "prompt": prompt,
            "agent_type": agent_type,
            "required_params": required_params
        }
        
        try:
            if is_editing:
                st.session_state.db.update_agent(agent_to_edit[0], agent_data)
                st.success(f"Agent '{name}' updated successfully!")
            else:
                st.session_state.db.create_agent(agent_data)
                st.success(f"Agent '{name}' created successfully!")
            
            # Clear the selected agent from session state
            st.session_state.selected_agent = None
            
            # Redirect back to view agents
            time.sleep(1)  # Give time for the success message
            st.switch_page("pages/2_View_Agents.py")
        except Exception as e:
            st.error(f"Error saving agent: {str(e)}")
    else:
        st.error("All fields are required!")

# Add a cancel button
if st.button("Cancel"):
    st.session_state.selected_agent = None
    st.switch_page("pages/2_View_Agents.py")