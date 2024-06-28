import asyncio
from openai import OpenAI
from app.config import config, save_config


class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=config.aopse.providers["openai"].api_key)
        self.assistant_id = config.aopse.providers["openai"].assistant_id
        self.assistant = None
        self.check_assistant_exists()

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

    def check_assistant_exists(self):
        if self.assistant_id is None or self.assistant_id == "":
            self.create_assistant()
        try:
            self.assistant = self.client.beta.assistants.retrieve(self.assistant_id)
            if self.assistant is not None:
                return True
        except Exception as e:
            raise ValueError(f"Assistant ID {self.assistant_id} is invalid: {e}")

    def create_assistant(self):
        self.assistant = self.client.beta.assistants.create(
            name="AOPSE Assistant",
            description="AOPSE (AI OSINT People Search Engine) is an AI tool that helps users assess and improve online privacy and security. It scans public databases to identify potential vulnerabilities, data leaks, and other risks associated with a user's online presence. AOPSE provides personalized recommendations to remediate issues and strengthen privacy and security, such as guidance on strong passwords, 2FA, removing old accounts, and other best practices. AOPSE empowers users to protect their digital footprint.",
            model="gpt-3.5-turbo",
        )
        self.assistant_id = self.assistant.id
        # put assistant_id in config file
        config.aopse.providers["openai"].assistant_id = self.assistant_id
        save_config(config)
        return self.assistant
