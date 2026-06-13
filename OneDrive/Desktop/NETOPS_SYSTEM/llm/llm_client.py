from dotenv import load_dotenv
from openai import OpenAI   
import os

load_dotenv()

client = OpenAI(
    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

)


class LLMClient:
    def __init__ (self):
        self.client = OpenAI(
            api_key = os.getenv("OPOENAI_API_KEY")
        )

    def generate(
            self,
            prompt
                 ):
        
        response = self.client.responses.create(
            model = "gpt-4o",
            input = prompt
        )

        return response.output_text
    

        