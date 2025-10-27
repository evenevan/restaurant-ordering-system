<script lang="ts">
import * as Card from "$lib/components/ui/card";
import { orderStore } from "$lib/stores/orders.svelte";
import FoodOrderDialog from "./FoodOrderDIalog.svelte";
import Order from "./Order.svelte";
const { tableNumber } = $props();
const tableOrders = $derived(
	orderStore.orders.filter((order) => order.tableNumber === tableNumber),
);
</script>

<Card.Root>
    <Card.Header>
        <Card.Title>Table {tableNumber}</Card.Title>
    </Card.Header>
    <Card.Content>
        <FoodOrderDialog {tableNumber} />
        <div class="flex flex-col gap-2">
            {#if tableOrders.length === 0}
                <p class="text-sm text-muted-foreground mt-4">No orders yet.</p>
            {:else}
                {#each tableOrders as order}
                    <Order {...order} />
                {/each}
            {/if}
        </div>
    </Card.Content>
</Card.Root>
