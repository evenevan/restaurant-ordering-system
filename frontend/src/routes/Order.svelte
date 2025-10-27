<script lang="ts">
import type { Order } from "$lib/stores/orders.svelte";
const { orderedAt, foodName, completedAt }: Order = $props();
</script>

<div class="flex flex-col">
    <p class="font-medium">{foodName}</p>
    <p class="text-xs text-muted-foreground">
        Ordered at {new Date(orderedAt).toLocaleTimeString()}
        <br>
        Status: {completedAt ? 'Received' : 'Pending'}
        {#if completedAt}
            <br>
            Received at {new Date(completedAt).toLocaleTimeString()}
        {/if}
    </p>
    
</div>
