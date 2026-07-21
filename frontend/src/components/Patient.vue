<script setup>
import { useRoute } from 'vue-router';
import { ref } from 'vue';
import { api_get } from '@/util';
const route = useRoute()
const id = route.params.id
const patient = ref(await api_get(`/paziente/${id}`))
console.log(patient)

// query per ottenere i dati del paziente
// const patient = { Nome: "Sara", Cognome: "Cappelli", CF: "CPPSRA05T62C573F", Data_Nascita: "22/12/2005", Indirizzo: "Via Redichiaro 2020, Cesena (FC)" }
</script>

<template>
<h1>{{ patient["Nome"] }} {{ patient["Cognome"] }}</h1>
<p>{{ patient["Codice_Fiscale"] }}</p>

<nav class="vertical">
    <a href="">Diagnosi</a>
    <a>Prescrizioni</a>
    <a>Sessioni</a>
    <a>Test</a>
</nav>

</template>

<style scoped>
nav.vertical {
    flex-direction: column;
}
</style> 