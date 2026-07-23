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

const emit = defineEmits(["submit"])


const nome_disturbo = ref("")
const id_disturbo = computed(() => disturbi_db.value.find(d => d["Nome"] == nome_disturbo.value)["ID"])
const nome_farmaco_error = computed(() => nome_disturbo.value != "" && disturbi_db.value.find(f => f["Nome"] == nome_disturbo.value) === undefined)
const stato = ref("")
const note = ref("")

function add_diagnosis(event) {
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
    api_get(`${route.path}/diagnosi`, "", "POST", diagnosi)
    reset()

    emit("submit")
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
            <input type="submit" value="Conferma Prescrizione">
        </div>
    </form>
</section>

</template>

<style scoped>
.list.compact {
    padding: .5rem;
    background: whitesmoke;
}
.list.compact .list-item-title {
    font-size: 1.1rem;
}
.list.compact .list-item-icon {
    width: 1.5rem;
    height: 1.5rem;
}
.list.compact .list-item-icon path {
    stroke: black;
}
.list-item.no-bg {
    border: none;
    margin: 0;
}
.list-item.no-bg:hover {
    box-shadow: 1px 1px 4px gray;
}
.list-action {
    position: absolute;
    top: .5rem;
    right: .5rem;
}


.form-container {
    border: 2px solid darkgreen;
    background: white;
    border-radius: .8rem;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.form-container header {
    border-bottom: none;
    margin: 0;
    padding: 0;
    text-align: center;
    display: flex;
    justify-content: space-between;
}
h3 {
    margin: 0;
}
form {
    margin: 0;
    padding: 0;
}
.form-secondary {
    padding: 0;
}
.dropdown-search {
    position: relative;
}
.dropdown-search input {
    display: block;
    width: 100%;
    box-shadow: none;
}
.dropdown-search input.error {
    outline: 3px solid red !important;
    color: red;
}
.dropdown-search:has(> input:focus) {
    box-shadow: 3px 3px 4px darkolivegreen;
}
.dropdown-search input:focus {
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
}
.dropdown-search .options {
    flex-direction: column;
    background: white;
    max-height: 10rem;
    overflow: scroll;
    position: absolute;
    width: calc(100% + 6px);
    border: 3px solid palegreen;
    border-top: none;
    left: -3px;
    box-shadow: 1px 1px 4px darkolivegreen;
    border-bottom-left-radius: .8rem;
    border-bottom-right-radius: .8rem;
    display: none;
}
.dropdown-search input:focus ~ .options {
    display: flex;
}
.option {
    padding: .7rem 1rem;
}
.option:hover {
    background: rgba(0, 0, 0, 0.05);
}
</style>