<script lang="ts">
import { TABLE_COUNT } from "$lib/constants";
import TableCard from "./TableCard.svelte";
</script>

<div class="flex gap-4 h-full w-full place-items-start">
    {#each Array(TABLE_COUNT) as _, index}
        <TableCard tableNumber={index + 1} />
    {/each}
</div>
