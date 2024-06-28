from openai import OpenAI
from config import settings

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    async def stream_response(self, message: str):
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
