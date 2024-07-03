<script lang="ts">
    import {afterUpdate, onMount} from 'svelte';
    import {
        chatStore,
        currentModel,
        isModelUpdating,
        isResponseLoading,
        isThreadLoading,
        Models,
        type ModelType,
        threadId
    } from '../stores/chatStore.js';
    import {
        Accordion,
        AccordionItem,
        clipboard,
        getModalStore,
        type ModalSettings,
        popup,
        type PopupSettings
    } from '@skeletonlabs/skeleton';
    import DOMPurify from 'dompurify';

    let currentMessage = '';
    let messageContainer: HTMLElement;
    const modalStore = getModalStore();


    function scrollToBottom() {
        messageContainer?.scrollTo({top: messageContainer.scrollHeight, behavior: 'smooth'});
    }

    onMount(scrollToBottom);
    afterUpdate(scrollToBottom);

    function handleSendMessage() {
        if (!$isResponseLoading) {
            chatStore.sendMessage(currentMessage);
            currentMessage = '';
        }
    }

    function handleNewThread() {
        const modal: ModalSettings = {
            type: 'confirm',
            title: 'Start New Thread',
            body: 'Are you sure you want to start a new thread? This will delete all current messages.',
            response: (r: boolean) => {
                if (r) {
                    chatStore.initiateThread();
                }
            }
        };
        modalStore.trigger(modal);
    }

    function handleModelChange(event: Event) {
        if (!$isModelUpdating) {
            const select = event.target as HTMLSelectElement;
            chatStore.changeModel(select.value as ModelType);
        }
    }

    const copyPopup: PopupSettings = {
        event: 'click',
        target: 'copyPopup',
        placement: 'top'
    };


    function formatMessage(text: string): string {
        const encodedText = text
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        const rawHtml = encodedText
            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
            .replace(/\*(.*?)\*/g, '<i>$1</i>')
            .replace(/~~(.*?)~~/g, '<del>$1</del>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/^### (.*$)/gm, '<h3>$1</h3>')
            .replace(/^\> (.*$)/gm, '<blockquote>$1</blockquote>')
            .replace(/\n/g, '<br>')
            .replace(/^\* (.*$)/gm, '<li>$1</li>')
            .replace(/^([0-9]+\. .*$)/gm, '<li>$1</li>')
            .replace(/<\/li>\n<li>/g, '</li><li>')
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
            .replace(/\[([^\]]+)\]\(([^\)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="anchor hover:underline text-primary-500 hover:text-primary-700">$1</a>');

        return DOMPurify.sanitize(rawHtml, {
            ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'blockquote', 'code', 'del'],
            ALLOWED_ATTR: ['href', 'target', 'rel', 'class']
        });
    }
</script>

<div class="card bg-surface-100 dark:bg-gray-800 flex flex-col h-[calc(100vh-4rem)]">
    <header class="p-4 border-b border-surface-300 dark:border-gray-700">
        <h2 class="h2 text-center">Chat</h2>
    </header>

    <Accordion class="w-full mb-4">
        <AccordionItem>
            <svelte:fragment slot="lead">
                <span class="font-materialSymbols text-2xl text-primary-500">settings</span>
            </svelte:fragment>
            <svelte:fragment slot="summary">
                <span class="text-lg font-semibold">Chat Settings</span>
            </svelte:fragment>
            <svelte:fragment slot="content">
                <div class="space-y-6 p-4 bg-surface-200 dark:bg-surface-700 rounded-b-lg">
                    <div class="flex flex-col space-y-2">
                        <label for="thread-id" class="text-sm font-medium">Current Thread</label>
                        <div class="flex items-center space-x-2">
                            <input
                                    id="thread-id"
                                    type="text"
                                    readonly
                                    value={$threadId}
                                    class="input input-sm flex-grow"
                            />
                            <button
                                    type="button"
                                    class="btn btn-sm variant-filled-primary"
                                    on:click={handleNewThread}
                                    disabled={$isThreadLoading}
                            >
                                {#if $isThreadLoading}
                                    <span class="font-materialSymbols text-2xl animate-spin">refresh</span>
                                {:else}
                                    <span class="font-materialSymbols text-2xl">add</span>
                                {/if}
                                <span>New Thread</span>
                            </button>
                        </div>
                    </div>

                    <div class="flex flex-col space-y-2">
                        <label for="model-select" class="text-sm font-medium">AI Model</label>
                        <div class="flex items-center space-x-2">
                            <select
                                    id="model-select"
                                    class="select select-sm flex-grow"
                                    value={$currentModel}
                                    on:change={handleModelChange}
                                    disabled={$isModelUpdating}
                            >
                                {#each Object.entries(Models) as [key, value]}
                                    <option value={value}>{key}</option>
                                {/each}
                            </select>
                            {#if $isModelUpdating}
                                <span class="font-materialSymbols text-2xl animate-spin text-primary-500">sync</span>
                            {/if}
                        </div>
                    </div>
                </div>
            </svelte:fragment>
        </AccordionItem>
    </Accordion>

    <section bind:this={messageContainer} class="flex-grow overflow-y-auto p-4 space-y-4 h-full">
        {#each $chatStore as message, index}
            <div class="flex {message.sender === 'user' ? 'justify-end' : ''}">
                <div class="rounded-lg p-3 max-w-[70%] {message.sender === 'user' ? 'bg-primary-500 text-white' : 'bg-surface-200 dark:bg-gray-700'} relative group">
                    {#if message.sender === 'ai' && message.toolCalls}
                        <div class="mb-2 p-2 bg-surface-300 dark:bg-gray-600 rounded">
                            <h4 class="text-sm font-semibold mb-1">Tool Calls:</h4>
                            {#each message.toolCalls as toolCall (toolCall.id)}
                                <div class="text-xs mb-1">
                                    <span class="font-medium">{toolCall.name}:</span> {toolCall.arguments}
                                    {#if toolCall.status}
                                        <span class="ml-1 px-1 py-0.5 rounded text-xs {toolCall.status === 'completed' ? 'bg-green-500' : 'bg-yellow-500'}">
                                            {toolCall.status}
                                        </span>
                                    {/if}
                                </div>
                            {/each}
                        </div>
                    {/if}
                    <div class="{message.sender === 'ai' && !message.isLoading ? 'pb-6' : ''}">
                        {#if message.sender === 'ai'}
                            <div class="whitespace-pre-wrap break-words">
                                {@html formatMessage(message.text)}
                            </div>
                        {:else}
                            <div>{message.text}</div>
                        {/if}
                        {#if message.sender === 'ai' && message.isLoading}
                            <span class="inline-block animate-pulse">▋</span>
                        {/if}
                    </div>
                    {#if message.sender === 'ai' && !message.isLoading}
                        <button
                                use:clipboard={message.text}
                                use:popup={copyPopup}
                                class="absolute bottom-1 right-1 text-sm opacity-50 hover:opacity-100 transition-opacity"
                        >
                            <span class="font-materialSymbols text-lg">content_copy</span>
                        </button>
                    {/if}
                </div>
            </div>
        {/each}
    </section>


    <footer class="p-4 border-t border-surface-300 dark:border-gray-700 mt-auto">
        <div class="input-group input-group-divider grid-cols-[1fr_auto]">
            <input
                    bind:value={currentMessage}
                    type="text"
                    placeholder="Type a message..."
                    class="input"
                    on:keydown={(e) => e.key === 'Enter' && !$isResponseLoading && handleSendMessage()}
                    disabled={$isResponseLoading}
            />
            <button
                    type="button"
                    class={`btn ${$isResponseLoading ? 'variant-filled-error' : 'variant-filled-primary'}`}
                    on:click={$isResponseLoading ? chatStore.stopResponse : handleSendMessage}
            >
                <span class="font-materialSymbols text-2xl">{$isResponseLoading ? 'stop' : 'send'}</span>
                <span>{$isResponseLoading ? 'Stop' : 'Send'}</span>
            </button>
        </div>
    </footer>
</div>

<div class="card p-2 variant-filled-success" data-popup="copyPopup">
    <span class="font-materialSymbols">check</span>
    <div class="arrow variant-filled-success"/>
</div>

