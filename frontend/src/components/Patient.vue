<script setup>
import { useRoute } from 'vue-router';
import { ref } from 'vue';
import { fetch_path } from '@/util';
const route = useRoute()
const id = route.params.id
const patient = ref(await fetch_path(`/patient/${id}`))
console.log(patient)

// query per ottenere i dati del paziente
// const patient = { Nome: "Sara", Cognome: "Cappelli", CF: "CPPSRA05T62C573F", Data_Nascita: "22/12/2005", Indirizzo: "Via Redichiaro 2020, Cesena (FC)" }
</script>

<template>
<h1>{{ patient["NOME"] }} {{ patient["COGNOME"] }}</h1>
<p>{{ patient["CODICE_FISCALE"] }}</p>

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