<script setup>
import { api_get } from '@/util';

const utente = await api_get("/profilo")
</script>


<template>
<h1>Profilo Specialista</h1>
{{ utente.Nome }} {{ utente.Cognome }}
{{ utente.Email }}
{{ utente.Numero_Telefono }}
</template>