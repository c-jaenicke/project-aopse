<script lang="ts">
    import { getModalStore } from '@skeletonlabs/skeleton';

    const modalStore = getModalStore();

    $: modalData = $modalStore[0];
    $: items = modalData?.meta?.items || [];
    $: title = modalData?.title || 'Full List';

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
                        <th class="px-4 py-2 text-left">Type</th>
                        <th class="px-4 py-2 text-left">Query</th>
                        <th class="px-4 py-2 text-left">Result</th>
                    </tr>
                </thead>
                <tbody>
                    {#each items as item}
                        <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700">
                            <td class="px-4 py-2 bg-white dark:bg-gray-800">{item.key}</td>
                            <td class="px-4 py-2 bg-white dark:bg-gray-800">{item.value}</td>
                            <td class="px-4 py-2 bg-white dark:bg-gray-800">
                                {#if item.key === 'account_check'}
                                    <a href={item.result} target="_blank" class="text-blue-500 hover:underline">link</a>
                                {:else}
                                    {item.result}
                                {/if}
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {:else}
        <p>No items to display.</p>
    {/if}
</div>
