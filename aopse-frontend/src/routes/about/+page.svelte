<script>
	import ProjectCard from '$lib/ProjectCard.svelte';
</script>

<svelte:head>
	<title>About</title>
</svelte:head>

<h1 class="h1">About</h1>

<p>You can view this project on Github!</p>
<br />
<ProjectCard
	title="GitHub/c-jaenicke/project-aopse"
	content="AI OSINT People Search Engine - AOPSE"
	url="https://github.com/c-jaenicke/project-aopse"
	urlText="https://github.com/c-jaenicke/project-aopse"
/>

<br />
<h2 class="h2">Stack</h2>

<p>The following software has been used to build this project.</p>
<br />

<section class="grid grid-cols-2 md:grid-cols-3 sm:grid-cols-1 gap-4">
	<div>
		<ProjectCard title="" content="" url="" urlText="" />
	</div>
	<div>
		<ProjectCard title="" content="" url="" urlText="" />
	</div>
	<div>
		<ProjectCard title="" content="" url="" urlText="" />
	</div>
</section>
