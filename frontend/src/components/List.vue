<script setup>
import { api_get } from '@/util';
import { ref } from 'vue';

const props = defineProps(['query'])
console.log(props.query)
const list = ref(await api_get(props.query))
console.log(list.value)
</script>

<template>

<li v-for="item in list">
    {{ item["Stato"] }} {{ item["Descrizione"] }}
</li>

</template>


<style scoped>

</style>