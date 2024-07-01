<script lang="ts">
    import ProjectCard from '$lib/ProjectCard.svelte';
</script>

<svelte:head>
    <title>About</title>
</svelte:head>

<h1 class="h1 mb-4">About AOPSE</h1>

<p class="mb-6">Explore the inner workings of AOPSE on our GitHub repository!</p>
<br/>
<ProjectCard
        title="AI OSINT People Search Engine"
        content="AOPSE - An advanced search engine leveraging AI for Open Source Intelligence gathering on individuals."
        url="https://github.com/c-jaenicke/project-aopse"
        urlText="Explore on GitHub"
        tags={['AI', 'OSINT', 'Search Engine']}
        authors={[
    { avatar: "https://avatars.githubusercontent.com/u/72254270", name: "C. N. Jaenicke" },
    { avatar: "https://avatars.githubusercontent.com/u/107936933", name: "A. Tippe"},
    { initials: "IB", name: "I. Bingöl"}
  ]}
        icon="search"
/>

<br/>
<h2 class="h2 mt-8 mb-4">Our Technological Stack</h2>

<p class="mb-6">Here's an overview of the key components that power our project.</p>
<br/>

<section class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
    <ProjectCard
            title="Svelte"
            content="Cybernetically enhanced web apps"
            url="https://svelte.dev"
            urlText="svelte.dev"
            tags={['Frontend', 'JavaScript']}
            icon="code"
    />
    <ProjectCard
            title="Skeleton UI"
            content="A fully featured UI toolkit for Svelte + Tailwind"
            url="https://www.skeleton.dev"
            urlText="skeleton.dev"
            tags={['UI', 'Tailwind']}
            icon="palette"
    />
    <ProjectCard
            title="FastAPI"
            content="Modern, fast (high-performance), web framework for building APIs with Python"
            url="https://fastapi.tiangolo.com"
            urlText="fastapi.tiangolo.com"
            tags={['Backend', 'Python', 'API']}
            icon="bolt"
    />
</section>
