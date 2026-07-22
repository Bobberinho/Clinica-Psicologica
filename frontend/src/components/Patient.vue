<script setup>
import { useRoute } from 'vue-router';
import { computed, inject, ref } from 'vue';
import { api_get } from '@/util';
import List from './List.vue';
import FormPrescrizioni from './FormPrescrizioni.vue';
import Prescrizione from './Prescrizione.vue';
const route = useRoute()
const id = route.params.id
const patient = ref(await api_get(`/paziente/${id}`))
const utente = ref(inject("utente"))
const is_psichiatra = computed(() => utente.value["Is_Psichiatra"] == 1)

const active_tab = ref(0)

</script>

<template>
<section class="patient-info">
    <h1>{{ patient["Nome"] }} {{ patient["Cognome"] }}</h1>
    <div>{{ patient["Codice_Fiscale"] }}</div>
    <div>{{ patient["Residenza"] }}</div>
</section>

<nav class="nav-buttons">
    <a class="tab-button" @click="active_tab = 0" :class="active_tab == 0 ? 'active' : ''">
        <span class="icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M3.00002 2.49988C2.44773 2.49988 2.00002 2.94759 2.00002 3.49987L2 8.99996C2 10.7412 2.61441 12.2563 3.71064 13.337C4.5831 14.1971 5.72091 14.7429 7 14.9287V15.75C7 19.2018 9.79822 22 13.25 22C16.7018 22 19.5 19.2018 19.5 15.75V15.0933C20.8056 14.6715 21.75 13.446 21.75 12C21.75 10.2051 20.2949 8.75 18.5 8.75C16.7051 8.75 15.25 10.2051 15.25 12C15.25 13.446 16.1944 14.6715 17.5 15.0933V15.75C17.5 18.0972 15.5972 20 13.25 20C10.9028 20 9 18.0972 9 15.75V14.9287C10.2791 14.7429 11.4169 14.1971 12.2894 13.337C13.3856 12.2563 14 10.7412 14 8.99997V3.49988C14 2.94759 13.5523 2.49988 13 2.49988H11.0023C10.45 2.49988 10.0023 2.94759 10.0023 3.49988C10.0023 4.05216 10.45 4.49988 11.0023 4.49988H12V8.99997C12 10.2587 11.5642 11.2435 10.8853 11.9128C10.2042 12.5842 9.21555 12.9999 8 12.9999C6.78445 12.9999 5.7958 12.5842 5.11473 11.9128C4.43584 11.2435 4 10.2587 4 8.99997L4.00001 4.49988H5.00002C5.5523 4.49988 6.00002 4.05216 6.00002 3.49988C6.00002 2.94759 5.5523 2.49988 5.00002 2.49988H3.00002ZM18.5 10.75C19.1904 10.75 19.75 11.3096 19.75 12C19.75 12.6904 19.1904 13.25 18.5 13.25C17.8096 13.25 17.25 12.6904 17.25 12C17.25 11.3096 17.8096 10.75 18.5 10.75Z" fill="#212121"></path> </g></svg>
        </span>
        <span>Diagnosi</span>
    </a>
    <a class="tab-button" @click="active_tab = 1" :class="active_tab == 1 ? 'active' : ''">
        <span class="icon">
            <svg fill="#000000" viewBox="0 0 32 32" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;" version="1.1" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:serif="http://www.serif.com/" xmlns:xlink="http://www.w3.org/1999/xlink"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M9.966,9.784l0.006,1.192c0.002,0.262 -0.102,0.514 -0.287,0.7c-0.185,0.186 -0.436,0.291 -0.699,0.291l-0.002,-0l0,-0c-0.796,-0 -1.559,0.316 -2.122,0.878c-0.564,0.563 -0.88,1.326 -0.88,2.122c-0,3.076 -0,8.936 -0,12.013c-0,0.796 0.316,1.559 0.88,2.122c0.563,0.562 1.326,0.878 2.122,0.878c3.464,-0 10.532,-0 13.995,-0c0.796,-0 1.56,-0.316 2.123,-0.878c0.563,-0.563 0.88,-1.326 0.88,-2.122c-0,-3.077 -0,-8.937 -0,-12.013c-0,-0.796 -0.317,-1.559 -0.88,-2.122c-0.563,-0.562 -1.327,-0.878 -2.123,-0.878l-0.001,-0c-0.55,-0 -0.997,-0.446 -0.998,-0.996l-0.002,-1.193c0.412,-0.148 0.792,-0.386 1.108,-0.702c0.562,-0.563 0.878,-1.326 0.878,-2.121l0,-1.974c0,-0.796 -0.316,-1.559 -0.878,-2.122c-0.563,-0.562 -1.326,-0.878 -2.122,-0.878l-10,-0c-0.795,-0 -1.558,0.316 -2.121,0.878c-0.563,0.563 -0.879,1.326 -0.879,2.122c0,0.635 0,1.338 0,1.974c0,0.795 0.316,1.558 0.879,2.121c0.32,0.32 0.704,0.56 1.123,0.708Zm13.012,4.183l0.001,-0c0.266,-0 0.521,0.105 0.709,0.293c0.188,0.188 0.294,0.442 0.294,0.707l-0,12.013c-0,0.265 -0.106,0.519 -0.294,0.706c-0.188,0.188 -0.443,0.294 -0.709,0.294l-13.995,-0c-0.266,-0 -0.521,-0.106 -0.709,-0.294c-0.188,-0.187 -0.293,-0.441 -0.293,-0.706l-0,-12.013c-0,-0.265 0.105,-0.519 0.293,-0.707c0.188,-0.188 0.443,-0.293 0.709,-0.293l0.002,-0c0.795,-0 1.557,-0.317 2.117,-0.88c0.56,-0.564 0.873,-1.327 0.869,-2.122l-0.005,-0.985c0,-0 8.011,-0 8.011,-0c-0,-0 0.002,0.995 0.002,0.995c0.003,1.653 1.345,2.992 2.998,2.992Zm-1.014,-8.986l0,1.974c0,0.265 -0.105,0.519 -0.293,0.707c-0.187,0.187 -0.441,0.293 -0.707,0.293c0,-0 -10,-0 -10,-0c-0.265,-0 -0.519,-0.106 -0.707,-0.293c-0.187,-0.188 -0.293,-0.442 -0.293,-0.707l0,-1.974c0,-0.266 0.106,-0.52 0.293,-0.707c0.188,-0.188 0.442,-0.293 0.707,-0.293c0,-0 10,-0 10,-0c0.266,-0 0.52,0.105 0.707,0.293c0.188,0.187 0.293,0.441 0.293,0.707Z"></path><path d="M14.982,17.98l-2.012,-0c-0.552,-0 -1,0.448 -1,1c0,0.552 0.448,1 1,1l2.012,-0l-0,2.011c-0,0.552 0.448,1 1,1c0.552,0 1,-0.448 1,-1l-0,-2.011l2.011,-0c0.552,-0 1,-0.448 1,-1c0,-0.552 -0.448,-1 -1,-1l-2.011,-0l-0,-2.012c-0,-0.552 -0.448,-1 -1,-1c-0.552,0 -1,0.448 -1,1l-0,2.012Z"></path></g></svg>
        </span>
        <span>Prescrizioni</span>
    </a>
    <a class="tab-button" @click="active_tab = 2" :class="active_tab == 2 ? 'active' : ''">
        <span class="icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M3 9H21M17 13.0014L7 13M10.3333 17.0005L7 17M7 3V5M17 3V5M6.2 21H17.8C18.9201 21 19.4802 21 19.908 20.782C20.2843 20.5903 20.5903 20.2843 20.782 19.908C21 19.4802 21 18.9201 21 17.8V8.2C21 7.07989 21 6.51984 20.782 6.09202C20.5903 5.71569 20.2843 5.40973 19.908 5.21799C19.4802 5 18.9201 5 17.8 5H6.2C5.0799 5 4.51984 5 4.09202 5.21799C3.71569 5.40973 3.40973 5.71569 3.21799 6.09202C3 6.51984 3 7.07989 3 8.2V17.8C3 18.9201 3 19.4802 3.21799 19.908C3.40973 20.2843 3.71569 20.5903 4.09202 20.782C4.51984 21 5.07989 21 6.2 21Z" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
        </span>
        <span>Sessioni</span>
    </a>
    <a class="tab-button" @click="active_tab = 3" :class="active_tab == 3 ? 'active' : ''">
        <span class="icon">
            <svg fill="#000000" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 490.899 490.899" xml:space="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <path d="M474.5,330.849l-104.3-104.3v-167.8c0-11.5-9.4-20.9-20.9-20.9h-73v-16.6c0-11.5-9.4-20.9-20.9-20.9H114.8 c-11.5,0-20.9,9.4-20.9,20.9v16.7h-73c-11.5,0-20.9,9.4-20.9,20.9v410.8c0,11.5,9.4,20.9,20.9,20.9h328.4 c11.5,0,20.9-9.4,20.9-20.9v-30.3c21.6,21.6,65.1,20.5,95.9-10.3C495.3,399.649,499.5,355.849,474.5,330.849z M135.6,41.049h99 v35.4h-99V41.049z M40.8,449.649v-370.1H94v16.7c0,11.5,9.4,20.9,20.9,20.9h140.6c10.4,0,19.8-9.4,20.9-19.8v-17.8h52.1v115.6 l-89.7-16.6c-7-3-25,3.1-22.9,22.9l17.7,95.9c0,4.2,2.1,7.3,5.2,10.4l89.7,89.7v52.1H40.8V449.649z M436.9,399.649 c-8.3,7.3-27.1,18.5-40.7,8.3l-124-124l-11.5-60.5l59.4,11.5l125.1,125.1C452.6,367.349,451.5,385.049,436.9,399.649z"></path> </g> </g></svg>
        </span>
        <span>Test</span>
    </a>
</nav>

<div v-if="active_tab == 0" class="tab">
    <h2>Diagnosi</h2>
    
</div>
<div v-if="active_tab == 1" class="tab">
    <h2>Prescrizioni</h2>
    <FormPrescrizioni v-if="is_psichiatra"></FormPrescrizioni>
    <List :query="route.path + '/prescrizioni'" title="Prescrizioni">
        <template #item="{ Nome_Farmaco, Principio_Attivo, Dosaggio, Forma_Farmaceutica, Posologia, Durata, Note_Prescrizione, Nome_Psichiatra, Cognome_Psichiatra, Data }">
            <div class="list-item-title">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M9 14H15M12 11V17M8 7V9L6.21115 12.5777C6.07229 12.8554 6 13.1616 6 13.4721V19C6 20.1046 6.89543 21 8 21H16C17.1046 21 18 20.1046 18 19V13.4721C18 13.1616 17.9277 12.8554 17.7889 12.5777L16 9V7M8 7H16M8 7C7.44772 7 7 6.55228 7 6V5C7 4.44772 7.44772 4 8 4H16C16.5523 4 17 4.44772 17 5V6C17 6.55228 16.5523 7 16 7" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
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
.tab-button path {
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
.tab-button.active path {
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