<script setup>
import { api_get } from '@/util';
import { ref } from 'vue';
import Prescrizione from './Prescrizione.vue';

const props = defineProps(['query', 'title'])
console.log(props.query)
const list = ref([])
const error = ref(false)
const error_info = ref({})
try {
    list.value = await api_get(props.query)
} catch (err) {
    error.value = true
    error_info.value = err
}
console.log(list.value)
</script>

<template>
<div v-if="!error" class="list fill-window">
    <li v-for="item in list" :key="item['ID_Prescrizione']" class="list-item">
        <slot name="item" v-bind="item"></slot> <!-- IMPORTANTE CHE name E v-bind SIANO UGUALI -->
    </li>
</div>
<div v-else class="error">{{ error_info }}</div>

</template>


<style>
.list-item:hover {
    background: white;
}
.list-item-title {
    font-size: 1.3rem;
    margin-bottom: .5rem;
    line-height: 1.3rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}
.list-item-title svg {
    width: 2rem;
    height: 2rem;
}
.list-item-title svg path {
    stroke: darkgreen;
}

.grayed {
    color: gray;
}
.list-item-subtitle {
    margin-top: .5rem;
    text-justify: distribute;
}

.info-btn {
    position: absolute;
    top: .5rem;
    right: .5rem;
    background: none;
    border: none;
    padding: .5rem;
    border-radius: 50%;
    aspect-ratio: 1;
}
.info-btn:hover {
    background: rgba(0, 0, 0, 0.05);
}
.info-btn path {
    stroke: gray;
    fill: gray;
}
.info-btn svg {
    margin: none;
    padding: none;
    width: 1rem;
    height: 1rem;
}
</style>