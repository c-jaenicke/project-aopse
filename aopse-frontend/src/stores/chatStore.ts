import {get, type Writable, writable} from 'svelte/store';

export const isResponseLoading: Writable<boolean> = writable(false);
export const isThreadLoading: Writable<boolean> = writable(false);
export const isModelUpdating: Writable<boolean> = writable(false);
export const errorMessage: Writable<string | null> = writable(null);
export const threadId: Writable<string> = writable('');

export const Models = {
    GPT_4O: 'gpt-4o',
    GPT_4_TURBO: 'gpt-4-turbo',
    GPT_3_5_TURBO: 'gpt-3.5-turbo-0125',
} as const;

export type ModelType = typeof Models[keyof typeof Models];

export const currentModel: Writable<ModelType> = writable(Models.GPT_3_5_TURBO);

interface ToolCall {
    id: string;
    name: string;
    arguments: string;
    status: 'in_progress' | 'completed';
    progress_percentage?: string;
}


interface ChatMessage {
    text: string;
    sender: 'user' | 'ai';
    isLoading?: boolean;
    error?: boolean;
    toolCalls?: ToolCall[];
}

export interface PasswordFinding {
    value: string;
    result: 'leaked' | 'safe';
}

export interface AccountFinding {
    value: string;
    result: string;
    query: string;
}

export interface BreachFinding {
    value: string;
    breachDate: string;
    dataClasses: string[];
    query: string;
}

export const passwordFindings: Writable<PasswordFinding[]> = writable([]);
export const accountFindings: Writable<AccountFinding[]> = writable([]);
export const breachFindings: Writable<BreachFinding[]> = writable([]);

enum EventType {
    CLIENT_MESSAGE = "client_message",
    CLIENT_ABORT = "client_abort",
    CLIENT_INITIATE_THREAD = "client_initiate_thread",
    CLIENT_CHANGE_MODEL = "client_change_model",
    SERVER_CHANGE_MODEL = "server_change_model",
    SERVER_AI_RESPONSE = "server_ai_response",
    SERVER_SEND_THREAD = "server_send_thread",
    SERVER_ABORT = "server_abort",
    SERVER_ERROR = "server_error",
    SERVER_AI_STATUS = "server_ai_status",
    SERVER_TOOL_CALL = "server_tool_call",
    SERVER_REQUIRES_ACTION = "server_requires_action"
}

enum AIResponseStatus {
    STREAMING = "streaming",
    COMPLETED = "completed",
    ABORTED = "aborted"
}

enum AIRunStatus {
    QUEUED = "queued",
    IN_PROGRESS = "in_progress",
    COMPLETED = "completed",
    REQUIRES_ACTION = "requires_action",
    EXPIRED = "expired",
    CANCELLING = "cancelling",
    CANCELLED = "cancelled",
    FAILED = "failed",
    INCOMPLETE = "incomplete"
}

interface ServerResponse {
    status?: AIResponseStatus;
    content: string;
    run_status?: AIRunStatus;
    metadata?: {
        tool_name?: string;
        query?: string;
        tool_call_id?: string;
        result?: any;
        [key: string]: any;
    };
}

interface ClientMessage {
    thread_id: string;
    content: string;
}

interface WebSocketMessage {
    event: EventType;
    data?: ServerResponse | ClientMessage;
}

interface CheckBreachesResult {
}

interface CheckBreachesEntry {
    "Name": string;
    "Title": string;
    "Domain": string;
    "BreachDate": string;
    "AddedDate": string;
    "ModifiedDate": string;
    "PwnCount": number;
    "Description": string;
    "LogoPath": string;
    "DataClasses": string[];
    "IsVerified": boolean;
    "IsFabricated": boolean;
    "IsSensitive": boolean;
    "IsRetired": boolean;
    "IsSpamList": boolean;
    "IsMalware": boolean;
    "IsSubscriptionFree": boolean;
}

function createChatStore() {
    const chatMessages: Writable<ChatMessage[]> = writable([]);
    let socket: WebSocket | null = null;
    let reconnectAttempts = 0;
    const MAX_RECONNECT_ATTEMPTS = 5;

    function connectWebSocket(): void {
        try {
            socket = new WebSocket('ws://localhost:8000/ws/chat');
            socket.onopen = () => {
                console.log('WebSocket connected');
                reconnectAttempts = 0;
                errorMessage.set(null);
                initiateThread();
            };
            socket.onmessage = (event: MessageEvent) => {
                try {
                    const message: WebSocketMessage = JSON.parse(event.data);
                    handleServerMessage(message);
                } catch (error) {
                    console.error('Error processing message:', error);
                    errorMessage.set('Error processing server response');
                }
            };
            socket.onclose = (event: CloseEvent) => {
                console.log('WebSocket disconnected', event.reason);
                if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                    setTimeout(() => {
                        reconnectAttempts++;
                        connectWebSocket();
                    }, 5000 * Math.pow(2, reconnectAttempts));
                } else {
                    errorMessage.set('Unable to connect to server. Please try again later.');
                }
            };
            socket.onerror = (error: Event) => {
                console.error('WebSocket error:', error);
                errorMessage.set('WebSocket error occurred');
            };
        } catch (error) {
            console.error('Error connecting to WebSocket:', error);
            errorMessage.set('Failed to connect to server');
        }
    }

    function handleServerMessage(message: WebSocketMessage): void {
        switch (message.event) {
            case EventType.SERVER_AI_RESPONSE:
                handleAIResponse(message.data as ServerResponse);
                break;
            case EventType.SERVER_SEND_THREAD:
                handleNewThread(message.data as ServerResponse);
                break;
            case EventType.SERVER_CHANGE_MODEL:
                handleNewModel(message.data as ServerResponse);
                break;
            case EventType.SERVER_ABORT:
                handleAbort();
                break;
            case EventType.SERVER_ERROR:
                handleError(message.data?.content);
                break;
            case EventType.SERVER_AI_STATUS:
                handleAIStatus(message.data as ServerResponse);
                break;
            case EventType.SERVER_TOOL_CALL:
                handleToolCall(message.data as ServerResponse);
                break;
            case EventType.SERVER_REQUIRES_ACTION:
                handleRequiresAction(message.data as ServerResponse);
                break;
        }
    }

    function handleAIResponse(data?: ServerResponse): void {
        if (!data) return;
        chatMessages.update(messages => {
            const lastMessage = messages[messages.length - 1];
            if (lastMessage.sender === 'ai') {
                lastMessage.text += data.content;
                if (data.status === AIResponseStatus.STREAMING) {
                    isResponseLoading.set(true);
                    lastMessage.isLoading = true;
                } else if (data.status === AIResponseStatus.COMPLETED) {
                    isResponseLoading.set(false);
                    lastMessage.isLoading = false;
                }
            }
            return messages;
        });
    }

    function handleNewThread(data?: ServerResponse): void {
        if (data && data.content) {
            threadId.set(data.content);
            isThreadLoading.set(false);
            console.log('Thread ID:', data.content);
            clearMessages();
        } else {
            console.error('Received empty thread ID from server');
            errorMessage.set('Received empty thread ID from server');
        }
    }

    function handleNewModel(data?: ServerResponse): void {
        if (data && data.content) {
            const newModel = data.content;
            if (Object.values(Models).includes(newModel as ModelType)) {
                currentModel.set(newModel as ModelType);
                isModelUpdating.set(false);
                console.log('Model updated to:', newModel);
            } else {
                console.error('Received invalid model from server:', newModel);
                errorMessage.set('Received invalid model from server');
            }
        } else {
            console.error('Received empty model data from server');
            errorMessage.set('Received empty model data from server');
        }
    }

    function handleAbort(): void {
        isResponseLoading.set(false);
        chatMessages.update(messages => {
            const lastMessage = messages[messages.length - 1];
            if (lastMessage.sender === 'ai') {
                lastMessage.isLoading = false;
                lastMessage.text += ' (Aborted)';
            }
            return messages;
        });
    }

    function handleError(errorMsg?: string): void {
        isResponseLoading.set(false);
        errorMessage.set(errorMsg || 'An error occurred');
        chatMessages.update(messages => {
            const lastMessage = messages[messages.length - 1];
            if (lastMessage.sender === 'ai') {
                lastMessage.isLoading = false;
                lastMessage.error = true;
                lastMessage.text = 'Error: ' + (errorMsg || 'Unknown error');
            }
            return messages;
        });
    }

    function handleAIStatus(data: ServerResponse): void {
        console.log('AI Status:', data.content, 'Run Status:', data.run_status);
        // TODO: maybe update UI elements based on AI status
        // check if status is aborted and run status is cancelled
        if (data.status === AIResponseStatus.ABORTED && data.run_status === AIRunStatus.CANCELLED) {
            handleAbort();
        }
    }

    function handleToolCall(data: ServerResponse): void {
        if (data.metadata && typeof data.metadata === 'object' &&
            'tool_name' in data.metadata && 'query' in data.metadata && 'tool_call_id' in data.metadata) {

            const {tool_name: toolName, query, tool_call_id: toolCallId} = data.metadata;

            if (typeof toolName === 'string' && typeof query === 'string' && typeof toolCallId === 'string') {
                chatMessages.update(messages => {
                    const lastMessage = messages[messages.length - 1];
                    if (lastMessage.sender === 'ai') {
                        if (!lastMessage.toolCalls) {
                            lastMessage.toolCalls = [];
                        }
                        const existingToolCall = lastMessage.toolCalls.find(tc => tc.id === toolCallId);
                        if (existingToolCall) {
                            existingToolCall.status = data.status === AIResponseStatus.COMPLETED ? 'completed' : 'in_progress';

                            if (toolName === 'password_check') {
                                let result = '';
                                if (data.metadata && 'result' in data.metadata) {
                                    result = String(data.metadata.result);
                                }
                                handlePasswordCheck(query, result);
                            } else if (toolName === 'account_check') {
                                if (data.metadata && 'result' in data.metadata && Array.isArray(data.metadata.result)) {
                                    handleAccountCheck(data.metadata.result, query);
                                }
                                if (data.metadata && 'progress_percentage' in data.metadata) {
                                    existingToolCall.progress_percentage = String(data.metadata.progress_percentage);
                                }
                            } else if (toolName === 'check_breaches') {
                                if (data.metadata && 'result' in data.metadata && typeof data.metadata.result === 'string') {
                                    handleCheckBreaches(data.metadata.result, query);
                                }
                            }
                        } else {
                            lastMessage.toolCalls.push({
                                id: toolCallId,
                                name: toolName,
                                arguments: query,
                                status: data.status === AIResponseStatus.COMPLETED ? 'completed' : 'in_progress'
                            });
                        }
                    }
                    return messages;
                });
            }
        }
    }


    function handlePasswordCheck(query: string, result: string) {
        const finding: PasswordFinding = {
            value: query,
            result: result === "true" ? 'leaked' : 'safe'
        };
        passwordFindings.update(values => [...values, finding]);
    }

    function handleAccountCheck(result: any[], query: string) {
        const newFindings: AccountFinding[] = result.map(object => ({
            value: object.name,
            result: object.url,
            query: query
        }));
        accountFindings.update(values => [...values, ...newFindings]);
    }

    function handleCheckBreaches(result: string, query: string) {
        const parsedResult = JSON.parse(result);
        const newFindings: BreachFinding[] = parsedResult.map((object: CheckBreachesEntry) => ({
            value: object.Domain === '' ? object.Name : object.Domain,
            breachDate: object.BreachDate,
            dataClasses: object.DataClasses,
            query: query
        }));
        breachFindings.update(values => [...values, ...newFindings]);
    }


    function handleRequiresAction(data: ServerResponse): void {
        console.log('AI requires action:', data.content);
        // TODO: also maybe update UI elements based on this
    }

    function initiateThread(): void {
        if (socket && socket.readyState === WebSocket.OPEN) {
            const message: WebSocketMessage = {
                event: EventType.CLIENT_INITIATE_THREAD
            };
            socket.send(JSON.stringify(message));
            isThreadLoading.set(true);
        }
    }

    async function sendMessage(currentMessage: string): Promise<void> {
        if (currentMessage.trim() === '') {
            errorMessage.set('Message cannot be empty');
            return;
        }
        if (get(isResponseLoading)) {
            errorMessage.set('Please wait for the current message to complete');
            return;
        }
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            errorMessage.set('Not connected to server. Please try again.');
            return;
        }
        try {
            chatMessages.update(messages => [...messages, {text: currentMessage, sender: 'user'}]);
            chatMessages.update(messages => [...messages, {text: '', sender: 'ai', isLoading: true}]);
            isResponseLoading.set(true);
            errorMessage.set(null);
            const message: WebSocketMessage = {
                event: EventType.CLIENT_MESSAGE,
                data: {content: currentMessage, thread_id: get(threadId)}
            };
            socket.send(JSON.stringify(message));
        } catch (error) {
            console.error('Error sending message:', error);
            handleError('Failed to send message. Please try again.');
        }
    }

    function stopResponse(): void {
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            errorMessage.set('Not connected to server. Cannot stop response.');
            return;
        }
        try {
            const message: WebSocketMessage = {
                event: EventType.CLIENT_ABORT,
                data: {thread_id: get(threadId), content: ''}
            };
            socket.send(JSON.stringify(message));
        } catch (error) {
            console.error('Error stopping response:', error);
            errorMessage.set('Failed to stop response. Please try again.');
        }
    }

    function changeModel(model: ModelType): void {
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            errorMessage.set('Not connected to server. Cannot change model.');
            return;
        }
        try {
            const currentModelValue = get(currentModel);
            const message: WebSocketMessage = {
                event: EventType.CLIENT_CHANGE_MODEL,
                data: {content: model, thread_id: get(threadId)}
            };
            socket.send(JSON.stringify(message));
            isModelUpdating.set(true);
            const timeoutId = setTimeout(() => {
                if (get(isModelUpdating)) {
                    currentModel.set(currentModelValue);
                    isModelUpdating.set(false);
                    errorMessage.set('Model update timed out. Please try again.');
                    console.error('Model update timed out after 10 seconds');
                }
            }, 10000);
        } catch (error) {
            console.error('Error changing model:', error);
            errorMessage.set('Failed to change model. Please try again.');
        }
    }

    function clearMessages(): void {
        chatMessages.set([]);
    }

    connectWebSocket();

    return {
        subscribe: chatMessages.subscribe,
        isLoading: {subscribe: isResponseLoading.subscribe},
        errorMessage: {subscribe: errorMessage.subscribe},
        currentModel: {subscribe: currentModel.subscribe},
        sendMessage,
        stopResponse,
        changeModel,
        initiateThread
    };
}

export const chatStore = createChatStore();
