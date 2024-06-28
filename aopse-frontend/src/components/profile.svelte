<script lang="ts">
import { ProgressRadial } from '@skeletonlabs/skeleton';

let userInfo = {
    email: 'user@example.com',
    username: 'user',
    socialMedia: ['Facebook', 'Twitter', 'LinkedIn']
};

let privacyScore = 65;

let vulnerabilities = [
    'Weak password',
    'Public social media profiles',
    'Unsecured network usage'
];

let leakedPasswords = 2;

function getAdvice(vulnerability: string) {
    console.log(`Getting advice for ${vulnerability}`);
}
</script>

<div class="card bg-surface-100 dark:bg-gray-800 flex flex-col h-[calc(100vh-4rem)]">
    <header class="p-4 border-b border-surface-300 dark:border-gray-700">
        <h2 class="h2 text-center">Profile</h2>
    </header>
    <section class="p-4 flex-grow overflow-y-auto space-y-4">

        <div>
            <h3 class="h3 mb-2">User Information</h3>
            <p>Email: {userInfo.email}</p>
            <p>Username: {userInfo.username}</p>
            <p>Social Media: {userInfo.socialMedia.join(', ')}</p>
        </div>

        <div>
            <h3 class="h3 mb-2">Privacy Score</h3>
            <ProgressRadial value={privacyScore} meter="stroke-primary-500">
                {privacyScore}%
            </ProgressRadial>
        </div>

        <div>
            <h3 class="h3 mb-2">Vulnerabilities</h3>
            <ul class="list">
                {#each vulnerabilities as vulnerability}
                    <li>
                        <button class="btn variant-soft w-full text-left" on:click={() => getAdvice(vulnerability)}>
                            {vulnerability}
                        </button>
                    </li>
                {/each}
            </ul>
        </div>

        {#if leakedPasswords > 0}
            <div>
                <h3 class="h3 mb-2">Leaked Passwords</h3>
                <p class="text-error-500">
                    We found {leakedPasswords} leaked password{leakedPasswords > 1 ? 's' : ''} associated with your email.
                    Please change {leakedPasswords > 1 ? 'them' : 'it'} immediately!
                </p>
            </div>
        {/if}
    </section>
</div>
