from database import Database

def initialize_agents():
    db = Database()
    
    agents = [
        {
            "name": "Competition Overview Agent",
            "expertise": "Market Competition Analysis",
            "description": "Specializes in providing detailed competition overviews for specific market categories and geographical locations.",
            "agent_type": "overview",
            "required_params": "market_category,geographical_location",
            "prompt": """Please provide a Competition Overview for the following:
Market Category: {market_category}
Geographical Location: {geographical_location}

Please ensure the overview is:
- Detailed and well-structured
- Relevant to the market category and location
- Based on current data and trends

Market Overview: Briefly describe the growth and trends in the market, including factors driving demand.

Key Competitors: Identify major competitors in the market. For each competitor, provide:
- Name
- Brief description of their offerings
- Market positioning

Strengths and Weaknesses: For each competitor, list their strengths and weaknesses.

Geographical Focus: Outline the key geographical areas where these competitors operate and any regional trends that influence their strategies.

Comparative Analysis: Summarize the competitive landscape, highlighting opportunities for new entrants or existing players looking to improve their market position."""
        },
        {
            "name": "Persona Development Agent",
            "expertise": "Customer Persona Creation",
            "description": "Creates detailed buyer personas for specific products or services targeting particular audiences.",
            "agent_type": "persona",
            "required_params": "product_or_service,target_audience",
            "prompt": """Create a detailed persona for {product_or_service} targeting {target_audience}. Use the following template:

Persona: "[DESCRIPTIVE NAME]"

Demographics and Background:
- Age
- Occupation
- Department
- Level of Seniority
- Education
- Career Path
- Industry
- Organization Size

Goals and Objectives:
- Primary Goals
- Secondary Benefits

Challenges and Pain Points:
- Technical Challenges
- Organizational Challenges
- Lifestyle Challenges

Decision-Making Process:
- Research Stages
- Evaluation Criteria
- Key Decision-Makers
- Decision Timelines

Information Sources:
- Publications
- Forums
- Events
- Social Media

Objections and Concerns:
- Cost
- Implementation Difficulty
- User Adoption
- Integration

Preferred Communication Channels

Ideal Solution Features:
- Must-Haves
- Nice-to-Haves

Relationship to Product/Service:
- Current Usage
- Pain Points Addressed
- Potential Impact

Key Insights for Development"""
        },
        {
            "name": "Market Sizing Agent",
            "expertise": "Market Size Analysis",
            "description": "Provides detailed market size analysis including TAM, SAM, and SOM calculations.",
            "agent_type": "sizing",
            "required_params": "sector,region,market_segment",
            "prompt": """Estimate the market size of the {sector} in {region} targeting {market_segment}. Your analysis should cover:

1. Introduction:
   - Brief overview of the {sector} and its relevance
   - Key components: TAM, SAM, and SOM analysis

2. Total Addressable Market (TAM):
   - Overall revenue opportunity
   - Recent market valuation figures
   - Growth projections
   - Relation to {market_segment}

3. Serviceable Available Market (SAM):
   - Relevant portion considering constraints
   - Key sub-segments
   - Market trends specific to target audience

4. Serviceable Obtainable Market (SOM):
   - Realistic capture estimation
   - Market penetration rates
   - Competitor analysis

5. Conclusion and Market Opportunity:
   - Summary of market sizing
   - Strategic factors
   - Revenue potential"""
        },
        {
            "name": "Solution Mapping Agent",
            "expertise": "Solution Analysis and Mapping",
            "description": "Maps and analyzes different solutions available in specific market categories.",
            "agent_type": "solution",
            "required_params": "market_category",
            "prompt": """Perform a targeted analysis of the {market_category} to distinguish the different types of solutions available and categorize the kinds of providers offering these solutions. Your analysis should include:

1. Types of Solutions:
   - Main solution types
   - Specific examples of tools/services

2. Categories of Providers:
   - Provider categories
   - Grouping by size/specialization

3. Market Dynamics:
   - Key trends
   - Innovations
   - Challenges

4. Strategic Implications:
   - Business insights
   - Growth areas
   - Potential gaps"""
        },
        {
            "name": "ICP Development Agent",
            "expertise": "Ideal Customer Profile Development",
            "description": "Creates detailed Ideal Customer Profiles (ICP) for specific products or services.",
            "agent_type": "icp",
            "required_params": "product_service,business_segment",
            "prompt": """Develop an Ideal Customer Profile (ICP) for {product_service} targeting {business_segment}. The profile should cover:

1. Business Demographics:
   - Size
   - Industry
   - Location
   - Revenue

2. Decision-Maker Characteristics:
   - Roles
   - Responsibilities
   - Pain Points

3. Technological Maturity:
   - Level of Adoption
   - Innovation Requirements

4. Operational Needs:
   - Challenges
   - Goals

5. Values and Long-Term Objectives:
   - Core Values
   - Long-Term Goals

6. ICP Summary:
   - Key characteristics
   - Solution alignment"""
        },
        {
            "name": "Focus Group Analysis Agent",
            "expertise": "Focus Group Insights",
            "description": "Conducts detailed focus group analysis for specific products or services.",
            "agent_type": "focus",
            "required_params": "product_service,user_roles,company_types",
            "prompt": """Conduct a focused focus group to gather in-depth insights on {product_service} for {user_roles} in {company_types}.

1. Participant Profiles:
   - Professional roles
   - Goals
   - Product interest

2. Emotional Connection:
   - User excitement factors
   - Value alignment

3. Contextual Use:
   - Daily operations
   - Process improvements

4. Unmet Needs:
   - Pain points
   - Missing features
   - Implementation challenges

5. Personalization and Customization:
   - Customization needs
   - Workflow integration

6. Behavioral Change:
   - Operational changes
   - Efficiency improvements

7. Product Opportunities:
   - Enhancement suggestions
   - Innovation areas

8. Conclusion:
   - Key insights
   - Strategic opportunities"""
        },
        {
            "name": "Historical Insights Agent",
            "expertise": "Historical Market Analysis",
            "description": "Analyzes historical development and trends in specific sectors and regions.",
            "agent_type": "historical",
            "required_params": "sector,region,timeframe",
            "prompt": """Conduct a detailed analysis of the historical development of the {sector} in {region} over the past {timeframe}. Your analysis should include:

1. Introduction:
   - Sector evolution overview
   - Key themes/trends

2. Technological Advancements:
   - Major innovations
   - Evolution periods

3. Regulatory Changes:
   - Policy developments
   - Legal framework changes

4. Market Dynamics:
   - Structure shifts
   - Competition changes
   - Key players

5. Consumer Demand Shifts:
   - Preference changes
   - Adoption rates
   - Driving factors

6. Key Events and Milestones:
   - Turning points
   - Significant developments

7. Conclusion:
   - Development summary
   - Future trends
   - Growth areas"""
        }
    ]

    # First, clear existing agents (optional, remove if you want to keep existing agents)
    try:
        db.cursor.execute("DELETE FROM agents")
        db.conn.commit()
        print("Cleared existing agents")
    except Exception as e:
        print(f"Error clearing existing agents: {e}")

    # Add new agents
    for agent in agents:
        try:
            db.create_agent(agent)
            print(f"Successfully created agent: {agent['name']}")
        except Exception as e:
            print(f"Error creating agent {agent['name']}: {e}")

if __name__ == "__main__":
    initialize_agents() 