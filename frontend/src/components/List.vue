<script setup>
import { api_get } from '@/util';
import { ref } from 'vue';
import Prescrizione from './Prescrizione.vue';

const props = defineProps(['query', 'title'])
console.log(props.query)
const list = ref(await api_get(props.query))
console.log(list.value)
</script>

<template>
<h2>{{ title }}</h2>
<div class="list fill-window">
    <Prescrizione v-for="item in list" :info="item"></Prescrizione>
</div>

</template>


<style scoped>
h2 {
    border-bottom: 1px solid darkgreen;
    color: darkslategrey;
    text-align: center;
    margin-top: 2rem;
}
</style>