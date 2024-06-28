<script>
import Chat from "../components/chat.svelte";
import Profile from "../components/profile.svelte";
</script>

<svelte:head>
	<title>AOPSE - Chat</title>
</svelte:head>

<div class="grid grid-cols-2 gap-4 h-full">
    <Profile />
    <Chat />
</div>