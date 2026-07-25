<script setup>
import Close from '@/icons/Close.vue';
import { api_get, sort } from '@/util';
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import AddButton from './building_components/AddButton.vue';

const route = useRoute()

const form_open = ref(false)
const disturbi_db = ref([])
disturbi_db.value = sort(await api_get("/disturbi"), "Nome")
const disturbi_db_filtered = computed(() => disturbi_db.value.filter((f) => f["Nome"].match(new RegExp(nome_disturbo.value, "i"))))

const emit = defineEmits(["after_submit"])


const nome_disturbo = ref("")
const id_disturbo = computed(() => disturbi_db.value.find(d => d["Nome"] == nome_disturbo.value)["ID"])
const nome_farmaco_error = computed(() => nome_disturbo.value != "" && disturbi_db.value.find(f => f["Nome"] == nome_disturbo.value) === undefined)
const stato = ref("")
const note = ref("")

async function add_diagnosis(event) {
    event.preventDefault()
    const date = new Date().toISOString().split('T', 1)[0]
    const diagnosi = {
        ID_Paziente: route.params.id,
        ID_Specialista: -1,
        ID_Disturbo: id_disturbo.value,
        Descrizione: note.value,
        Data: date,
        Stato: stato.value,
    }
    console.log(diagnosi)
    await api_get(`${route.path}/diagnosi`, "", "POST", diagnosi)
    reset()

    emit("after_submit")
}
function reset() {
    note.value = ""
    nome_disturbo.value = ""
    stato.value = ""
    form_open.value = false
}
</script>

<template>
<AddButton v-if="!form_open" @click="form_open = true" text="Aggiungi una diagnosi"></AddButton>

<section class="form-container" v-if="form_open">
    <header>
        <h3>Nuova Diagnosi</h3>
    </header>
    <form @submit="add_diagnosis">
        <div class="dropdown-search">
            <input required type="text" :class="nome_farmaco_error ? 'error' : ''" v-model="nome_disturbo" placeholder="Disturbo...">
            <div class="options">
                <div class="option" @mousedown="nome_disturbo = disturbo['Nome']" v-for="disturbo in disturbi_db_filtered" :key="disturbo['ID']">{{ disturbo["Nome"] }}</div>
            </div>
        </div>
        <select required v-model="stato">
            <option value="" disabled>--Stato--</option>
            <option value="Stabile">Stabile</option>
            <option value="Grave">Grave</option>
            <option value="Critico">Critico</option>
        </select>
        <textarea placeholder="Note..." v-model="note"></textarea>
        <div style="display: flex; gap: .5rem;">
            <button @click="reset()">Annulla</button>
            <input type="submit" value="Conferma">
        </div>
    </form>
</section>

</template>