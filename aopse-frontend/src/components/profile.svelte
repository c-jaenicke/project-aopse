<script lang="ts">
    import {Accordion, AccordionItem, getModalStore, type ModalSettings, ProgressRadial} from '@skeletonlabs/skeleton';
    import {
        passwordFindings,
        accountFindings,
        breachFindings,
        type PasswordFinding,
        type AccountFinding,
        type BreachFinding
    } from "../stores/chatStore";

    function getPreviewItems<T>(items: T[]): T[] {
        return items.slice(0, 5);
    }

    const modalStore = getModalStore();

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
            return parsedUrl.hostname;
        } catch (e) {
            return url.length > 30 ? url.substring(0, 30) + '...' : url;
        }
    }

    $: leakedPasswords = $passwordFindings.filter(f => f.result === 'leaked').length;
    $: safePasswords = $passwordFindings.filter(f => f.result === 'safe').length;
    $: totalPasswords = $passwordFindings.length;

    $: usernamesInFindings = [...new Set($accountFindings.map(f => f.query))];
    $: emailsInFindings = [...new Set($breachFindings.map(f => f.query))];

</script>

<div class="card bg-white dark:bg-gray-800 shadow-md rounded-lg flex flex-col h-[calc(100vh-4rem)]">
    <header class="p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 class="h2 text-center">Privacy Profile</h2>
    </header>

    <section class="p-4 flex-grow overflow-y-auto space-y-4">
        <div class="card p-4 bg-surface-100 dark:bg-surface">
            <h3 class="h3 mb-4">Digital Exposure</h3>
            <hr class="opacity-50 mb-4"/>
            <div class="space-y-6">
                <div>
                    <h4 class="font-semibold mb-2">Usernames</h4>
                    {#if usernamesInFindings.length > 0}
                        <ul class="list-disc pl-5 space-y-1">
                            {#each usernamesInFindings as username}
                                <li class="text-gray-600 dark:text-gray-300">{username}</li>
                            {/each}
                        </ul>
                    {:else}
                        <p class="text-gray-600 dark:text-gray-300">No usernames found yet.</p>
                    {/if}
                </div>
                <div>
                    <h4 class="font-semibold mb-2">Emails</h4>
                    {#if emailsInFindings.length > 0}
                        <ul class="list-disc pl-5 space-y-1">
                            {#each emailsInFindings as email}
                                <li class="text-gray-600 dark:text-gray-300">{email}</li>
                            {/each}
                        </ul>
                    {:else}
                        <p class="text-gray-600 dark:text-gray-300">No emails found yet.</p>
                    {/if}
                </div>
            </div>
        </div>
        <Accordion>
            <AccordionItem>
                <svelte:fragment slot="lead">
                    <span class="font-materialSymbols text-2xl {leakedPasswords > 0 ? 'text-error-500' : 'text-success-500'}">lock</span>
                </svelte:fragment>
                <svelte:fragment slot="summary">
                    <div class="flex items-center justify-between">
                        <span>Passwords ({$passwordFindings.length})</span>
                    </div>
                </svelte:fragment>
                <svelte:fragment slot="content">
                    <p class="mb-4">
                        {#if leakedPasswords > 0}
            <span class="text-error-500">
                {leakedPasswords} of {totalPasswords}
                checked passwords {leakedPasswords === 1 ? 'has' : 'have'} been leaked.
            </span>
                        {:else}
            <span class="text-success-500">
                All {totalPasswords} checked passwords are safe.
            </span>
                        {/if}
                    </p>
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
                            <span class={finding.result === 'leaked' ? 'text-error-500' : 'text-success-500'}>
                                {finding.result}
                            </span>
                                    </td>
                                </tr>
                            {/each}
                            </tbody>
                        </table>
                        {#if $passwordFindings.length > 5}
                            <div class="flex items-center justify-center my-2">
                                <p class="mr-2">
                                    Showing 5 out of {$passwordFindings.length} items.
                                </p>
                                <button class="text-primary-500 flex items-center justify-center"
                                        on:click|stopPropagation={() => openModal($passwordFindings, `All Password Findings`)}>
                                    <span class="font-materialSymbols text-xl">open_in_full</span>
                                    <span class="ml-1">View all</span>
                                </button>
                            </div>
                        {/if}
                    </div>
                </svelte:fragment>

            </AccordionItem>

            <AccordionItem>
                <svelte:fragment slot="lead">
                    <span class="font-materialSymbols text-2xl">account_circle</span>
                </svelte:fragment>
                <svelte:fragment slot="summary">
                    <div class="flex items-center justify-between">
                        Accounts ({$accountFindings.length})
                    </div>
                </svelte:fragment>
                <svelte:fragment slot="content">
                    <p class="mb-4">We found {$accountFindings.length} accounts associated with your information.</p>
                    <div class="overflow-x-auto">
                        <table class="table-auto w-full">
                            <thead>
                            <tr class="bg-gray-100 dark:bg-gray-700">
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Username</th>
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Website</th>
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Link</th>
                            </tr>
                            </thead>
                            <tbody>
                            {#each getPreviewItems($accountFindings) as finding, index}
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.query}</td>
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.value}</td>
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">
                                        <a href={finding.result} target="_blank"
                                           class="text-primary-500 hover:text-primary-700 hover:underline">
                                            {shortenUrl(finding.result)}
                                        </a>
                                    </td>
                                </tr>
                            {/each}
                            </tbody>
                        </table>
                        {#if $accountFindings.length > 5}
                            <div class="flex items-center justify-center my-2">
                                <p class="mr-2">
                                    Showing 5 out of {$accountFindings.length} items.
                                </p>
                                <button class="text-primary-500 flex items-center justify-center"
                                        on:click|stopPropagation={() => openModal($accountFindings, `All Account Findings`)}>
                                    <span class="font-materialSymbols text-xl">open_in_full</span>
                                    <span class="ml-1">View all</span>
                                </button>
                            </div>
                        {/if}
                    </div>
                </svelte:fragment>
            </AccordionItem>

            <AccordionItem>
                <svelte:fragment slot="lead">
                    <span class="font-materialSymbols text-2xl {$breachFindings.length > 0 ? 'text-error-500' : 'text-success-500'}">security</span>
                </svelte:fragment>
                <svelte:fragment slot="summary">
                    <div class="flex items-center justify-between">
                        Breaches ({$breachFindings.length})
                    </div>
                </svelte:fragment>
                <svelte:fragment slot="content">
                    <p class="mb-4">
                        {#if $breachFindings.length > 0}
                            <span class="text-error-500">
                                Your information was found in {$breachFindings.length}
                                data {$breachFindings.length === 1 ? 'breach' : 'breaches'}.
                            </span>
                        {:else}
                            <span class="text-success-500">
                                No data breaches were found containing your information.
                            </span>
                        {/if}
                    </p>
                    <div class="overflow-x-auto">
                        <table class="table-auto w-full">
                            <thead>
                            <tr class="bg-gray-100 dark:bg-gray-700">
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Email</th>
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Domain</th>
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Breach Date</th>
                                <th class="px-4 py-2 text-left text-gray-600 dark:text-gray-300">Data Classes</th>
                            </tr>
                            </thead>
                            <tbody>
                            {#each getPreviewItems($breachFindings) as finding}
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.query}</td>
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.value}</td>
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.breachDate}</td>
                                    <td class="px-4 py-2 text-gray-800 dark:text-gray-300">{finding.dataClasses.join(', ')}</td>
                                </tr>
                            {/each}
                            </tbody>
                        </table>
                        {#if $breachFindings.length > 5}
                            <div class="flex items-center justify-center my-2">
                                <p class="mr-2">
                                    Showing 5 out of {$breachFindings.length} items.
                                </p>
                                <button class="text-primary-500 flex items-center justify-center"
                                        on:click|stopPropagation={() => openModal($breachFindings, `All Breach Findings`)}>
                                    <span class="font-materialSymbols text-xl">open_in_full</span>
                                    <span class="ml-1">View all</span>
                                </button>
                            </div>
                        {/if}
                    </div>
                </svelte:fragment>
            </AccordionItem>
        </Accordion>
    </section>
</div>
