<script lang="ts">
    import {Accordion, AccordionItem} from '@skeletonlabs/skeleton';
</script>

<svelte:head>
    <title>Privacy Policy - AOPSE</title>
</svelte:head>

<div class="container mx-auto p-4">
    <h1 class="h1 mb-4">Privacy Policy</h1>

    <p class="mb-6">AOPSE (AI OSINT People Search Engine) is designed to help you assess and improve your online privacy
        and security. This policy outlines how we handle the information you provide when using our service.</p>

    <div class="card p-4 mb-6">
        <h2 class="h3 mb-2">Data Handling</h2>
        <p>AOPSE is designed to scan public databases and identify potential vulnerabilities in your online presence. To
            provide this service, we need to process the information you provide.</p>
    </div>

    <h2 class="h2 mt-8 mb-4">Key Privacy Points</h2>

    <Accordion>
        <AccordionItem>
            <svelte:fragment slot="lead"><span class="font-materialSymbols">analytics</span></svelte:fragment>
            <svelte:fragment slot="summary">Data Processing</svelte:fragment>
            <svelte:fragment slot="content">
                <p>The information you input is processed in real-time to provide our services. This processing occurs
                    through OpenAI's GPT models and our algorithms designed to assess online
                    vulnerabilities.</p>
            </svelte:fragment>
        </AccordionItem>
        <AccordionItem>
            <svelte:fragment slot="lead"><span class="font-materialSymbols">share</span></svelte:fragment>
            <svelte:fragment slot="summary">Data Storage</svelte:fragment>
            <svelte:fragment slot="content">
                <p>AOPSE is a stateless application, meaning we do not store your personal information on our servers.
                    However, to provide our service, we temporarily process your data and may cache results for the
                    duration of your session.</p>
            </svelte:fragment>
        </AccordionItem>
        <AccordionItem>
            <svelte:fragment slot="lead"><span class="font-materialSymbols">security</span></svelte:fragment>
            <svelte:fragment slot="summary">Data Security</svelte:fragment>
            <svelte:fragment slot="content">
                <p>We implement industry-standard security measures to protect your data during transmission and
                    processing. However, please be aware that no method of internet transmission is 100% secure.</p>
            </svelte:fragment>
        </AccordionItem>
    </Accordion>

    <div class="card p-4 mt-8">
        <h3 class="h3 mb-2">User Responsibility and Consent</h3>
        <p>By using AOPSE, you consent to the processing of the information you provide for the purpose of assessing
            your online privacy and security. While we need certain information to provide our service, we encourage you
            to be mindful of the details you share. Our goal is to help you improve your online security, not compromise
            it.</p>
    </div>

    <p class="mt-8">For more information about how OpenAI handles data processed through their models, please refer to
        <a href="https://openai.com/policies/privacy-policy" class="text-primary-500 hover:underline">OpenAI's Privacy
            Policy</a>.</p>
</div>
