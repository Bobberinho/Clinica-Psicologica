<script setup>
import Close from '@/icons/Close.vue';
import { api_get, sort } from '@/util';
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import AddButton from './building_components/AddButton.vue';

const route = useRoute()

const form_open = ref(false)
const farmaci_db = ref([])
farmaci_db.value = sort(await api_get("/farmaci"), "Nome")
const farmaci_db_filtered = computed(() => farmaci_db.value.filter((f) => f["Nome"].match(new RegExp(nome_farmaco.value, "i"))))

const emit = defineEmits(["submit"])


const farmaci = ref([])
const nome_farmaco = ref("")
const nome_farmaco_error = computed(() => nome_farmaco.value != "" && farmaci_db.value.find(f => f["Nome"] == nome_farmaco.value) === undefined)
const posologia = ref("")
const durata = ref("")
function add_farmaco(event) {
    event.preventDefault()
    const farm = {
        ID_Prescrizione: -1,
        ID_Farmaco: farmaci_db.value.find(f => f["Nome"] == nome_farmaco.value)["ID"],
        Nome: nome_farmaco.value,
        Posologia: posologia.value,
        Durata: durata.value
    }
    farmaci.value.push(farm)
    secondary_form_open.value = false
    nome_farmaco.value = ""
    posologia.value = ""
    durata.value = ""
    //console.log(farm)
}
function remove_farmaco(idx) {
    farmaci.value.splice(idx, 1)
}

const secondary_form_open = ref(false)
const note = ref("")
function add_prescrizione(event) {
    event.preventDefault()
    const date = new Date().toISOString().split('T', 1)[0]
    if (farmaci.value != []) {
        const prescrizione = {
            ID_Paziente: route.params.id,
            Note: note.value,
            Data: date,
            Lista_Dettagli: []
        }
        farmaci.value.forEach((f) => prescrizione["Lista_Dettagli"].push(f))
        console.log(prescrizione)
        api_get(`${route.path}/prescrizione`, "", "POST", prescrizione)
    }
    form_open.value = false
    emit("submit")
    // TODO: errore se non c'è almeno un farmaco aggiunto
}
function reset() {
    farmaci.value = []
    note.value = ""
    nome_farmaco.value = ""
    posologia.value = ""
    durata.value = ""
    form_open.value = false
}
</script>

<template>
<AddButton v-if="!form_open" @click="form_open = true" text="Aggiungi una prescrizione"></AddButton>

<section class="form-container" v-if="form_open">
    <header>
        <h3>Nuova Prescrizione</h3>
    </header>
    <li class="list compact">
        <ul class="list-item no-bg" v-for="(farmaco, idx) in farmaci">
            <div class="list-action">
                <Close @click="remove_farmaco(idx)"></Close>
            </div>
            <div class="list-item-title">
                <svg class="list-item-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M9 14H15M12 11V17M8 7V9L6.21115 12.5777C6.07229 12.8554 6 13.1616 6 13.4721V19C6 20.1046 6.89543 21 8 21H16C17.1046 21 18 20.1046 18 19V13.4721C18 13.1616 17.9277 12.8554 17.7889 12.5777L16 9V7M8 7H16M8 7C7.44772 7 7 6.55228 7 6V5C7 4.44772 7.44772 4 8 4H16C16.5523 4 17 4.44772 17 5V6C17 6.55228 16.5523 7 16 7" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
                {{ farmaco["Nome"] }}
            </div>
            <div class=""><strong>Dosaggio: </strong>{{ farmaco["Posologia"] }}</div>
            <div class=""><strong>Durata del trattamento: </strong>{{ farmaco["Durata"] }}</div>
        </ul>
        <AddButton v-if="!secondary_form_open" @click="secondary_form_open = true" class="simple" text="Aggiungi un farmaco"></AddButton>
    </li>
    <form v-if="secondary_form_open" class="form-secondary" @submit="add_farmaco">
        <div class="dropdown-search">
            <input required type="text" :class="nome_farmaco_error ? 'error' : ''" v-model="nome_farmaco" placeholder="Farmaco...">
            <div class="options">
                <div class="option" @mousedown="nome_farmaco = farmaco['Nome']" v-for="farmaco in farmaci_db_filtered" :key="farmaco['ID']">{{ farmaco["Nome"] }}</div>
            </div>
        </div>
        <input required type="text" v-model="posologia" placeholder="Posologia...">
        <input required type="text" v-model="durata" placeholder="Durata del trattamento...">
        <input type="submit" value="Aggiungi Farmaco">
    </form>

    <form @submit="add_prescrizione">
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