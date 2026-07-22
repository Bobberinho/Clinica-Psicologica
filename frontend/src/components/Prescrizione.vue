<script setup>
import { ref } from 'vue';

const props = defineProps(["info"])
const show_info = ref(false)

function toggle_info() {
    show_info.value = !show_info.value
    console.log(show_info.value)
}
</script>



<template>
    <li v-if="info" class="list-item">
        <div class="list-item-title">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M9 14H15M12 11V17M8 7V9L6.21115 12.5777C6.07229 12.8554 6 13.1616 6 13.4721V19C6 20.1046 6.89543 21 8 21H16C17.1046 21 18 20.1046 18 19V13.4721C18 13.1616 17.9277 12.8554 17.7889 12.5777L16 9V7M8 7H16M8 7C7.44772 7 7 6.55228 7 6V5C7 4.44772 7.44772 4 8 4H16C16.5523 4 17 4.44772 17 5V6C17 6.55228 16.5523 7 16 7" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
            {{ info["Nome_Farmaco"] }} <span class=grayed>({{ info["Principio_Attivo"] }} {{ info["Dosaggio"] }})</span></div>
        <div class=""><strong>Modalità di assunzione: </strong>{{ info["Forma_Farmaceutica"] }}</div>
        <div class=""><strong>Dosaggio: </strong>{{ info["Posologia"] }}</div>
        <div class=""><strong>Durata del trattamento: </strong>{{ info["Durata"] }}</div>
        <div class="list-item-subtitle"><strong>Note dello psichiatra: </strong>{{ info["Note_Prescrizione"] }}</div>
        
        <button class="info-btn" @click="toggle_info()"><svg fill="#000000" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 416.979 416.979" xml:space="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <path d="M356.004,61.156c-81.37-81.47-213.377-81.551-294.848-0.182c-81.47,81.371-81.552,213.379-0.181,294.85 c81.369,81.47,213.378,81.551,294.849,0.181C437.293,274.636,437.375,142.626,356.004,61.156z M237.6,340.786 c0,3.217-2.607,5.822-5.822,5.822h-46.576c-3.215,0-5.822-2.605-5.822-5.822V167.885c0-3.217,2.607-5.822,5.822-5.822h46.576 c3.215,0,5.822,2.604,5.822,5.822V340.786z M208.49,137.901c-18.618,0-33.766-15.146-33.766-33.765 c0-18.617,15.147-33.766,33.766-33.766c18.619,0,33.766,15.148,33.766,33.766C242.256,122.755,227.107,137.901,208.49,137.901z"></path> </g> </g></svg></button>
        <div :class="show_info ? 'list-info show' : 'list-info'">
            <hr>
            <div class="list-item-info-wseparator grayed"><span><strong>Psichiatra: </strong><span>{{ info["Nome_Psichiatra"] }} {{ info["Cognome_Psichiatra"] }}</span></span><span><strong>Data di prescrizione: </strong><span>{{ info["Data"] }}</span></span></div>
        </div>
    </li>
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


.list-info {
    display: none;
}
.list-info.show {
    display: block;
}
</style>