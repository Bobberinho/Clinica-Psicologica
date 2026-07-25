<script setup>
import Close from '@/icons/Close.vue';
import { api_get, sort } from '@/util';
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import AddButton from './building_components/AddButton.vue';

const route = useRoute()

const form_open = ref(false)
const test_db = ref([])
test_db.value = sort(await api_get("/test"), "Nome")
const test_db_filtered = computed(() => test_db.value.filter((t) => t["Nome"].match(new RegExp(nome_test.value, "i"))))

const emit = defineEmits(["after_submit"])


const nome_test = ref("")
const id_test = computed(() => test_db.value.find(t => t["Nome"] == nome_test.value)["ID"])
const nome_test_error = computed(() => nome_test.value != "" && test_db.value.find(f => f["Nome"] == nome_test.value) === undefined)
const note = ref("")
const default_date = (new Date()).toISOString().split('T')[0]
const date = ref(default_date)
const risultato = ref("")

async function add_test(event) {
    event.preventDefault()
    const test = {
        ID_Paziente: route.params.id,
        ID_Psicoterapeuta: -1,
        ID_Test: id_test.value,
        Note: note.value,
        Data_Esecuzione: date.value,
        Risultato: risultato.value,
    }
    console.log(test)
    await api_get(`${route.path}/test`, "", "POST", test)
    reset()

    emit("after_submit")
}
function reset() {
    note.value = ""
    nome_test.value = ""
    risultato.value = ""
    date.value = default_date
    form_open.value = false
}
</script>

<template>
<AddButton v-if="!form_open" @click="form_open = true" text="Registra il risultato di un test"></AddButton>

<section class="form-container" v-if="form_open">
    <header>
        <h3>Nuovo Test</h3>
    </header>
    <form @submit="add_test">
        <div class="dropdown-search">
            <input required type="text" :class="nome_test_error ? 'error' : ''" v-model="nome_test" placeholder="Test...">
            <div class="options">
                <div class="option" @mousedown="nome_test = test['Nome']" v-for="test in test_db_filtered" :key="test['ID']">{{ test["Nome"] }}</div>
            </div>
        </div>
        <div class="flex-hor">
            <label for="date">Data di esecuzione del test:</label>
            <input required type="date" name="date" v-model="date">
        </div>
        <input required type="text" v-model="risultato" placeholder="Risultato...">
        <textarea placeholder="Note..." v-model="note"></textarea>
        <div style="display: flex; gap: .5rem;">
            <button @click="reset()">Annulla</button>
            <input type="submit" value="Conferma">
        </div>
    </form>
</section>

</template>