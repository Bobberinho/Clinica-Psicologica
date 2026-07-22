<script setup>
import { api_get, sort } from '@/util'
import { onMounted, ref } from 'vue'

let case_sensitive = false
let search_text = ""
const patients = sort(await api_get("/pazienti"), "Cognome")
// const patients = [
//     { Nome: "Diego", Cognome: "Bernabini", CF: "BRNDGI05S10H294J", Data_Nascita: "10/11/2005", Indirizzo: "Piazza Cavalcaconte 1, Sant'Agata Feltria (RN)" }
//     { Nome: "Sara", Cognome: "Cappelli", CF: "CPPSRA05T62C573F", Data_Nascita: "22/12/2005", Indirizzo: "Via Redichiaro 2020, Cesena (FC)" },
// ]
const patients_filtered = ref(patients.filter((p) => true))
const count = ref(patients.length)

function search(event) {
    event.preventDefault()
    let flag = case_sensitive ? "" : "i"
    let re = new RegExp(search_text, flag)
    patients_filtered.value = patients.filter((p) => p["Nome"].match(re) || p["Cognome"].match(re) || p["Codice_Fiscale"].match(re))
    count.value = patients_filtered.value.length
}
function toggle_case_sensitive() {
    case_sensitive = !case_sensitive
    document.getElementById("case-sensitive-btn").classList.toggle('active')
}
onMounted(() => {
    resize_fills()
})
window.addEventListener("resize", resize_fills)
function resize_fills() {
    // console.log("resized", window.innerHeight)
    Array.prototype.forEach.call(document.getElementsByClassName("fill-window"), element => {
        let y = element.getBoundingClientRect().top
        const style = window.getComputedStyle(element)
        let mg = parseInt(style.marginTop.replace("px", "")) + parseInt(style.marginBottom.replace("px", ""))
        element.style.maxHeight = `${window.innerHeight - y - mg}px`
    });
}
</script>

<template>
<form @submit="search">
    <input type="text" name="search" placeholder="Cerca un paziente..." v-model="search_text" autocomplete="false">
    <a class="icon-btn" id="case-sensitive-btn" @click="toggle_case_sensitive">
        <svg xmlns="http://www.w3.org/2000/svg" width="800px" height="800px" viewBox="0 0 16 16" fill="#000000"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.495 9.052l.891 2.35h1.091L6.237 3h-1.02L2 11.402h1.095l.838-2.35h3.562zM5.811 4.453l.044.135 1.318 3.574H4.255l1.307-3.574.044-.135.038-.156.032-.152.021-.126h.023l.024.126.029.152.038.156zm7.984 6.011v.936h.96V7.498c0-.719-.18-1.272-.539-1.661-.359-.389-.889-.583-1.588-.583-.199 0-.401.019-.606.056a4.875 4.875 0 0 0-1.078.326 2.081 2.081 0 0 0-.343.188v.984c.266-.23.566-.411.904-.54a2.927 2.927 0 0 1 1.052-.193c.188 0 .358.028.513.085a.98.98 0 0 1 .396.267c.109.121.193.279.252.472.059.193.088.427.088.7l-1.811.252c-.344.047-.64.126-.888.237a1.947 1.947 0 0 0-.615.419 1.6 1.6 0 0 0-.36.58 2.134 2.134 0 0 0-.117.721c0 .246.042.475.124.688.082.213.203.397.363.551.16.154.36.276.598.366.238.09.513.135.826.135.402 0 .76-.092 1.075-.278.315-.186.572-.454.771-.806h.023zm-2.128-1.743c.176-.064.401-.114.674-.149l1.465-.205v.609c0 .246-.041.475-.123.688a1.727 1.727 0 0 1-.343.557 1.573 1.573 0 0 1-.524.372 1.63 1.63 0 0 1-.668.135c-.187 0-.353-.025-.495-.076a1.03 1.03 0 0 1-.357-.211.896.896 0 0 1-.22-.316A1.005 1.005 0 0 1 11 9.732a1.6 1.6 0 0 1 .055-.44.739.739 0 0 1 .202-.334 1.16 1.16 0 0 1 .41-.237z"/></svg>
    </a>
    <input type="submit" value="Cerca">
</form>

<div style="position: sticky;">{{ count }} {{ count != 1 ? "risultati." : "risultato." }}</div>

<section class="list fill-window">
    <a :href="'/paziente/' + patient.ID" class="list-item" v-for="patient in patients_filtered" :key="patient.ID">
        <div class="list-item-title">{{ patient["Nome"] }} {{ patient["Cognome"] }}</div>
        <div class="list-item-subtitle">{{ patient["Codice_Fiscale"] }}</div>
        <div class="list-item-info-wseparator">
            <span>{{ patient["Data_Nascita"] }}</span>
            <span>{{ patient["Residenza"] }}</span>
        </div>
    </a>
</section>

</template>

<style scoped>
form {
    display: flex;
    flex-direction: row;
    position: sticky;
}
form input[type="text"] {
    flex-grow: 1;
}
.icon-btn {
    background-color: white;
    border-radius: .8rem;
    border: 2px solid transparent;
    box-shadow: 1px 1px 2px gray;
    display: flex;
    align-items: center;
    padding-left: .5rem;
    padding-right: .5rem;
}
.icon-btn.active {
    border: 2px solid gray;
    background-color: gainsboro;
    box-shadow: none;
}
.icon-btn.active:hover {
    background-color: color-mix(in srgb, gainsboro 95%, black 5%);
}
.icon-btn:hover {
    background-color: whitesmoke;
}
.icon-btn svg {
    width: 2rem;
    height: 2rem;
}
.list {
    display: flex;
    margin-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    gap: .5rem;
    flex-direction: column;
    overflow-y: scroll;
}
.list-item {
    color: black;
    text-decoration: none;
    padding: .8rem;
    border: 2px solid darkgreen;
    border-radius: .5rem;
    background-color: white;
    cursor: pointer;
    flex-grow: 1;
}
.list-item:hover {
    background-color: color-mix(in srgb, white 95%, black 5%);
}
.list-item-title {
    font-weight: bold;
}
.list-item-subtitle {
    color: gray;
}
.list-item-info-wseparator {
    margin-top: .2rem;
    display: flex;
    gap: 1rem;
}
.list-item-info-wseparator span {
    position: relative;
}
.list-item-info-wseparator span ~ span::before {
    content: "";
    width: 8px;
    height: 8px;
    border-radius: 100%;
    background-color: lightgray;
    position: absolute;
    top: calc(50% - 4px);
    left: calc(-0.5rem - 4px);
}
</style>
