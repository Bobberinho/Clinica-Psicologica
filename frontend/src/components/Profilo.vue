<script setup>
import { computed, inject, ref } from 'vue';

const utente = ref(inject('utente'))
</script>


<template>
<h1>Profilo Specialista</h1>
{{ utente.Nome }} {{ utente.Cognome }}, {{ utente.ruolo }} ()
<p>{{ utente.Email }}</p>
<p>{{ utente.Numero_Telefono }}</p>
</template>