<script setup>
import { useRoute } from 'vue-router';
import UserWidget from './components/UserWidget.vue';
import { onMounted, provide, ref } from 'vue';
import { api_get } from './util.js';

const utente = ref({})
provide("utente", utente)
const route = useRoute()
get_profile()

async function get_profile() {
	console.log("logged in!")
	try {
		utente.value = await api_get("/profilo")
	} catch {
		utente.value = {}
	}
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
	<header class="site-header">
		<h1>PsicOk <span>clinica psicologica e psichiatrica</span></h1>
		<Suspense>
			<UserWidget></UserWidget>
		</Suspense>
	</header>
	<nav>
		<a href="/statistiche" :class="route.path == '/statistiche' ? 'active' : ''">Statistiche</a>
		<a href="/cerca" :class="route.path == '/cerca' ? 'active' : ''">Pazienti</a>
		<a href="/profilo" :class="route.path == '/profilo' ? 'active' : ''">Profilo</a>
	</nav>
	<main style="height: 100%;">
		<section style="grid-column: 2; height: 100%;">
			<Suspense><RouterView @login="get_profile"></RouterView></Suspense>
		</section>
	</main>
</template>

<style>
* {
	box-sizing: border-box;
	font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
#app {
	height: 100%;
}
body {
	background-color: whitesmoke;
	margin: 0;
}
main {
	display: grid;
	grid-template-rows: 1fr;
	grid-template-columns: 1fr 2fr 1fr;
}
.icon {
	border: none;
	border-radius: 50%;
	background: none;
	width: 2.5rem;
	height: 2.5rem;
	padding: .5rem;
	display: inline-block;
}
.icon:hover {
	background: rgba(0,0,0,0.05);
}
.site-header {
	padding: 2rem;
	background: white;
	border-bottom: 2px solid darkgreen;
}
.site-header h1 {
	color: limegreen;
	font-size: 3rem;
	line-height: 3rem;
	margin: 0;
}
.site-header span {
	color: darkgray;
	font-size: 2rem;
}
nav {
	display: flex;
	flex-direction: row;
	justify-content: center;
	background-color: rgb(189, 255, 189);
	box-shadow: 2px 2px 4px gray;
}
nav a {
	padding: 1rem 3rem;
	font-size: 1.2rem;
	cursor: pointer;
	color: black;
	text-decoration: none;
}
nav a:hover {
	background-color: rgba(0,0,0,0.05);
}
nav a.active {
	background-color: limegreen;
}
nav a.active:hover {
	background-color: color-mix(in srgb, limegreen 90%, darkgreen 10%);
}

form {
	padding: 1rem;
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
	margin-top: 2rem;
	margin-bottom: 2rem;
}
.form-title {
	font-size: 1.6rem;
	margin: 0;
	border-bottom: 1px solid black;
	text-align: center;
}
form input, textarea, select {
	padding: 0.8rem;
	border-radius: .5rem;
	font-size: 1rem;
	border: 2px solid darkslategray;
	flex-grow: 1;
}
form input:focus, textarea:focus, select:focus {
	outline: 3px solid palegreen;
}
form input[type=submit] {
	font-weight: bold;
	color: white;
	background-color: limegreen;
}
form input[type=submit]:hover {
	background-color: color-mix(in srgb, limegreen 90%, rgba(0,0,0,0.5) 10%);
}
button {
	border: 2px solid darkslategray;
	border-radius: .5rem;
	padding: .8rem;
	font-weight: bold;
	color: darkslategray;
	font-size: 1rem;
	display: block;
	flex-grow: 1;
}
button:hover {
	background-color: gainsboro;
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
	list-style-type: none;
	position: relative;
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




.error {
	color: red;
}
</style>
