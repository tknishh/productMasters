from openai import OpenAI
import json
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
    try:
        client = OpenAI(api_key=api_key)
        name, category, query_params = agent_data[1], agent_data[2], json.loads(agent_data[3])
        
        system_prompt = f"""You are an AI assistant specialized in {category}.
Your task is to provide information based on the following parameters:
{json.dumps(query_params, indent=2)}

Please provide detailed and accurate responses while staying within these parameters."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing request: {str(e)}"