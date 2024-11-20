import streamlit as st
from database import Database
import time

# Initialize session state if needed
if 'db' not in st.session_state:
    st.session_state.db = Database()

st.header("View Agents")

# Get all agents from the database
agents = st.session_state.db.get_agents()

if not agents:
    st.info("No agents found. Create one first!")
else:
    # Add search/filter functionality
    search = st.text_input("🔍 Search agents by name or expertise", "")
    
    # Filter agents based on search
    filtered_agents = agents
    if search:
        filtered_agents = [
            agent for agent in agents 
            if search.lower() in agent[1].lower() or search.lower() in agent[2].lower()
        ]
    
    # Display agents in a cleaner layout
    for agent in filtered_agents:
        with st.container():
            # Create a card-like container
            st.markdown("""
            <style>
            .agent-card {
                padding: 20px;
                border-radius: 10px;
                background-color: #f0f2f6;
                margin: 10px 0;
            }
            </style>
            """, unsafe_allow_html=True)
            
            with st.container():
                # Header row
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {agent[1]}")
                    st.markdown(f"*{agent[2]}*")
                
                with col2:
                    # Action buttons in a more compact layout
                    cols = st.columns(3)
                    with cols[0]:
                        if st.button("💬", key=f"chat_{agent[0]}", help="Chat with agent"):
                            st.session_state.selected_agent = agent
                            time.sleep(0.1)  # Small delay to ensure state is updated
                            st.switch_page("pages/3_Chat.py")
                    
                    with cols[1]:
                        if st.button("✏️", key=f"edit_{agent[0]}", help="Edit agent"):
                            st.session_state.selected_agent = agent
                            time.sleep(0.1)  # Small delay to ensure state is updated
                            st.switch_page("pages/1_Create_Agent.py")
                    
                    with cols[2]:
                        if st.button("🗑️", key=f"delete_{agent[0]}", help="Delete agent"):
                            if st.session_state.db.delete_agent(agent[0]):
                                st.success(f"Agent '{agent[1]}' deleted successfully!")
                                time.sleep(1)  # Give time for the success message
                                st.rerun()
                            else:
                                st.error("Failed to delete agent!")
                
                # Details section
                with st.expander("View Details"):
                    st.markdown("**Description:**")
                    st.write(agent[3])
                    
                    st.markdown("**Type:**")
                    st.write(agent[5])
                    
                    st.markdown("**Required Parameters:**")
                    params = agent[6].split(',')
                    for param in params:
                        st.markdown(f"- {param.strip()}")
                    
                    st.markdown("**Prompt Template:**")
                    st.code(agent[4], language="markdown")
            
            st.divider()

# Add a floating action button to create new agent
st.sidebar.markdown("### Quick Actions")
if st.sidebar.button("➕ Create New Agent", use_container_width=True):
    time.sleep(0.1)  # Small delay to ensure state is updated
    st.switch_page("pages/1_Create_Agent.py")