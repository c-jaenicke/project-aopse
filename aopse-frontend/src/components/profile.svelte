<script lang="ts">
    import {findings} from "../stores/chatStore";

</script>

<div class="card bg-surface-100 dark:bg-gray-800 flex flex-col h-[calc(100vh-4rem)]">
    <header class="p-4 border-b border-surface-300 dark:border-gray-700">
        <h2 class="h2 text-center">Profile</h2>
    </header>
    <section class="p-4 flex-grow overflow-y-auto space-y-4">

        <h3 class="h3 mb-2">Information</h3>
        <div class="table-container">
            <table class="table table-hover">
                <thead>
                <tr>
                    <th>Type</th>
                    <th>Query</th>
                    <th>Result</th>
                </tr>
                </thead>
                <tbody>
                {#each $findings as finding, index}
                    <tr>
                        <td>
                            {#if finding.key === 'password_check'}
                                password
                            {:else if finding.key === 'account_check'}
                                username
                            {:else if finding.key === 'check_breaches'}
                                breach
                            {/if}
                        </td>
                        <td>{finding.value}</td>
                        <td>
                            {#if finding.key === 'account_check'}
                                <a href='{finding.result}' target='_blank'>link</a>
                            {:else}
                                {finding.result}
                            {/if}
                        </td>
                    </tr>
                {/each}
                </tbody>

            </table>
        </div>
    </section>
</div>
