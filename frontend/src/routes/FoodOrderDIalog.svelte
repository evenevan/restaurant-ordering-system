<script lang="ts">
import { Button, buttonVariants } from "$lib/components/ui/button";
import * as Dialog from "$lib/components/ui/dialog";
import { Input } from "$lib/components/ui/input";
import { Label } from "$lib/components/ui/label";
import { orderStore } from "$lib/stores/orders.svelte";
import { toast } from "svelte-sonner";

const { tableNumber } = $props();
let foodOrderName = $state("");
let isFoodOrderDialogOpen = $state(false);

const createOrder = async (e: SubmitEvent) => {
	try {
		e.preventDefault();
		await orderStore.orderFood(tableNumber, foodOrderName);
		toast.success("Order placed successfully!");
	} catch (error) {
		toast.error("Failed to place order.");
	} finally {
		foodOrderName = "";
		isFoodOrderDialogOpen = false;
	}
};
</script>

<Dialog.Root bind:open={isFoodOrderDialogOpen}>
    <Dialog.Trigger class={buttonVariants({ variant: 'outline' })}>
        Order Food
    </Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[425px]">
        <Dialog.Header>
            <Dialog.Title>Order Food</Dialog.Title>
        </Dialog.Header>
        <form onsubmit={createOrder}>
            <div class="grid gap-4 py-4">
                <Label for="food" class="text-right">Food Name</Label>
                <Input
                    id="food"
                    bind:value={foodOrderName}
                    class="col-span-3"
                />
            </div>
            <Dialog.Footer>
                <Button type="submit" disabled={!foodOrderName}>Order</Button>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>
