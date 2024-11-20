import ssl
import httpx
from openai import OpenAI

# Disable SSL verification (FOR DEVELOPMENT ONLY)
ssl._create_default_https_context = ssl._create_unverified_context

client = OpenAI(
    http_client=httpx.Client(verify=False)  # Disable SSL verification
)

chat_completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello world"}]
)

print(chat_completion.choices[0].message.content)