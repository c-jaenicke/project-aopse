<script lang="ts">
  import { onMount, afterUpdate } from 'svelte';
  import { chatStore, isLoading } from '../stores/chatStore.js';

  let currentMessage = '';
  let messageContainer: HTMLElement;

  function scrollToBottom() {
      console.log('i received isloading as', $isLoading)
      messageContainer?.scrollTo({ top: messageContainer.scrollHeight, behavior: 'smooth' });
  }

  onMount(scrollToBottom);
  afterUpdate(scrollToBottom);

  function handleSendMessage() {
      if (!$isLoading) {
          chatStore.sendMessage(currentMessage);
          currentMessage = '';
      }
  }
</script>

<div class="card bg-surface-100 dark:bg-gray-800 flex flex-col h-[calc(100vh-4rem)]">
    <header class="p-4 border-b border-surface-300 dark:border-gray-700">
        <h2 class="h2 text-center">Chat</h2>
    </header>
    <section bind:this={messageContainer} class="flex-grow overflow-y-auto p-4 space-y-4 h-full">
        {#each $chatStore as message}
            <div class="flex {message.sender === 'user' ? 'justify-end' : ''}">
                <div class="rounded-lg p-3 max-w-[70%] {message.sender === 'user' ? 'bg-primary-500 text-white' : 'bg-surface-200 dark:bg-gray-700'}">
                    {message.text}
                    {#if message.sender === 'ai' && message.isLoading}
                        <span class="inline-block animate-pulse">▋</span>
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
                on:keydown={(e) => e.key === 'Enter' && !$isLoading && handleSendMessage()}
                disabled={$isLoading}
            />
            <button
                    type="button"
                    class={`btn ${$isLoading ? 'variant-filled-error' : 'variant-filled-primary'}`}
                    on:click={$isLoading ? chatStore.stopResponse : handleSendMessage}
            >
                <span>{$isLoading ? 'Stop' : 'Send'}</span>
            </button>
        </div>
    </footer>
</div>
