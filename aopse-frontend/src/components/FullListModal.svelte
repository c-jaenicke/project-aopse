<script lang="ts">
    import {getModalStore} from '@skeletonlabs/skeleton';

    const modalStore = getModalStore();
    $: modalData = $modalStore[0];
    $: items = modalData?.meta?.items || [];
    $: title = modalData?.title || 'Full List';
    $: type = title.toLowerCase().includes('password') ? 'password' :
        title.toLowerCase().includes('account') ? 'account' :
            title.toLowerCase().includes('breach') ? 'breach' : '';

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

    console.log('Modal Data:', modalData);
    console.log('Items:', items);
</script>

<div class="w-modal-wide p-4 bg-white dark:bg-gray-800">
    <h2 class="h2 mb-4">{title}</h2>
    {#if items && items.length > 0}
        <div class="overflow-y-auto max-h-[60vh]">
            <table class="table-auto w-full bg-white dark:bg-gray-800 shadow-lg">
                <thead>
                <tr class="bg-gray-200 dark:bg-gray-700">
                    {#if type === 'password'}
                        <th class="px-4 py-2 text-left">Password</th>
                        <th class="px-4 py-2 text-left">Status</th>
                    {:else if type === 'account'}
                        <th class="px-4 py-2 text-left">Account</th>
                        <th class="px-4 py-2 text-left">Link</th>
                    {:else if type === 'breach'}
                        <th class="px-4 py-2 text-left">Domain</th>
                        <th class="px-4 py-2 text-left">Breach Date</th>
                        <th class="px-4 py-2 text-left">Data Classes</th>
                    {/if}
                </tr>
                </thead>
                <tbody>
                {#each items as item}
                    <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700">
                        {#if type === 'password'}
                            <td class="px-4 py-2 bg-white dark:bg-gray-800">{item.value}</td>
                            <td class="px-4 py-2 bg-white dark:bg-gray-800">
                                    <span class={item.result === 'leaked' ? 'text-red-500' : 'text-green-500'}>
                                        {item.result}
                                    </span>
                            </td>
                        {:else if type === 'account'}
                            <td class="px-4 py-2 bg-white dark:bg-gray-800">{item.value}</td>
                            <td class="px-4 py-2 bg-white dark:bg-gray-800">
                                <a href={item.result} target="_blank" class="text-blue-500 hover:underline"
                                   title={item.result}>
                                    {shortenUrl(item.result)}
                                </a>
                            </td>
                        {:else if type === 'breach'}
                            <td class="px-4 py-2 bg-white dark:bg-gray-800">{item.value}</td>
                            <td class="px-4 py-2 bg-white dark:bg-gray-800">{item.breachDate}</td>
                            <td class="px-4 py-2 bg-white dark:bg-gray-800">{item.dataClasses.join(', ')}</td>
                        {/if}
                    </tr>
                {/each}
                </tbody>
            </table>
        </div>
    {:else}
        <p>No items to display.</p>
    {/if}
</div>
