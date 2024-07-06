<script lang="ts">
    import {Accordion, AccordionItem, type ModalSettings, getModalStore} from '@skeletonlabs/skeleton';
    import {passwordFindings, accountFindings, breachFindings} from "../stores/chatStore";

    interface PasswordFinding {
        value: string;
        result: 'leaked' | 'safe';
    }

    interface AccountFinding {
        value: string;
        result: string;
    }

    interface BreachFinding {
        value: string;
        breachDate: string;
        dataClasses: string[];
    }

    const modalStore = getModalStore();

    function getPreviewItems<T>(items: T[]): T[] {
        return items.slice(0, 10);
    }

    function openModal(items: PasswordFinding[] | AccountFinding[] | BreachFinding[], title: string): void {
        const modal: ModalSettings = {
            type: 'component',
            component: 'fullListModal',
            title,
            meta: {items}
        };
        modalStore.trigger(modal);
    }

    function shortenUrl(url: string): string {
        try {
            const parsedUrl = new URL(url);
            let shortUrl = parsedUrl.hostname;
            if (parsedUrl.pathname !== '/') {
                shortUrl += parsedUrl.pathname.length > 20
                    ? parsedUrl.pathname.substring(0, 20) + '...'
                    : parsedUrl.pathname;
            }
            return shortUrl;
        } catch (e) {
            return url.length > 30 ? url.substring(0, 30) + '...' : url;
        }
    }

</script>

<div class="card bg-white dark:bg-gray-800 shadow-md rounded-lg flex flex-col h-[calc(100vh-4rem)]">
    <header class="p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 class="h2 text-center">Profile</h2>
    </header>

    <section class="p-4 flex-grow overflow-y-auto space-y-4">
        <Accordion>
            <AccordionItem>
                <svelte:fragment slot="lead">Passwords ({$passwordFindings.length})</svelte:fragment>
                <svelte:fragment slot="summary">Preview of password findings</svelte:fragment>
                <svelte:fragment slot="content">
                    <div class="overflow-x-auto">
                        <table class="table-auto w-full">
                            <thead>
                            <tr class="bg-gray-100 dark:bg-gray-700">
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Password</th>
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Status</th>
                            </tr>
                            </thead>
                            <tbody>
                            {#each getPreviewItems($passwordFindings) as finding}
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.value}</td>
                                    <td class="px-4 py-2">
                                    <span class={finding.result === 'leaked' ? 'text-red-500' : 'text-green-500'}>
                                        {finding.result}
                                    </span>
                                    </td>
                                </tr>
                            {/each}
                            </tbody>
                        </table>
                    </div>
                    {#if $passwordFindings.length > 10}
                        <button class="btn variant-filled mt-4 bg-blue-500 hover:bg-blue-600 text-white"
                                on:click={() => openModal($passwordFindings, `All Password Findings`)}>
                            Show all ({$passwordFindings.length})
                        </button>
                    {/if}
                </svelte:fragment>
            </AccordionItem>

            <AccordionItem>
                <svelte:fragment slot="lead">Accounts ({$accountFindings.length})</svelte:fragment>
                <svelte:fragment slot="summary">Preview of account findings</svelte:fragment>
                <svelte:fragment slot="content">
                    <div class="overflow-x-auto">
                        <table class="table-auto w-full">
                            <thead>
                            <tr class="bg-gray-100 dark:bg-gray-700">
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Account</th>
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Link</th>
                            </tr>
                            </thead>
                            <tbody>
                            {#each getPreviewItems($accountFindings) as finding}
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.value}</td>
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">
                                        <a href={finding.result} target="_blank" class="text-blue-500 hover:underline"
                                           title={finding.result}>
                                            {shortenUrl(finding.result)}
                                        </a>
                                    </td>
                                </tr>
                            {/each}
                            </tbody>
                        </table>
                    </div>
                    {#if $accountFindings.length > 10}
                        <button class="btn variant-filled mt-4 bg-blue-500 hover:bg-blue-600 text-white"
                                on:click={() => openModal($accountFindings, `All Account Findings`)}>
                            Show all ({$accountFindings.length})
                        </button>
                    {/if}
                </svelte:fragment>
            </AccordionItem>

            <AccordionItem>
                <svelte:fragment slot="lead">Breaches ({$breachFindings.length})</svelte:fragment>
                <svelte:fragment slot="summary">Preview of breach findings</svelte:fragment>
                <svelte:fragment slot="content">
                    <div class="overflow-x-auto">
                        <table class="table-auto w-full">
                            <thead>
                            <tr class="bg-gray-100 dark:bg-gray-700">
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Domain</th>
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Breach Date</th>
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Data Classes</th>
                            </tr>
                            </thead>
                            <tbody>
                            {#each getPreviewItems($breachFindings) as finding}
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.value}</td>
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.breachDate}</td>
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.dataClasses.join(', ')}</td>
                                </tr>
                            {/each}
                            </tbody>
                        </table>
                    </div>
                    {#if $breachFindings.length > 10}
                        <button class="btn variant-filled mt-4 bg-blue-500 hover:bg-blue-600 text-white"
                                on:click={() => openModal($breachFindings, `All Breach Findings`)}>
                            Show all ({$breachFindings.length})
                        </button>
                    {/if}
                </svelte:fragment>
            </AccordionItem>
        </Accordion>
    </section>
</div>
