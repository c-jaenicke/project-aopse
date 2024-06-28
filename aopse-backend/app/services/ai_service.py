import asyncio
from openai import OpenAI
from app.config import settings


class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    async def stream_response(self, message: str):
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            stream=True,
        )
        try:
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                await asyncio.sleep(0)  # TODO: check if this works as intended
        except asyncio.CancelledError:
            stream.close()
            raise
