from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_claude(prompt):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=700,
        temperature=0.2,
        messages=[
            {"role":"user","content":prompt}
        ]
    )
    return response.content[0].text