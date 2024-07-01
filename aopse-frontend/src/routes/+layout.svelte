<script>
	import '../app.postcss';
	import { AppShell, AppBar, LightSwitch } from '@skeletonlabs/skeleton';

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';

	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	// Modals
	import { initializeStores, Modal } from '@skeletonlabs/skeleton';

	initializeStores()
</script>

<Modal />
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
				<strong class="text-xl uppercase">
					<a class="btn btn-sm variant-ghost-surface" href="/about"> About </a>
				</strong>
				<LightSwitch />
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<div class="px-8 py-2 h-full min-h-96">
		<!-- Page Route Content -->
		<slot />
	</div>
	<svelte:fragment slot="pageFooter">
		<AppBar>
			<svelte:fragment slot="lead">
				<div class="flex flex-wrap">
					<a href="/about">About</a>
				</div>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<LightSwitch />
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
</AppShell>
