<script lang="ts">
    import {Avatar} from '@skeletonlabs/skeleton';

    export let title: string;
    export let content: string;
    export let url: string;
    export let urlText: string;
    export let tags: string[] = [];
    export let icon: string = 'code';
    export let authors: Array<{ avatar?: string; initials?: string; name: string }> = [];

    const MAX_DISPLAYED_AUTHORS = 3;
</script>

<div class="card card-hover flex flex-col h-full">
    <header class="card-header p-4 flex items-center gap-4">
        <div class="w-12 h-12 flex items-center justify-center rounded-full bg-primary-500 text-white flex-shrink-0">
            <span class="font-materialSymbols text-2xl">{icon}</span>
        </div>
        <div class="flex-grow">
            <h3 class="h3">{title}</h3>
            {#if authors.length > 0}
                <div class="flex items-center mt-2">
                    <div class="flex -space-x-2 overflow-hidden mr-2">
                        {#each authors.slice(0, MAX_DISPLAYED_AUTHORS) as author, index}
                            {#if author.avatar}
                                <Avatar src={author.avatar} width="w-6" rounded="rounded-full"
                                        border="border-2 border-surface-100-800-token"/>
                            {:else if author.initials}
                                <Avatar initials={author.initials} width="w-6" background="bg-secondary-500"
                                        border="border-2 border-surface-100-800-token"/>
                            {/if}
                        {/each}
                        {#if authors.length > MAX_DISPLAYED_AUTHORS}
                            <div class="w-6 h-6 flex items-center justify-center rounded-full bg-secondary-500 text-white text-xs border-2 border-surface-100-800-token">
                                +{authors.length - MAX_DISPLAYED_AUTHORS}
                            </div>
                        {/if}
                    </div>
                    <span class="text-sm text-surface-600-300-token">
            {authors.map(a => a.name).join(', ')}
          </span>
                </div>
            {/if}
        </div>
    </header>
    <section class="p-4 flex-grow">
        <p class="mb-4">{content}</p>
        {#if tags.length > 0}
            <div class="flex flex-wrap gap-2 mb-4">
                {#each tags as tag}
                    <span class="badge variant-filled-secondary">{tag}</span>
                {/each}
            </div>
        {/if}
    </section>
    <footer class="card-footer p-4 mt-auto">
        <a href={url} target="_blank" rel="noopener noreferrer" class="btn variant-filled-primary w-full">
            <span class="font-materialSymbols mr-2">open_in_new</span>
            {urlText}
        </a>
    </footer>
</div>
