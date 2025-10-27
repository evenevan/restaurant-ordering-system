<script lang="ts">
    import { onMount } from 'svelte';
    import { Toaster } from '$lib/components/ui/sonner';
    import { ModeWatcher } from 'mode-watcher';
    import '../app.css';
    import { orderStore } from '$lib/stores/orders.svelte';

    let { children } = $props();
    let isLoading = $state(true);
    let errorMessage = $state<string | null>(null);

    onMount(async () => {
        try {
            await orderStore.init();
        } catch (err) {
            errorMessage =
                err instanceof Error
                    ? err.message
                    : 'Failed to initialize order system';
        } finally {
            isLoading = false;
        }
    });
</script>

<div class="flex flex-col min-h-screen bg-background text-foreground">
    <main class="flex flex-1 flex-col p-4">
        {#if isLoading}
            <p>Loading... (‾◡◝)</p>
        {:else if errorMessage}
            <div>
                <p>{errorMessage}</p>
                <button
                    onclick={() => window.location.reload()}
                    class="underline"
                >
                    Retry
                </button>
            </div>
        {:else}
            {@render children()}
        {/if}
    </main>
</div>

<Toaster />
<ModeWatcher />
