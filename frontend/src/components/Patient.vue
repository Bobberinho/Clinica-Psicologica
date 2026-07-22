<script setup>
import { useRoute } from 'vue-router';
import { inject, ref } from 'vue';
import { api_get } from '@/util';
import List from './List.vue';
const route = useRoute()
const id = route.params.id
const patient = ref(await api_get(`/paziente/${id}`))
const utente = inject("utente")
const is_psichiatra = false

</script>

<template>
<h1>{{ patient["Nome"] }} {{ patient["Cognome"] }}</h1>
<p>{{ patient["Codice_Fiscale"] }}</p>

<nav class="vertical">
    <a>Diagnosi</a>
    <a>Prescrizioni</a>
    <a>Sessioni</a>
    <a>Test</a>
</nav>

<List query="/paziente/4/prescrizioni" title="Prescrizioni">

</List>

</template>

<style scoped>
nav.vertical {
    flex-direction: column;
}
</style> 