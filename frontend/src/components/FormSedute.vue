<script setup>
import Close from '@/icons/Close.vue';
import { api_get, sort } from '@/util';
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import AddButton from './building_components/AddButton.vue';

const route = useRoute()

const form_open = ref(false)
const emit = defineEmits(["after_submit"])

const description = ref("")
const default_date = (new Date()).toISOString().split('T')[0]
const date = ref(default_date)
const time = ref("")

async function add_session(event) {
    event.preventDefault()
    const full_date = `${date.value} ${time.value}`
    const session = {
        ID_Paziente: route.params.id,
        ID_Specialista: -1,
        Descrizione: description.value,
        Data: full_date,
    }
    console.log(session)
    await api_get(`${route.path}/seduta`, "", "POST", session)
    reset()
    emit("after_submit")
}
function reset() {
    description.value = ""
    date.value = default_date
    time.value = ""
    form_open.value = false
}
</script>

<template>
<AddButton v-if="!form_open" @click="form_open = true" text="Registra una seduta"></AddButton>

<section class="form-container" v-if="form_open">
    <header>
        <h3>Nuova Seduta</h3>
    </header>
    <form @submit="add_session">
        <div class="flex-hor">
            <label for="date">Data:</label>
            <input required name="date" type="date" v-model="date">
        </div>
        <div class="flex-hor">
            <label for="time">Orario:</label>
            <input required type="time" name="time" step="600" v-model="time">
        </div>
        <textarea required placeholder="Descrizione..." v-model="description"></textarea>
        <div style="display: flex; gap: .5rem;">
            <button @click="reset()">Annulla</button>
            <input type="submit" value="Conferma">
        </div>
    </form>
</section>

</template>


<style>
.flex-hor {
    display: flex;
    align-items: center;
    gap: 1rem;
}
</style>