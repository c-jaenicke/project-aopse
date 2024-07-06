<script>
	import '../app.postcss';
	import { AppShell, AppBar, LightSwitch } from '@skeletonlabs/skeleton';

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';

	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	// Modals & Toasts
	import { initializeStores, Modal, Toast } from '@skeletonlabs/skeleton';

	initializeStores()
</script>

<Modal />
<Toast />
<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<svelte:fragment slot="lead">
				<strong class="text-xl uppercase">
					<a href="/">AOPSE</a>
				</strong>

			</svelte:fragment>
			<svelte:fragment slot="trail">
				<nav class="hidden sm:flex items-center space-x-4">
					<a class="btn btn-sm variant-ghost-surface" href="/">Chat</a>
				</nav>
				<nav class="hidden sm:flex items-center space-x-4">
					<a class="btn btn-sm variant-ghost-surface" href="/about">About</a>
				</nav>
				<LightSwitch />
				<button class="btn btn-sm variant-ghost-surface sm:hidden">
					<span class="font-materialSymbols">menu</span>
				</button>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>

	<div class="px-4 sm:px-8 py-4 min-h-[calc(100vh-8rem)]">
		<!-- Page Route Content -->
		<slot />
	</div>

	<svelte:fragment slot="pageFooter">
		<footer class="bg-surface-100-800-token p-4">
			<div class="container mx-auto flex flex-col sm:flex-row justify-between items-center">
				<div class="mb-4 sm:mb-0">
					<p>&copy; AOPSE. All rights reserved.</p>
				</div>
				<nav class="flex flex-wrap justify-center sm:justify-end space-x-4">
					<a href="/" class="hover:underline">Home</a>
					<a href="/about" class="hover:underline">About</a>
					<a href="/privacy" class="hover:underline">Privacy Policy</a>
					<a href="/terms" class="hover:underline">Terms of Service</a>
				</nav>
			</div>
		</footer>
	</svelte:fragment>
</AppShell>
