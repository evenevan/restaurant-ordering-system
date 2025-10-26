<script lang="ts">
import { Button, buttonVariants } from "$lib/components/ui/button";
import * as Dialog from "$lib/components/ui/dialog";
import { Input } from "$lib/components/ui/input";
import { Label } from "$lib/components/ui/label";
</script>

<Dialog.Root>
    <Dialog.Trigger class={buttonVariants({ variant: 'outline' })}>
        Order Food
    </Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[425px]">
        <Dialog.Header>
            <Dialog.Title>Order Food</Dialog.Title>
        </Dialog.Header>
        <div class="grid gap-4 py-4">
            <Label for="food" class="text-right">Food Name</Label>
            <Input id="food" value="" class="col-span-3" />
        </div>
        <Dialog.Footer>
            <Button type="submit">Order</Button>
        </Dialog.Footer>
    </Dialog.Content>
</Dialog.Root>
