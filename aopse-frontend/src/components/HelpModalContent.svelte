<script lang="ts">
    import {getModalStore} from '@skeletonlabs/skeleton';

    const modalStore = getModalStore();
    $: modalData = $modalStore[0];

    const helpItems = [
        {
            title: "Check Username",
            prompt: "Check the username [username]",
            description: "This will search for the username on various social media networks.",
            icon: 'account_circle'
        },
        {
            title: "Check Password",
            prompt: "Check the password [password]",
            description: "This will verify if the password appears in any known wordlists and provide advice.",
            icon: 'lock'
        },
        {
            title: "Check Email for Breaches",
            prompt: "Has the email [email address] been breached",
            description: "This will check if the given email address has been found in any known data breaches.",
            icon: 'mail'
        },
        {
            title: "Search for New Information",
            prompt: "Is there any new information on [topic]",
            description: "This will search for recent information or news about the specified topic.",
            icon: 'search'
        }
    ];
</script>

<div class="w-modal-wide p-4 bg-white dark:bg-gray-800">
    <h2 class="h2 mb-4">{modalData?.title || 'Help'}</h2>
    <div class="overflow-y-auto max-h-[60vh]">
        <p class="text-lg mb-4">The following prompts, or similar ones, will execute specific tools:</p>

        <div class="space-y-4">
            {#each helpItems as item}
                <div class="card p-4 variant-soft">
                    <div class="flex items-center gap-3 mb-2">
                        <span class="font-materialSymbols text-xl">{item.icon}</span>
                        <h3 class="h3">{item.title}</h3>
                    </div>
                    <p class="font-bold text-primary-500 mb-2">{item.prompt}</p>
                    <p>{item.description}</p>
                </div>
            {/each}
        </div>
    </div>
</div>
