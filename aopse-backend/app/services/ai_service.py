import asyncio
from typing import AsyncGenerator
from openai import OpenAI
from openai.lib.streaming import AssistantEventHandler

from app.config import config, save_config
from app.models import WebSocketMessage, EventType, ServerResponse, AIResponseStatus

from fastapi import WebSocket


class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=config.aopse.providers["openai"].api_key)
        self.assistant_id = config.aopse.providers["openai"].assistant_id
        self.assistant = None
        self.check_assistant_exists()

    class EventHandler(AssistantEventHandler):
        def __init__(self, callback, thread_id):
            super().__init__()
            self.thread_id = thread_id
            self.callback = callback

        def on_text_delta(self, delta, snapshot):
            self.callback(delta.value)

    def stream_response(self, thread_id: str, message: str, websocket: WebSocket):  # Add websocket as an argument
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )

        def text_callback(text):
            response_event = WebSocketMessage(
                event=EventType.SERVER_AI_RESPONSE,
                data=ServerResponse(content=text, status=AIResponseStatus.streaming)
            )
            asyncio.run(websocket.send_text(response_event.json()))  # Use the websocket argument

        try:
            with self.client.beta.threads.runs.create_and_stream(
                    thread_id=thread_id,
                    assistant_id=self.assistant_id,
                    event_handler=self.EventHandler(text_callback, thread_id),
            ) as stream:
                stream.until_done()

            response_event = WebSocketMessage(
                event=EventType.SERVER_AI_RESPONSE,
                data=ServerResponse(content="", status=AIResponseStatus.completed)
            )
            asyncio.run(websocket.send_text(response_event.json()))  # Use the websocket argument
        except Exception as e:
            print(f"Error in stream_response: {e}")

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

    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread.id
