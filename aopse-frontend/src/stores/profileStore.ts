import {get, type Writable, writable} from 'svelte/store';

export const isResponseLoading: Writable<boolean> = writable(false);
export const isThreadLoading: Writable<boolean> = writable(false);
export const isModelUpdating: Writable<boolean> = writable(false);
export const errorMessage: Writable<string | null> = writable(null);
export const threadId: Writable<string> = writable('');

interface Finding {
    key: string;
    value: string;
    text: string;
}

enum EventType {
    SERVER_FINDING_RESPONSE = "server_finding_response"
}

interface ServerResponse {
    content: string;
}

interface WebSocketMessage {
    event: EventType;
    data?: ServerResponse;
}

function createProfileStore() {
    const findings: Writable<Finding[]> = writable([]);
    let socket: WebSocket | null = null;
    let reconnectAttempts = 0;
    const MAX_RECONNECT_ATTEMPTS = 5;

    function connectWebSocket(): void {
        try {
            socket = new WebSocket('ws://localhost:8000/ws/chat');
            socket.onopen = () => {
                console.log('WebSocket for profile connected');
                reconnectAttempts = 0;
                errorMessage.set(null);
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
        console.log("new message in profile")
        switch (message.event) {
            case EventType.SERVER_FINDING_RESPONSE:
                handleFinding(message.data as ServerResponse)
                break;
        }
    }

    function handleFinding(data: ServerResponse): void {
        if (!data) return;
        findings.update(messages => [...messages]);
        console.log("Profile: findings" + findings)
    }

    connectWebSocket();

    return {
        subscribe: findings.subscribe,
        isLoading: {subscribe: isResponseLoading.subscribe},
        errorMessage: {subscribe: errorMessage.subscribe},
    };
}

export const profileStore = createProfileStore();
