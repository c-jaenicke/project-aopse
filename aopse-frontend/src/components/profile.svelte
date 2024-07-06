<script lang="ts">
    import {findings} from "../stores/chatStore";

    $: passwordFindings = $findings.filter(f => f.key === 'password_check');
    $: accountFindings = $findings.filter(f => f.key === 'account_check');
    $: breachFindings = $findings.filter(f => f.key === 'check_breaches');
</script>

<div class="card bg-surface-100 dark:bg-gray-800 flex flex-col h-[calc(100vh-4rem)]">
    <header class="p-4 border-b border-surface-300 dark:border-gray-700">
        <h2 class="h2 text-center">Profile</h2>
    </header>

    <section class="p-4 flex-grow overflow-y-auto space-y-4">
        <h3 class="h3 mb-2">Passwords</h3>
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
                {#each passwordFindings as finding}
                    <tr>
                        <td>password</td>
                        <td>{finding.value}</td>
                        <td>{finding.result}</td>
                    </tr>
                {/each}
                </tbody>
            </table>
        </div>

        <h3 class="h3 mb-2">Accounts</h3>
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
                {#each accountFindings as finding}
                    <tr>
                        <td>username</td>
                        <td>{finding.value}</td>
                        <td><a href='{finding.result}' target='_blank'>link</a></td>
                    </tr>
                {/each}
                </tbody>
            </table>
        </div>

        <h3 class="h3 mb-2">Breaches</h3>
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
                {#each breachFindings as finding}
                    <tr>
                        <td>breach</td>
                        <td>{finding.value}</td>
                        <td>{finding.result}</td>
                    </tr>
                {/each}
                </tbody>
            </table>
        </div>
    </section>
</div>
