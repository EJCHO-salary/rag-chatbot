from litellm import completion
from typing import List, Dict
from ragchat.config import config

class LLMInterface:
    def __init__(self, model_name: str = config.LLM_MODEL):
        self.model_name = model_name

    def generate_response(self, context: str, user_message: str) -> str:
        """
        Generates a response from the LLM based on the provided context and user message.
        """
        messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": f"You are a helpful assistant. Use the following context to answer the user's question.\n\nContext:\n{context}"
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        response = completion(
            model=self.model_name,
            messages=messages,
            api_key=config.GEMINI_API_KEY
        )
        
        return response.choices[0].message.content
