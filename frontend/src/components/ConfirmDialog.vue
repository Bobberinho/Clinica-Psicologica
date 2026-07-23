<script setup>
import { onMounted, useTemplateRef } from 'vue';

const popup = useTemplateRef("popup")
const props = defineProps(["message"])
const emit = defineEmits(["confirm", "cancel"])
// const overlay = useTemplateRef("overlay")

function open() {
    popup.value.showModal()
}
function dialog_cancel() {
    emit("cancel")
    popup.value.close("closed")
}
function confirm() {
    emit("confirm")
    popup.value.close()
}
defineExpose({
    open,
})
</script>

<template>

<!-- <div class="overlay" ref="overlay"></div> -->
<dialog ref="popup">
    {{ message }}
    <div class="flex">
        <button @click="dialog_cancel()">Annulla</button>
        <button class="confirm" @click="confirm()">Conferma</button>
    </div>
</dialog>

</template>

<style scoped>
dialog[open] .flex {
    display: flex;
    text-align: center;
    margin-top: 1rem;
    gap: .5rem;
}
button.confirm {
    background: rgba(255, 0, 0, 7%);
    color: red;
    border-color: red;
}
button.confirm:hover {
    background: rgba(255, 0, 0, 12%);
}
dialog {
    background-color: white;
    padding: 2rem;
    width: fit-content;
    height: fit-content;
    border-radius: .8rem;
}
dialog::backdrop {
    background-color: rgba(0, 0, 0, 20%);
}
</style>