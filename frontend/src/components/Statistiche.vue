<script setup>
import { api_get } from '@/util';
import PieChart from './building_components/PieChart.vue';
import { computed, ref } from 'vue';
import StatisticsBox from './building_components/StatisticsBox.vue';
import StatisticsEntry from './building_components/StatisticsEntry.vue';

const diffusione_disturbi = ref(await api_get("/diffusione_disturbi"))
const pie_data = computed(() => diffusione_disturbi.value.map((d) => { return { title: d["Disturbo"], percentage: d["Percentuale_Pazienti"] } }))

const pazienti_con_prescrizioni = ref(await api_get("/elenco_pazienti_con_prescrizione"))
const numero_sedute_mese = ref((await api_get("/numero_sedute_mese")))
</script>


<template>
<h1>Statistiche</h1>
<section class="statistics-page">
    <StatisticsBox title="Statistiche Generali">
        <StatisticsEntry v-if="pazienti_con_prescrizioni" title="Numero di pazienti con prescrizioni:" :value="pazienti_con_prescrizioni.length"></StatisticsEntry>
        <StatisticsEntry v-if="numero_sedute_mese" title="Numero di sedute svolte nel mese attuale:" :value="numero_sedute_mese"></StatisticsEntry>
    </StatisticsBox>
    <StatisticsBox title="Diffusione dei disturbi">
        <PieChart :pie_data="pie_data"></PieChart>
    </StatisticsBox>
</section>
</template>

<style scoped>
.statistics-page {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
</style>