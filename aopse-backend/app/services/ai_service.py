import asyncio
import json
from datetime import datetime

from fastapi import WebSocket
from openai import OpenAI
from openai.lib.streaming import AssistantEventHandler
from openai.types.beta import AssistantStreamEvent
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta

from app.config import ConfigSingleton
from app.models import WebSocketMessage, EventType, ServerResponse, AIResponseStatus, AIRunStatus
from app.storage.chroma_storage import ChromaStorage
from app.utils.hibp import HIBP
from app.utils.sherlock_search import SherlockSearch, QueryResult
from app.utils.tavily import TavilySearch


class AIService:
    def __init__(self):
        self.config = ConfigSingleton.get_instance()
        self.client = OpenAI(api_key=self.config.aopse.providers["openai"].api_key)
        self.assistant_id = self.config.aopse.providers["openai"].assistant_id
        self.current_model = self.config.aopse.providers["openai"].model
        self.assistant = None
        self.current_run_id = None
        self.websocket = None
        self.check_assistant_exists()
        self.tavily_search = TavilySearch()
        self.chromadb = ChromaStorage()
        self.hibp = HIBP()
        self.account_check = SherlockSearch()
        self.site_index = 0

    class EventHandler(AssistantEventHandler):
        def __init__(self, callback, thread_id):
            super().__init__()
            self.thread_id = thread_id
            self.callback = callback

        def on_event(self, event: AssistantStreamEvent) -> None:
            if event.event == "thread.run.created":
                self.callback(event.data.id, event_type="run_created")
            elif event.event == "thread.run.queued":
                self.callback("Run queued", event_type="run_queued")
            elif event.event == "thread.run.in_progress":
                self.callback("Run in progress", event_type="run_in_progress")
            elif event.event == "thread.run.completed":
                self.callback("Run completed", event_type="run_completed")
            elif event.event == "thread.run.requires_action":
                tool_calls = event.data.required_action.submit_tool_outputs.tool_calls
                self.callback(tool_calls, event_type="run_requires_action", thread_id=self.thread_id)
            elif event.event == "thread.run.expired":
                self.callback("Run expired", event_type="run_expired")
            elif event.event == "thread.run.cancelling":
                self.callback("Run cancelling", event_type="run_cancelling")
            elif event.event == "thread.run.cancelled":
                self.callback("Run cancelled", event_type="run_cancelled")
            elif event.event == "thread.run.failed":
                error = event.data.last_error
                self.callback(f"Run failed: {error}", event_type="run_failed")
            elif event.event == "thread.run.incomplete":
                details = event.data.incomplete_details
                self.callback(f"Run incomplete: {details}", event_type="run_incomplete")

        def on_text_delta(self, delta, snapshot):
            print(f"Text delta: {delta}")
            self.callback(delta.value)

        def on_tool_call_created(self, tool_call: ToolCall):
            print(f"Tool call created: {tool_call}")

        def on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall):
            print(f"Tool call delta: {delta}")

    def stream_response(self, thread_id: str, message: str, websocket: WebSocket):
        self.websocket = websocket
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

        try:
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with self.client.beta.threads.runs.create_and_stream(
                    thread_id=thread_id,
                    assistant_id=self.assistant_id,
                    event_handler=self.EventHandler(self.text_callback, thread_id),
                    additional_instructions=(
                            f"It is currently {current_datetime}. "
                            f"When responding to the user, assume this is the current date and time. "
                            f"If the user asks about the current time, date, or anything related to the present moment,"
                            f" use this provided datetime as the frame of reference."
                    )
            ) as stream:
                stream.until_done()

            response_event = WebSocketMessage(
                event=EventType.SERVER_AI_RESPONSE,
                data=ServerResponse(content="", status=AIResponseStatus.completed)
            )
            asyncio.run(websocket.send_text(response_event.json()))
        except Exception as e:
            print(f"Error in stream_response: {e}")

    def text_callback(self, text, event_type=None, thread_id=None):
        if event_type == "run_created":
            print(f"Run created: {text}")
            self.current_run_id = text
        elif event_type in ["run_queued", "run_in_progress", "run_completed", "run_expired", "run_cancelling",
                            "run_cancelled", "run_failed", "run_incomplete"]:
            response_event = WebSocketMessage(
                event=EventType.SERVER_AI_STATUS,
                data=ServerResponse(content=text, status=AIResponseStatus.streaming)
            )
            asyncio.run(self.websocket.send_text(response_event.json()))
        elif event_type == "run_requires_action":
            requires_action_event = WebSocketMessage(
                event=EventType.SERVER_REQUIRES_ACTION,
                data=ServerResponse(
                    content="AI requires additional information",
                    status=AIResponseStatus.streaming,
                    metadata={
                        "tool_calls": [{"name": tool_call.function.name, "arguments": tool_call.function.arguments} for
                                       tool_call in text]}
                )
            )
            asyncio.run(self.websocket.send_text(requires_action_event.json()))
            self.handle_tool_calls(text, thread_id)
        elif event_type == "text_delta":
            response_event = WebSocketMessage(
                event=EventType.SERVER_AI_RESPONSE,
                data=ServerResponse(content=text, status=AIResponseStatus.streaming)
            )
            asyncio.run(self.websocket.send_text(response_event.json()))
        elif event_type in ["tool_call_created", "tool_call_delta"]:
            tool_call = text
            response_event = WebSocketMessage(
                event=EventType.SERVER_TOOL_CALL,
                data=ServerResponse(
                    content=f"Tool call: {tool_call.function.name}",
                    status=AIResponseStatus.streaming,
                    metadata={
                        "tool_name": tool_call.function.name,
                        "tool_arguments": tool_call.function.arguments
                    }
                )
            )
            asyncio.run(self.websocket.send_text(response_event.json()))
        else:
            response_event = WebSocketMessage(
                event=EventType.SERVER_AI_RESPONSE,
                data=ServerResponse(content=text, status=AIResponseStatus.streaming)
            )
            asyncio.run(self.websocket.send_text(response_event.json()))

    def cancel_current_run(self, thread_id: str, websocket: WebSocket):
        self.websocket = websocket
        if self.current_run_id is not None:
            try:
                success = self.client.beta.threads.runs.cancel(run_id=self.current_run_id, thread_id=thread_id)
                print(f"Cancelled run: {success}")
                if success:
                    self.current_run_id = None

                    response_event = WebSocketMessage(
                        event=EventType.SERVER_AI_STATUS,
                        data=ServerResponse(
                            content="Run cancelled",
                            status=AIResponseStatus.aborted,
                            run_status=AIRunStatus.cancelled
                        )
                    )

                    asyncio.run(self.websocket.send_text(response_event.json()))

                    return True
            except Exception as e:
                print(f"Error cancelling run: {e}")
        return False

    def check_assistant_exists(self):
        if not self.assistant_id:
            print("Creating new assistant due to missing ID")
            created_assistant = self.create_assistant()
            if created_assistant is None:
                raise ValueError("Failed to create assistant")
            print("Assistant successfully created")
        else:
            try:
                print("Trying to retrieve assistant")
                self.assistant = self.client.beta.assistants.retrieve(self.assistant_id)
                print("Assistant successfully retrieved")
            except Exception as e:
                print(f"Error retrieving assistant: {e}")
                print("Creating new assistant due to failed retrieval")
                created_assistant = self.create_assistant()
                print("Assistant successfully created")
                if created_assistant is None:
                    raise ValueError("Failed to create or retrieve assistant")

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
                                
                                The information you retrieve using account_check, password_check and check_breaches 
                                will be visible to the user on the left side panel of the interface. This 
                                conversation takes place on the right side panel. While the account_check and 
                                check_breaches functions may return a truncated list in the conversation if there are 
                                many matches (maximum 50 results shown), the complete unabridged list of all results 
                                can always be found by the user on the left hand panel. Make sure to remind the user 
                                they can see the full details there if you aren't able to include everything in your 
                                response.
                                
                                Remember, your goal is to be a trusted resource for users seeking to safeguard their 
                                digital presence. Always prioritize their privacy, security, and well-being in your 
                                interactions.""",
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "tavily_search",
                            "description": "Search the internet for up-to-date information",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "The search query"
                                    }
                                },
                                "required": ["query"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "password_check",
                            "description": "Check if a password is in the password database",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "The password to check"
                                    }
                                },
                                "required": ["query"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "account_check",
                            "description": "Check if a username exists on various platforms",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "The username to check"
                                    }
                                },
                                "required": ["query"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "check_breaches",
                            "description": "Check if an email has been involved in data breaches using Have I Been "
                                           "Pwned",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "The email to check"
                                    }
                                },
                                "required": ["query"]
                            }
                        }
                    }
                ],
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
                model=model
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

    def handle_tool_calls(self, tool_calls, thread_id):
        outputs = []
        for index, tool_call in enumerate(tool_calls, start=1):
            if tool_call.function.name == "tavily_search":
                query = json.loads(tool_call.function.arguments)["query"]

                tool_call_event = WebSocketMessage(
                    event=EventType.SERVER_TOOL_CALL,
                    data=ServerResponse(
                        content=f"Tool call {index}: Tavily search for '{query}'",
                        status=AIResponseStatus.streaming,
                        metadata={
                            "tool_name": "tavily_search",
                            "query": query,
                            "tool_call_id": tool_call.id
                        }
                    )
                )
                asyncio.run(self.websocket.send_text(tool_call_event.json()))

                search_results = self.tavily_search.search(query)

                outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": json.dumps(search_results)
                })

                tool_call_complete_event = WebSocketMessage(
                    event=EventType.SERVER_TOOL_CALL,
                    data=ServerResponse(
                        content=f"Tool call {index} completed: Tavily search for '{query}'",
                        status=AIResponseStatus.completed,
                        metadata={
                            "tool_name": "tavily_search",
                            "query": query,
                            "tool_call_id": tool_call.id
                        }
                    )
                )
                asyncio.run(self.websocket.send_text(tool_call_complete_event.json()))

            if tool_call.function.name == "password_check":
                print("ai_service: tool call password query")
                query = json.loads(tool_call.function.arguments)["query"]

                tool_call_event = WebSocketMessage(
                    event=EventType.SERVER_TOOL_CALL,
                    data=ServerResponse(
                        content=f"Tool call {index}: Check the password '{query}'",
                        status=AIResponseStatus.streaming,
                        metadata={
                            "tool_name": "password_checks",
                            "query": query,
                            "tool_call_id": tool_call.id
                        }
                    )
                )
                asyncio.run(self.websocket.send_text(tool_call_event.json()))

                print("ai_service: calling password check with" + query)
                search_results = self.chromadb.search(query)

                outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": json.dumps(search_results)
                })

                tool_call_complete_event = WebSocketMessage(
                    event=EventType.SERVER_TOOL_CALL,
                    data=ServerResponse(
                        content=f"Tool call {index} completed: Check the password '{query}' + status: '{search_results}'",
                        status=AIResponseStatus.completed,
                        metadata={
                            "tool_name": "password_check",
                            "query": query,
                            "tool_call_id": tool_call.id,
                            "result": search_results
                        }
                    )
                )

                asyncio.run(self.websocket.send_text(tool_call_complete_event.json()))

            if tool_call.function.name == "account_check":
                print("ai_service: tool call account_check")
                query = json.loads(tool_call.function.arguments)["query"]

                tool_call_event = WebSocketMessage(
                    event=EventType.SERVER_TOOL_CALL,
                    data=ServerResponse(
                        content=f"Tool call {index}: Check the username '{query}'",
                        status=AIResponseStatus.streaming,
                        metadata={
                            "tool_name": "account_check",
                            "query": query,
                            "tool_call_id": tool_call.id
                        }
                    )
                )
                asyncio.run(self.websocket.send_text(tool_call_event.json()))

                print("ai_service: calling username check with:" + query)

                def progress_callback(query_result: QueryResult):
                    self.site_index += 1
                    progress_percentage = (self.site_index / 406) * 100

                    tool_call_event = WebSocketMessage(
                        event=EventType.SERVER_TOOL_CALL,
                        data=ServerResponse(
                            content=f"Tool call {tool_call.id}: Check the username '{query}'",
                            status=AIResponseStatus.streaming,
                            metadata={
                                "tool_name": "account_check",
                                "query": query,
                                "tool_call_id": tool_call.id,
                                "progress": f"{query_result.site_name} ({self.site_index} of 406)",
                                "progress_percentage": f"{progress_percentage:.2f}%"
                            }
                        )
                    )
                    asyncio.run(self.websocket.send_text(tool_call_event.json()))

                search_results = self.account_check.search(query, progress_callback)
                try:
                    filtered_results = []
                    for account in search_results[:50]:
                        filtered_account = {
                            "name": account["name"],
                            "url": account["url"],
                        }
                        filtered_results.append(filtered_account)

                    output_data = {
                        "totalAccounts": len(search_results),
                        "accountsIncludedInResults": min(50, len(search_results)),
                        "accounts": filtered_results
                    }

                    outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(output_data)
                    })
                except json.JSONDecodeError:
                    print("Error: search_results is not a valid JSON string")
                except TypeError:
                    print("Error: search_results is neither a list nor a JSON string")
                except KeyError as e:
                    print(f"Error: Missing key in account data: {e}")
                self.site_index = 0

                tool_call_complete_event = WebSocketMessage(
                    event=EventType.SERVER_TOOL_CALL,
                    data=ServerResponse(
                        content=f"Tool call {index} completed: Check the username '{query}'",
                        status=AIResponseStatus.completed,
                        metadata={
                            "tool_name": "account_check",
                            "query": query,
                            "tool_call_id": tool_call.id,
                            "result": search_results
                        }
                    )
                )
                asyncio.run(self.websocket.send_text(tool_call_complete_event.json()))

            if tool_call.function.name == "check_breaches":
                query = json.loads(tool_call.function.arguments)["query"]
                tool_call_event = WebSocketMessage(
                    event=EventType.SERVER_TOOL_CALL,
                    data=ServerResponse(
                        content=f"Tool call {index}: Check breaches for email '{query}'",
                        status=AIResponseStatus.streaming,
                        metadata={
                            "tool_name": "check_breaches",
                            "query": query,
                            "tool_call_id": tool_call.id
                        }
                    )
                )
                asyncio.run(self.websocket.send_text(tool_call_event.json()))

                breach_check_results = self.hibp.get_breaches(query)
                try:
                    if isinstance(breach_check_results, str):
                        breach_check_results_json = json.loads(breach_check_results)
                        filtered_results = []
                        for breach in breach_check_results_json[:50]:
                            filtered_breach = {
                                "Name": breach["Name"],
                                "Title": breach["Title"],
                                "Domain": breach["Domain"],
                                "BreachDate": breach["BreachDate"],
                            }
                            filtered_results.append(filtered_breach)

                        output_data = {
                            "totalBreaches": len(breach_check_results_json),
                            "breachesIncludedInResults": min(50, len(breach_check_results_json)),
                            "breaches": filtered_results
                        }

                        outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(output_data)
                        })
                except json.JSONDecodeError:
                    print("Error: breach_check_results is not a valid JSON string")
                except TypeError:
                    print("Error: breach_check_results is neither a list nor a JSON string")
                except KeyError as e:
                    print(f"Error: Missing key in breach data: {e}")
                tool_call_complete_event = WebSocketMessage(
                    event=EventType.SERVER_TOOL_CALL,
                    data=ServerResponse(
                        content=f"Tool call {index} completed: Check breaches for email '{query}'",
                        status=AIResponseStatus.completed,
                        metadata={
                            "tool_name": "check_breaches",
                            "query": query,
                            "tool_call_id": tool_call.id,
                            "result": breach_check_results
                        }
                    )
                )
                asyncio.run(self.websocket.send_text(tool_call_complete_event.json()))

        if outputs:
            submit_outputs_event = WebSocketMessage(
                event=EventType.SERVER_AI_STATUS,
                data=ServerResponse(
                    content="Submitting tool outputs to AI for processing",
                    status=AIResponseStatus.streaming,
                    run_status=AIRunStatus.in_progress
                )
            )
            asyncio.run(self.websocket.send_text(submit_outputs_event.json()))

            with self.client.beta.threads.runs.submit_tool_outputs_stream(
                    thread_id=thread_id,
                    run_id=self.current_run_id,
                    tool_outputs=outputs,
                    event_handler=self.EventHandler(self.text_callback, thread_id)
            ) as stream:
                stream.until_done()

        print("Tool calls handling completed")
