<script>
import {InputChip} from "@skeletonlabs/skeleton";
</script>

<svelte:head>
	<title>AOPSE - Chat</title>
</svelte:head>

<div class="grid grid-cols-2 gap-4 h-full">
	<!-- PROFILE OF THE USER -->
	<div class="card bg-surface-100 dark:bg-gray-800">
		<header>
			<h2 class="h2 text-center">Profile</h2>
			<hr class="hr">
		</header>
		<section class="p-4">
			<!-- INFORMATION -->
		</section>
	</div>
	<!-- AI CHAT -->
	<div class="card bg-surface-100 dark:bg-gray-800">
		<header>
			<h2 class="h2 text-center">Chat</h2>
			<hr class="hr">
		</header>
		<section class="p-4">
			<!-- CHAT -->


		</section>

		<footer class="card-footer">
			<InputChip></InputChip>
		</footer>
	</div>
</div>