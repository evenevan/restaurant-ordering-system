<script lang="ts">
import { onDestroy, onMount } from "svelte";
import { Toaster } from "$lib/components/ui/sonner";
import { ModeWatcher } from "mode-watcher";
import "../app.css";
let { children } = $props();
</script>

<div class="flex flex-col min-h-screen bg-background text-foreground">
    <main class="flex flex-1 flex-col p-4">
        {@render children()}
    </main>
</div>

<Toaster />
<ModeWatcher />
