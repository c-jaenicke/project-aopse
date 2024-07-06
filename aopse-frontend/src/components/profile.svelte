<script lang="ts">
    import { Accordion, AccordionItem, type ModalSettings, getModalStore } from '@skeletonlabs/skeleton';
    import { findings } from "../stores/chatStore";

    interface Finding {
        key: string;
        value: string;
        result: string;
    }

    const modalStore = getModalStore();

    $: passwordFindings = ($findings as Finding[]).filter(f => f.key === 'password_check');
    $: accountFindings = ($findings as Finding[]).filter(f => f.key === 'account_check');
    $: breachFindings = ($findings as Finding[]).filter(f => f.key === 'check_breaches');

    function getPreviewItems<T>(items: T[]): T[] {
        return items.slice(0, 10);
    }

    function openModal(items: Finding[], title: string): void {
        const modal: ModalSettings = {
            type: 'component',
            component: 'fullListModal',
            title,
            meta: { items }
        };
        modalStore.trigger(modal);
    }
</script>

<div class="card bg-white dark:bg-gray-800 shadow-md rounded-lg flex flex-col h-[calc(100vh-4rem)]">
    <header class="p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 class="h2 text-center">Profile</h2>
    </header>

    <section class="p-4 flex-grow overflow-y-auto space-y-4">
        <Accordion>
            {#each [
                { title: 'Passwords', findings: passwordFindings, type: 'password' },
                { title: 'Accounts', findings: accountFindings, type: 'username' },
                { title: 'Breaches', findings: breachFindings, type: 'breach' }
            ] as { title, findings, type }}
                <AccordionItem>
                    <svelte:fragment slot="lead">{title} ({findings.length})</svelte:fragment>
                    <svelte:fragment slot="summary">Preview of {title.toLowerCase()} findings</svelte:fragment>
                    <svelte:fragment slot="content">
                        <div class="overflow-x-auto">
                            <table class="table-auto w-full">
                                <thead>
                                    <tr class="bg-gray-100 dark:bg-gray-700">
                                        <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Type</th>
                                        <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Query</th>
                                        <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Result</th>
                                    </tr>
                                </thead>
                                <tbody>
                                {#each getPreviewItems(findings) as finding}
                                    <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                                        <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{type}</td>
                                        <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.value}</td>
                                        <td class="px-4 py-2 text-gray-800 dark:text-gray-300">
                                            {#if type === 'username'}
                                                <a href={finding.result} target="_blank"
                                                   class="text-blue-500 hover:underline">link</a>
                                            {:else}
                                                {finding.result}
                                            {/if}
                                        </td>
                                    </tr>
                                {/each}
                                </tbody>
                            </table>
                        </div>
                        {#if findings.length > 10}
                            <button class="btn variant-filled mt-4 bg-blue-500 hover:bg-blue-600 text-white"
                                    on:click={() => openModal(findings, `All ${title} Findings`)}>
                                Show all ({findings.length})
                            </button>
                        {/if}
                    </svelte:fragment>
                </AccordionItem>
            {/each}
        </Accordion>
    </section>
</div>
