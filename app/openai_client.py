import openai
import os

from dotenv import load_dotenv
load_dotenv()

# Get OpenAI API key from environment variable
api_key = os.environ.get('OPENAI_API_KEY')
groq_key = os.environ.get('GROQ_KEY')

# Ensure the API key is set
if not api_key:
    print("No API Keys")

# Set the API key for OpenAI
client = openai.OpenAI(api_key=api_key)


groq_client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_key
)
