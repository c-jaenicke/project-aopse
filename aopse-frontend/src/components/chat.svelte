<script lang="ts">
    import {afterUpdate, onDestroy, onMount} from 'svelte';
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
        clipboard, getModalStore,
        type ModalSettings,
        popup,
        type PopupSettings, ProgressRadial
    } from '@skeletonlabs/skeleton';
    import DOMPurify from 'dompurify';

    let currentMessage = '';
    let messageContainer: HTMLElement;
    const modalStore = getModalStore();


    function scrollToBottom() {
        messageContainer?.scrollTo({top: messageContainer.scrollHeight, behavior: 'smooth'});
    }

    let placeholders = {
        username: '',
        password: '',
        email: '',
        topic: ''
    };

    const usernames = [
        'johndoe123',
        'alice_smith',
        'tech_guru99',
        'security_pro',
        'NotAHacker42',
        'AdminForReal',
    ];

    const emails = [
        'example@email.com',
        'user@domain.com',
        'securityalert@company.com',
        'privacy@org.net',
        'password.is.password@yahoo.com',
        'ceo@totally-legit-business.com',
        'hackerman@l33t.net'
    ];

    const topics = [
        'cybersecurity',
        'data breaches',
        'password strength',
        'two-factor authentication',
        'teaching your cat to spot phishing emails',
        'why 123456 is still a popular password',
        'securing your Silk Road from digital highwaymen',
    ];

    const passwords = [
        'Str0ngP@ssw0rd!',
        'qwerty123',
        'hunter2',
        '2FA_Enabled_2023',
        'correct.horse.battery.staple',
        'iloveyou3000',
        'password123!',
    ];

    let interval: number;

    function updatePlaceholders() {
        placeholders = {
            username: usernames[Math.floor(Math.random() * usernames.length)],
            password: passwords[Math.floor(Math.random() * passwords.length)],
            email: emails[Math.floor(Math.random() * emails.length)],
            topic: topics[Math.floor(Math.random() * topics.length)]
        };
    }

    onMount(() => {
        scrollToBottom();
        updatePlaceholders();
        interval = setInterval(updatePlaceholders, 15000);
    });
    afterUpdate(scrollToBottom);

    onDestroy(() => {
        clearInterval(interval);
    });

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
            body: `
                <p>Are you sure you want to start a new thread?</p>
                <p>This will delete all current messages.</p>
            `,
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
            .replace(/^#### (.*$)/gm, '<h4>$1</h4>')
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

<div class="card bg-white dark:bg-gray-800 flex flex-col h-[calc(100vh-4rem)]">
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
        {#if $chatStore.length === 0}
            <div class="flex flex-col items-center justify-center h-full">
                <div class="flex items-center mb-6">
                    <span class="font-materialSymbols text-primary-500 text-3xl mr-2">chat</span>
                    <h2 class="text-2xl font-bold text-primary-500">Start chatting</h2>
                </div>
                <p class="text-lg text-gray-400 mb-8">Try asking about</p>
                <div class="relative overflow-hidden w-full">
                    <div class="animate-scroll-text inline-flex" style="--scroll-time: 20s;">
                        {#each Array(2) as _}
                            <div class="flex gap-6 px-3">
                                <div class="text-center w-64">
                                    <span class="font-materialSymbols text-primary-500 mb-1 text-2xl">account_circle</span>
                                    <p class="text-lg font-semibold text-primary-500 mb-2">Accounts</p>
                                    <p class="text-sm text-gray-400">Check the username "{placeholders.username}"</p>
                                </div>
                                <div class="text-center w-64">
                                    <span class="font-materialSymbols text-primary-500 mb-1 text-2xl">lock</span>
                                    <p class="text-lg font-semibold text-primary-500 mb-2">Password Leaks</p>
                                    <p class="text-sm text-gray-400">Check the password "{placeholders.password}"</p>
                                </div>
                                <div class="text-center w-64">
                                    <span class="font-materialSymbols text-primary-500 mb-1 text-2xl">mail</span>
                                    <p class="text-lg font-semibold text-primary-500 mb-2">Data Breaches</p>
                                    <p class="text-sm text-gray-400">Is {placeholders.email} in a breach?</p>
                                </div>
                                <div class="text-center w-64">
                                    <span class="font-materialSymbols text-primary-500 mb-1 text-2xl">search</span>
                                    <p class="text-lg font-semibold text-primary-500 mb-2">Security News</p>
                                    <p class="text-sm text-gray-400">Latest on {placeholders.topic}?</p>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
        {/if}
        {#each $chatStore as message, index}
            <div class="flex {message.sender === 'user' ? 'justify-end' : ''}">
                <div class="rounded-lg p-3 max-w-[70%] {message.sender === 'user' ? 'bg-primary-500 text-white' : 'bg-surface-200 dark:bg-gray-700'} relative group">
                    {#if message.sender === 'ai' && message.toolCalls}
                        <Accordion>
                            <AccordionItem open>
                                <svelte:fragment slot="lead">
                                    <span class="font-materialSymbols text-xl">build</span>
                                </svelte:fragment>
                                <svelte:fragment slot="summary">Tool Calls</svelte:fragment>
                                <svelte:fragment slot="content">
                                    <ol class="list">
                                        {#each message.toolCalls as toolCall, index (toolCall.id)}
                                            <li class="mb-2 flex items-start bg-blue-50 dark:bg-gray-600 p-2 rounded">
                                                <div class="flex items-center">
                                                    {#if toolCall.status}
                                                    <span class="px-2 py-1 rounded-full text-xs text-gray-300 inline-flex items-center justify-center">
                                                        {#if toolCall.status === 'completed'}
                                                        <span class="font-materialSymbols text-2xl leading-none mr-1">check</span>
                                                        {:else}
                                                        <span class="font-materialSymbols text-2xl leading-none mr-1 animate-pulse">hourglass_empty</span>
                                                        {/if}
                                                        {#if toolCall.progress_percentage && toolCall.progress_percentage !== '100.00%'}
                                                          <div class="inline-flex items-center">
                                                            <span class="text-l font-medium">{toolCall.progress_percentage}</span>
                                                          </div>
                                                        {/if}
                                                    </span>
                                                    {/if}
                                                    <div class="flex-auto">
                                                        <div class="flex items-center flex-wrap gap-2">
                                                            <span class="font-medium">{toolCall.name}:</span>
                                                            <span class="chip variant-filled-surface truncate max-w-xs">{toolCall.arguments}</span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        {/each}
                                    </ol>
                                </svelte:fragment>
                            </AccordionItem>
                        </Accordion>
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

