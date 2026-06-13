from dotenv import load_dotenv

from openai import OpenAI

import os

load_dotenv()

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))




response = client.responses.create(
    model = "gpt-4o",
    input = "Say hello in one sentence."

)
print(response.output_text)