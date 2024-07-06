<script lang="ts">
	import '../app.postcss';
	import {AppShell, AppBar, LightSwitch, getModalStore} from '@skeletonlabs/skeleton';

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';

	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	// Modals & Toasts
	import { initializeStores, Modal, Toast } from '@skeletonlabs/skeleton';
	import type {ModalSettings} from "@skeletonlabs/skeleton";
	import {chatStore, isThreadLoading} from "../stores/chatStore.js";

	initializeStores()

	const modalStore = getModalStore();
	function openHelpModal() {
		const modal: ModalSettings = {
			type: 'alert',
			title: 'Help',
			body: 'The following prompts, or prompts similar to these, will execute a specific tool:\n' +
					'<strong class="font-bold"> check the username "username"</strong>will start a search for the username on different social media networks.\n' +
					'<strong class="font-bold"> check the password "password"</strong>will check if the password is present in one of the wordlists and give advice.\n' +
					'<strong class="font-bold"> has the email "email address" been breached</strong>will check if the given email address has been found in any breaches.\n' +
					'<strong class="font-bold"> is there any new information on "topic"</strong>will check for new information or news on the topic.'
		};
		modalStore.trigger(modal);
	}
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
					<button
							type="button"
							class="btn btn-sm variant-filled-warning"
							on:click={openHelpModal}
					>Help</button>
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
