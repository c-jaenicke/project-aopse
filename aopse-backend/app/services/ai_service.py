import asyncio

from fastapi import WebSocket
from openai import OpenAI
from openai.lib.streaming import AssistantEventHandler
from openai.types.beta import AssistantStreamEvent
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta

from app.config import ConfigSingleton
from app.models import WebSocketMessage, EventType, ServerResponse, AIResponseStatus


class AIService:
    def __init__(self):
        self.config = ConfigSingleton.get_instance()
        self.client = OpenAI(api_key=self.config.aopse.providers["openai"].api_key)
        self.assistant_id = self.config.aopse.providers["openai"].assistant_id
        self.assistant = None
        self.check_assistant_exists()
        self.current_run_id = None
        self.current_model = self.config.aopse.providers["openai"].model

    class EventHandler(AssistantEventHandler):
        def __init__(self, callback, thread_id):
            super().__init__()
            self.thread_id = thread_id
            self.callback = callback

        def on_text_delta(self, delta, snapshot):
            self.callback(delta.value)

        def on_event(self, event: AssistantStreamEvent) -> None:
            if event.event == "thread.run.created":
                self.callback(event.data.id, event_type="created")
            if event.event == "thread.run.cancelled":
                self.callback("Run cancelled", event_type="cancelled")

        def on_tool_call_created(self, tool_call: ToolCall):
            print(f"Tool call created: {tool_call}")

        def on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall):
            print(f"Tool call delta: {delta}")

    def stream_response(self, thread_id: str, message: str, websocket: WebSocket):
        valid_thread = self.check_thread_exists(thread_id)
        if not valid_thread:
            response_event = WebSocketMessage(
                event=EventType.SERVER_ERROR,
                data=ServerResponse(content="Invalid thread ID", status=AIResponseStatus.aborted)
            )
            asyncio.run(websocket.send_text(response_event.json()))
            return

        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )

        def text_callback(text, event_type=None):
            if event_type == "created":
                print(f"Run created: {text}")
                self.current_run_id = text
            elif event_type == "cancelled":
                response_event = WebSocketMessage(
                    event=EventType.SERVER_AI_RESPONSE,
                    data=ServerResponse(content=text, status=AIResponseStatus.aborted)
                )
                asyncio.run(websocket.send_text(response_event.json()))
            else:
                response_event = WebSocketMessage(
                    event=EventType.SERVER_AI_RESPONSE,
                    data=ServerResponse(content=text, status=AIResponseStatus.streaming)
                )
                asyncio.run(websocket.send_text(response_event.json()))

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
            asyncio.run(websocket.send_text(response_event.json()))
        except Exception as e:
            print(f"Error in stream_response: {e}")

    async def cancel_current_run(self, thread_id: str):
        if self.current_run_id is not None:
            try:
                success = self.client.beta.threads.runs.cancel(run_id=self.current_run_id, thread_id=thread_id)
                print(f"Cancelled run: {success}")
                if success:
                    self.current_run_id = None
                    return True
            except Exception as e:
                print(f"Error cancelling run: {e}")
        return False

    def check_assistant_exists(self):
        if self.assistant_id is None or self.assistant_id == "":
            self.create_assistant()
        try:
            self.assistant = self.client.beta.assistants.retrieve(self.assistant_id)
            if self.assistant is not None:
                return True
        except Exception as e:
            raise ValueError(f"Assistant ID {self.assistant_id} is invalid: {e}")

    def check_thread_exists(self, thread_id: str):
        try:
            thread = self.client.beta.threads.retrieve(thread_id)
            if thread is not None:
                return True
        except Exception as e:
            raise ValueError(f"Thread ID {thread_id} is invalid: {e}")

    def create_assistant(self):
        try:
            self.assistant = self.client.beta.assistants.create(
                name="AOPSE Assistant",
                description="AOPSE (AI OSINT People Search Engine) is an AI tool that helps users assess and improve "
                            "online privacy and security. It scans public databases to identify potential "
                            "vulnerabilities, data leaks, and other risks associated with a user's online presence. "
                            "AOPSE"
                            "provides personalized recommendations to remediate issues and strengthen privacy and "
                            "security, such as guidance on strong passwords, 2FA, removing old accounts, and other best"
                            "practices.",
                model=self.current_model,
                instructions="""You are AOPSE (AI OSINT People Search Engine), an AI tool designed to help users 
                                assess and improve their online privacy and security.

                                Your main tasks are: 1. Scan public databases to identify potential vulnerabilities, 
                                data leaks, and other risks associated with a user's online presence. 2. Provide 
                                personalized recommendations to remediate issues and strengthen privacy and security, 
                                such as: - Guidance on creating strong passwords - Advice on enabling two-factor 
                                authentication (2FA) - Suggestions for removing old or unused online accounts - Other 
                                best practices for online privacy and security 3. Empower users to protect their 
                                digital footprint by offering actionable insights and easy-to-follow steps.

                                When responding to user queries, ensure that your answers are: - Clear, concise, 
                                and easy to understand - Tailored to the user's specific situation and needs - 
                                Focused on practical solutions and actionable advice - Encouraging and supportive, 
                                helping users feel empowered to take control of their online privacy and security

                                Remember, your goal is to be a trusted resource for users seeking to safeguard their 
                                digital presence. Always prioritize their privacy, security, and well-being in your 
                                interactions.""",
                tools=[{"type": "code_interpreter"}],
            )
            self.assistant_id = self.assistant.id
            self.config.aopse.providers["openai"].assistant_id = self.assistant_id

            try:
                ConfigSingleton.save_config(self.config)
            except Exception as config_error:
                print(f"Error saving configuration: {config_error}")

            return self.assistant

        except Exception as e:
            print(f"Error creating assistant: {e}")
            return None

    def update_assistant(self, model: str, websocket: WebSocket):
        try:
            self.assistant = self.client.beta.assistants.update(
                self.assistant_id,
                name="AOPSE Assistant",
                description="AOPSE (AI OSINT People Search Engine) is an AI tool that helps users assess and improve "
                            "online privacy and security. It scans public databases to identify potential "
                            "vulnerabilities, data leaks, and other risks associated with a user's online presence. "
                            "AOPSE"
                            "provides personalized recommendations to remediate issues and strengthen privacy and "
                            "security, such as guidance on strong passwords, 2FA, removing old accounts, and other best"
                            "practices.",
                model=model,
                instructions="""You are AOPSE (AI OSINT People Search Engine), an AI tool designed to help users 
                                assess and improve their online privacy and security.
    
                                Your main tasks are: 1. Scan public databases to identify potential vulnerabilities, 
                                data leaks, and other risks associated with a user's online presence. 2. Provide 
                                personalized recommendations to remediate issues and strengthen privacy and security, 
                                such as: - Guidance on creating strong passwords - Advice on enabling two-factor 
                                authentication (2FA) - Suggestions for removing old or unused online accounts - Other 
                                best practices for online privacy and security 3. Empower users to protect their 
                                digital footprint by offering actionable insights and easy-to-follow steps.
    
                                When responding to user queries, ensure that your answers are: - Clear, concise, 
                                and easy to understand - Tailored to the user's specific situation and needs - 
                                Focused on practical solutions and actionable advice - Encouraging and supportive, 
                                helping users feel empowered to take control of their online privacy and security
    
                                Remember, your goal is to be a trusted resource for users seeking to safeguard their 
                                digital presence. Always prioritize their privacy, security, and well-being in your 
                                interactions.""",
                tools=[{"type": "code_interpreter"}],
            )

            response_event = WebSocketMessage(
                event=EventType.SERVER_CHANGE_MODEL,
                data=ServerResponse(content=model)
            )
            asyncio.run(websocket.send_text(response_event.json()))

            try:
                self.config.aopse.providers["openai"].model = model
                ConfigSingleton.save_config(self.config)
            except Exception as config_error:
                print(f"Error saving configuration: {config_error}")

            return self.assistant
        except Exception as e:
            print(f"Error updating assistant: {e}")
            return None

    def create_thread(self, websocket: WebSocket):
        try:
            thread = self.client.beta.threads.create()
            thread_id = thread.id
            response_event = WebSocketMessage(
                event=EventType.SERVER_SEND_THREAD,
                data=ServerResponse(content=thread_id)
            )
            asyncio.run(websocket.send_text(response_event.json()))
            return thread_id
        except Exception as e:
            print(f"Error creating thread: {e}")
            return None
