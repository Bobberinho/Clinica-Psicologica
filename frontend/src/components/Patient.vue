<script setup>
import { useRoute } from 'vue-router';
import { computed, inject, ref, useTemplateRef } from 'vue';
import { api_get } from '@/util';
import List from './List.vue';
import FormPrescrizioni from './FormPrescrizioni.vue';
import Calendar from '@/icons/Calendar.vue';
import Close from '@/icons/Close.vue';
import Stethoscope from '@/icons/Stethoscope.vue';
import PillBottle from '@/icons/PillBottle.vue';
import Notebook from '@/icons/Notebook.vue';
import FormDiagnosi from './FormDiagnosi.vue';
const route = useRoute()
const id = route.params.id
const patient = ref(await api_get(`/paziente/${id}`))
const utente = ref(inject("utente"))
const is_psichiatra = computed(() => utente.value["Is_Psichiatra"] == 1)

const active_tab = ref(0)


const prescriptions_list = ref(null)
const diagnosis_list = ref(null)

async function delete_prescription(id_p, id_f) {
    const params = new URLSearchParams()
    params.append("id_farmaco", id_f)
    await api_get(`/elimina_prescrizione/${id_p}`, params, "POST")
    prescriptions_list.value.refresh()
}
</script>

<template>
<section class="patient-info">
    <h1>{{ patient["Nome"] }} {{ patient["Cognome"] }}</h1>
    <div>{{ patient["Codice_Fiscale"] }}</div>
    <div>{{ patient["Residenza"] }}</div>
</section>

<nav class="nav-buttons">
    <a class="tab-button" @click="active_tab = 0" :class="active_tab == 0 ? 'active' : ''">
        <Stethoscope></Stethoscope>
        <span>Diagnosi</span>
    </a>
    <a class="tab-button" @click="active_tab = 1" :class="active_tab == 1 ? 'active' : ''">
        <PillBottle></PillBottle>
        <span>Prescrizioni</span>
    </a>
    <a class="tab-button" @click="active_tab = 2" :class="active_tab == 2 ? 'active' : ''">
        <Calendar></Calendar>
        <span>Sessioni</span>
    </a>
    <a class="tab-button" @click="active_tab = 3" :class="active_tab == 3 ? 'active' : ''">
        <Notebook></Notebook>
        <span>Test</span>
    </a>
</nav>

<div v-if="active_tab == 0" class="tab">
    <h2>Diagnosi</h2>
    <FormDiagnosi @submit="diagnosis_list.refresh()"></FormDiagnosi>
    <List ref="diagnosis_list" :query="route.path + '/diagnosi'" title="Diagnosi">
        <template #item="{ ID_Diagnosi, Nome_Disturbo, Stato_Diagnosi, Note_Diagnosi, Data_Diagnosi, Categoria_Disturbo, Descrizione_Disturbo, Nome_Specialista, Cognome_Specialista }">
            <div class="list-item-title">
                <Stethoscope></Stethoscope>
                {{ Nome_Disturbo }}
            </div>
            <div class=""><strong>Stato: </strong>{{ Stato_Diagnosi }}</div>
            <div class=""><strong>Note: </strong>{{ Note_Diagnosi }}</div>
            <div class="list-item-subtitle"><strong>Descrizione del disturbo: </strong>{{ Descrizione_Disturbo }}</div>
            
            <div class="list-info">
                <hr>
                <div class="list-item-info-wseparator grayed"><span><strong>Effettuata da: </strong><span>{{ Nome_Specialista }} {{ Cognome_Specialista }}</span></span><span><strong>Data: </strong><span>{{ Data_Diagnosi }}</span></span></div>
            </div>
        </template>
    </List>
</div>
<div v-if="active_tab == 1" class="tab">
    <h2>Prescrizioni</h2>
    <FormPrescrizioni v-if="is_psichiatra" @submit="prescriptions_list.refresh()"></FormPrescrizioni>
    <List ref="prescriptions_list" :query="route.path + '/prescrizioni'" title="Prescrizioni">
        <template #item="{ ID_Prescrizione, ID_Farmaco, Nome_Farmaco, Principio_Attivo, Dosaggio, Forma_Farmaceutica, Posologia, Durata, Note_Prescrizione, Nome_Psichiatra, Cognome_Psichiatra, Data }">
            <Close v-if="utente['Is_Psichiatra']" class="absolute" @click="delete_prescription(ID_Prescrizione, ID_Farmaco)"></Close>
            <div class="list-item-title">
                <PillBottle></PillBottle>
                {{ Nome_Farmaco }} <span class=grayed>({{ Principio_Attivo }} {{ Dosaggio }})</span></div>
            <div class=""><strong>Modalità di assunzione: </strong>{{ Forma_Farmaceutica }}</div>
            <div class=""><strong>Dosaggio: </strong>{{ Posologia }}</div>
            <div class=""><strong>Durata del trattamento: </strong>{{ Durata }}</div>
            <div class="list-item-subtitle"><strong>Note dello psichiatra: </strong>{{ Note_Prescrizione }}</div>
            
            <!-- <button class="info-btn" @click="toggle_info()"><svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 416.979 416.979" xml:space="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <path d="M356.004,61.156c-81.37-81.47-213.377-81.551-294.848-0.182c-81.47,81.371-81.552,213.379-0.181,294.85 c81.369,81.47,213.378,81.551,294.849,0.181C437.293,274.636,437.375,142.626,356.004,61.156z M237.6,340.786 c0,3.217-2.607,5.822-5.822,5.822h-46.576c-3.215,0-5.822-2.605-5.822-5.822V167.885c0-3.217,2.607-5.822,5.822-5.822h46.576 c3.215,0,5.822,2.604,5.822,5.822V340.786z M208.49,137.901c-18.618,0-33.766-15.146-33.766-33.765 c0-18.617,15.147-33.766,33.766-33.766c18.619,0,33.766,15.148,33.766,33.766C242.256,122.755,227.107,137.901,208.49,137.901z"></path> </g> </g></svg></button> -->
            <div class="list-info">
                <hr>
                <div class="list-item-info-wseparator grayed"><span><strong>Psichiatra: </strong><span>{{ Nome_Psichiatra }} {{ Cognome_Psichiatra }}</span></span><span><strong>Data di prescrizione: </strong><span>{{ Data }}</span></span></div>
            </div>
        </template>
    </List>
</div>
<div v-if="active_tab == 2" class="tab">
    <h2>Sessioni</h2>
    
</div>
<div v-if="active_tab == 3" class="tab">
    <h2>Test</h2>
    
</div>

</template>

<style scoped>
h2 {
    border-bottom: 1px solid darkgreen;
    color: darkslategrey;
    text-align: center;
    margin-top: 2rem;
}
.patient-info {
    margin-bottom: 2rem;
}
.icon:hover {
    background: none;
}
.tab-button {
    height: fit-content;
    border: 3px solid darkslategray;
    border-radius: .8rem;
    text-align: center;
    padding: .5rem 1rem;
    display: flex;
    font-weight: bold;
    color: darkslategray;
    flex-direction: column;
    align-items: center;
}
.tab-button :deep(path) {
    stroke: darkslategray;
    fill: darkslategray;
}
.tab-button.active {
    background-color: limegreen;
    border-color: darkgreen;
    color: white;
}
.tab-button.active:hover {
    background-color: color-mix(in srgb, limegreen 90%, black 10%);
}
.tab-button.active :deep(path) {
    fill: white;
    stroke: white;
}
.nav-buttons {
    background: none;
    display: flex;
    gap: 1rem;
    align-items: center;
    box-shadow: none;
}
.flex {
    display: flex;
}
</style> 