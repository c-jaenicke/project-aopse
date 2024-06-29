// chatStore.js
import {get, writable} from 'svelte/store';

export const isLoading = writable(false);

function createChatStore() {
    const chatMessages = writable([]);
    let socket: WebSocket | null = null;

    function connectWebSocket() {
        socket = new WebSocket('ws://localhost:8000/ws/chat');

        socket.onopen = () => {
            console.log('WebSocket connected');
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.event === 'server_ai_response') {
                chatMessages.update(messages => {
                    const lastMessage = messages[messages.length - 1];
                    if (lastMessage.sender === 'ai') {
                        lastMessage.text += data.data.content;
                        if (data.data.status === 'streaming') {
                            isLoading.set(true);
                           lastMessage.isLoading = true;
                        } else if (data.data.status === 'completed') {
                            isLoading.set(false);
                            lastMessage.isLoading = false;
                        }
                        console.log('Is loading:', get(isLoading));
                    }
                    return messages;
                });
            }
        };

        socket.onclose = () => {
            console.log('WebSocket disconnected');
            setTimeout(connectWebSocket, 5000);
        };
    }

    connectWebSocket();

    async function sendMessage(currentMessage: string) {
        if (currentMessage.trim() !== '' && !get(isLoading) && socket && socket.readyState === WebSocket.OPEN) {
            chatMessages.update(messages => [...messages, { text: currentMessage, sender: 'user' }]);
            chatMessages.update(messages => [...messages, { text: '', sender: 'ai', isLoading: true }]);
            isLoading.set(true);
            console.log('Is loading:', get(isLoading));
            try {
                socket.send(JSON.stringify({
                    event: 'client_message',
                    data: { thread_id: "thread_eilRlSu64KfgZlyoF6ANhLi5", content: currentMessage }
                }));
            } catch (error) {
                console.error('Error sending message:', error);
                chatMessages.update(messages => {
                    const lastMessage = messages[messages.length - 1];
                    if (lastMessage.sender === 'ai') {
                        lastMessage.text = 'Error: Failed to send message';
                        lastMessage.isLoading = false;
                    }
                    return messages;
                });
            } finally {
                //do nothing
            }
        }
    }

    function stopResponse() {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ event: 'abort' }));
            chatMessages.update(messages => {
                const lastMessage = messages[messages.length - 1];
                if (lastMessage.sender === 'ai') {
                    lastMessage.isLoading = false;
                    lastMessage.text += ' (Response stopped)';
                }
                return messages;
            });
            isLoading.set(false);
        }
    }

    return {
        subscribe: chatMessages.subscribe,
        isLoading: { subscribe: isLoading.subscribe },
        sendMessage,
        stopResponse
    };
}

export const chatStore = createChatStore();
