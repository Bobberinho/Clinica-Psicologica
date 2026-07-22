<script setup>
import { api_get, api_logout } from '@/util';
import { computed, inject, ref } from 'vue';

const utente = ref(inject("utente"))
const error = computed(() => utente.value["Nome"] === undefined)

console.log(error.value, utente.value["Nome"])
</script>


<template>

<button class="icon"><svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M8 7C9.65685 7 11 5.65685 11 4C11 2.34315 9.65685 1 8 1C6.34315 1 5 2.34315 5 4C5 5.65685 6.34315 7 8 7Z" fill="#000000"></path> <path d="M14 12C14 10.3431 12.6569 9 11 9H5C3.34315 9 2 10.3431 2 12V15H14V12Z" fill="#000000"></path> </g></svg>
    <div class="user-menu-container">
        <div v-if="!error" class="user-menu">
            <div class="grayed">Account</div>
            <div class="title">{{utente["Nome"]}} {{ utente["Cognome"] }}</div>
            <div>{{ utente["Email"] }}</div>
            <a @click="api_logout()" class="logout">Esci</a>
        </div>
        <div v-else class="user-menu">
            <div class="grayed">Account</div>
			<div>Stai navigando come ospite.</div>
            <a href="/login" class="login">Accedi</a>
        </div>
    </div>
</button>

</template>


<style scoped>
.icon {
	position: absolute;
	top: 1rem;
	right: 1rem;
}
.icon:hover .user-menu {
	display: flex;
}
.user-menu-container {
	position: absolute;
	top: 50%;
	right: 50%;
	padding: 1rem;
}
.user-menu {
	display: flex;
	position: relative;
	flex-direction: column;
	padding: 3.5rem 3rem 1.5rem;
	box-shadow: 0px 1px 4px darkslategray;
	font-weight: normal;
	background-color: white;
	border-radius: .8rem;
	border-top-right-radius: 0;
	display: none;
}
.user-menu .grayed {
	position: absolute;
	top: 1rem;
	left: 1rem;
	color: lightgray;
	letter-spacing: 1px;
	font-weight: bold;
	text-transform: uppercase;
}
.user-menu .title {
	font-weight: bold;
}
.user-menu a {
	margin-top: 1rem;
	padding: .5rem 2rem;
	border-radius: .6rem;
	line-height: 1rem;
	display: block;
	font-weight: bold;
	color: red;
	text-decoration: none;
}
.user-menu a:hover {
	background: rgba(255, 0, 0, 7%);
}
.user-menu a.login {
    color: royalblue;
}
.user-menu a.login:hover {
    background: rgba(0, 0, 255, 7%);
}
</style>