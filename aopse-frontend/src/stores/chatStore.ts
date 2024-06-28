import { writable, get } from 'svelte/store';

function createChatStore() {
    const chatMessages = writable([]);
    const isLoading = writable(false);
    let abortController: AbortController | null = null;

    async function sendMessage(currentMessage: string) {
        if (currentMessage.trim() !== '' && !get(isLoading)) {
            chatMessages.update(messages => [...messages, { text: currentMessage, sender: 'user' }]);
            chatMessages.update(messages => [...messages, { text: '', sender: 'ai', isLoading: true }]);
            isLoading.set(true);
            abortController = new AbortController();

            try {
                // Simulated LLM API response
                for (let i = 0; i < 5; i++) {
                    await new Promise((resolve, reject) => {
                        const timeout = setTimeout(() => {
                            chatMessages.update(messages => {
                                const lastMessage = messages[messages.length - 1];
                                if (lastMessage.sender === 'ai') {
                                    lastMessage.text += `AI response part ${i + 1}. `;
                                    lastMessage.isLoading = i < 4;
                                    return messages;
                                }
                                return messages;
                            });
                            resolve(null);
                        }, 1000);

                        abortController.signal.addEventListener('abort', () => {
                            clearTimeout(timeout);
                            reject(new Error('Aborted'));
                        });
                    });
                }
            } catch (error) {
                if (error.name === 'AbortError') {
                    chatMessages.update(messages => {
                        const lastMessage = messages[messages.length - 1];
                        if (lastMessage.sender === 'ai') {
                            lastMessage.text += ' (Response stopped)';
                            lastMessage.isLoading = false;
                        }
                        return messages;
                    });
                } else {
                    console.error('Error in AI response:', error);
                }
            } finally {
                if (abortController) {
                    isLoading.set(false);
                    abortController = null;
                }
            }
        }
    }

    function stopResponse() {
        if (abortController) {
            abortController.abort();
            chatMessages.update(messages => {
                const lastMessage = messages[messages.length - 1];
                if (lastMessage.sender === 'ai') {
                    lastMessage.isLoading = false;
                }
                return messages;
            });
            isLoading.set(false);
            abortController = null;
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
