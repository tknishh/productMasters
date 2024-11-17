import streamlit as st
from database import Database
from utils import process_agent_query

def initialize_session_state():
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'db' not in st.session_state:
        st.session_state.db = Database()
    if 'selected_agent' not in st.session_state:
        st.session_state.selected_agent = None

def create_agent_section():
    st.header("Create/Update Agent")
    
    action = st.radio("Action", ["Create New Agent", "Update Existing Agent"])
    
    if action == "Update Existing Agent":
        agents = st.session_state.db.get_agents()
        if not agents:
            st.info("No agents found to update!")
            return
        selected_agent = st.selectbox(
            "Select Agent to Update",
            options=agents,
            format_func=lambda x: x[1]
        )
        if selected_agent:
            name = st.text_input("Agent Name", value=selected_agent[1])
            expertise = st.text_input("Expertise", value=selected_agent[2])
            description = st.text_area("Description", value=selected_agent[3])
            prompt = st.text_area("Agent Prompt", value=selected_agent[4], height=300)
            agent_type = st.text_input("Agent Type", value=selected_agent[5])
            required_params = st.text_input("Required Parameters (comma-separated)", value=selected_agent[6])
            agent_id = selected_agent[0]
    else:
        name = st.text_input("Agent Name")
        expertise = st.text_input("Expertise")
        description = st.text_area("Description")
        prompt = st.text_area("Agent Prompt", height=300)
        agent_type = st.text_input("Agent Type")
        required_params = st.text_input("Required Parameters (comma-separated)")
        agent_id = None

    if st.button("Save Agent"):
        if all([name, expertise, description, prompt, agent_type, required_params]):
            agent_data = {
                "name": name,
                "expertise": expertise,
                "description": description,
                "prompt": prompt,
                "agent_type": agent_type,
                "required_params": required_params
            }
            
            if agent_id:
                st.session_state.db.update_agent(agent_id, agent_data)
                st.success(f"Agent '{name}' updated successfully!")
            else:
                st.session_state.db.create_agent(agent_data)
                st.success(f"Agent '{name}' created successfully!")
        else:
            st.error("All fields are required!")

def chat_section():
    st.header("Chat with Agent")
    
    agents = st.session_state.db.get_agents()
    if not agents:
        st.info("No agents found. Create one first!")
        return
        
    selected_agent = st.selectbox(
        "Select Agent",
        options=agents,
        format_func=lambda x: x[1]
    )
    
    if selected_agent:
        st.subheader(f"Chatting with {selected_agent[1]}")
        
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        user_input = st.chat_input("Your message")
        
        if user_input:
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.chat_history.append(
                {"role": "user", "content": user_input}
            )
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = process_agent_query(
                        st.session_state.api_key,
                        selected_agent,
                        user_input
                    )
                    st.write(response)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": response}
                    )

def view_agents_section():
    st.header("View All Agents")
    
    agents = st.session_state.db.get_agents()
    if not agents:
        st.info("No agents found. Create one first!")
        return
    
    # Create tabs for different view options
    view_type = st.radio("View Type", ["Card View", "Table View"])
    
    if view_type == "Card View":
        # Display agents in a grid of cards
        cols = st.columns(2)  # Create 2 columns
        for idx, agent in enumerate(agents):
            with cols[idx % 2]:  # Alternate between columns
                with st.expander(f"📱 {agent[1]}", expanded=True):
                    st.write(f"**Expertise:** {agent[2]}")
                    st.write(f"**Description:** {agent[3]}")
                    
                    # Add buttons for actions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Edit", key=f"edit_{agent[0]}"):
                            st.session_state.selected_agent = agent[0]
                            st.switch_page("Create Agent")  # This will need to be implemented
                    with col2:
                        if st.button("Delete", key=f"delete_{agent[0]}"):
                            if st.session_state.db.delete_agent(agent[0]):
                                st.success(f"Agent '{agent[1]}' deleted successfully!")
                                st.rerun()
                    
                    # Show/Hide prompt
                    if st.button("Show Prompt", key=f"prompt_{agent[0]}"):
                        st.text_area("Agent Prompt", value=agent[4], height=150, disabled=True)
    
    else:  # Table View
        # Convert agents data to a format suitable for a dataframe
        agent_data = {
            "Name": [],
            "Expertise": [],
            "Description": [],
            "Actions": []
        }
        
        for agent in agents:
            agent_data["Name"].append(agent[1])
            agent_data["Expertise"].append(agent[2])
            agent_data["Description"].append(agent[3])
            
            # Create action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Edit", key=f"edit_table_{agent[0]}"):
                    st.session_state.selected_agent = agent[0]
                    st.switch_page("Create Agent")
            with col2:
                if st.button("Delete", key=f"delete_table_{agent[0]}"):
                    if st.session_state.db.delete_agent(agent[0]):
                        st.success(f"Agent '{agent[1]}' deleted successfully!")
                        st.rerun()
        
        # Display the table
        st.dataframe(
            agent_data,
            column_config={
                "Name": st.column_config.TextColumn("Name", width="medium"),
                "Expertise": st.column_config.TextColumn("Expertise", width="medium"),
                "Description": st.column_config.TextColumn("Description", width="large"),
            },
            hide_index=True,
        )

def main():
    st.title("AI Agent Management System")
    initialize_session_state()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Create Agent", "View Agents", "Chat with Agent"])
    
    if page == "Create Agent":
        create_agent_section()
    elif page == "View Agents":
        view_agents_section()
    elif page == "Chat with Agent":
        chat_section()

if __name__ == "__main__":
    main()