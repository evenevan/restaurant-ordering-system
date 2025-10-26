<script lang="ts">
import * as Card from "$lib/components/ui/card";
import FoodOrderDIalog from "./FoodOrderDIalog.svelte";
const { tableNumber } = $props();
</script>

<Card.Root>
    <Card.Header>
        <Card.Title>Table {tableNumber}</Card.Title>
        <Card.Description>desc</Card.Description>
    </Card.Header>
    <Card.Content>
        <FoodOrderDIalog />
    </Card.Content>
</Card.Root>
