<script setup>
import { api_get, api_logout } from '@/util';
import { ref } from 'vue';

const utente = ref({})
const error = ref(false)
await getUser()

window.addEventListener('popstate', getUser);

async function getUser() {
    console.log("tried")
    try {
        utente.value = await api_get('/profilo')
    } catch {
        error.value = true
    }
}
</script>


<template>

<button class="account-icon"><svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M8 7C9.65685 7 11 5.65685 11 4C11 2.34315 9.65685 1 8 1C6.34315 1 5 2.34315 5 4C5 5.65685 6.34315 7 8 7Z" fill="#000000"></path> <path d="M14 12C14 10.3431 12.6569 9 11 9H5C3.34315 9 2 10.3431 2 12V15H14V12Z" fill="#000000"></path> </g></svg>
    <div class="user-menu-container">
        <div v-if="!error" class="user-menu">
            <div class="grayed">Account</div>
            <div class="title">{{utente["Nome"]}} {{ utente["Cognome"] }}</div>
            <div>{{ utente["Email"] }}</div>
            <a @click="api_logout()" class="logout">Esci</a>
        </div>
        <div v-else class="user-menu">
            <div class="grayed">Account</div>
            <a href="/login" class="login">Accedi</a>
        </div>
    </div>
</button>

</template>


<style scoped>
.account-icon {
	border: none;
	border-radius: 50%;
	background: none;
	position: absolute;
	top: 1rem;
	right: 1rem;
	width: 2.5rem;
	height: 2.5rem;
	padding: .5rem;
}
.account-icon:hover {
	background: whitesmoke;
}
.account-icon:hover .user-menu {
	display: flex;
}
.user-menu-container {
	position: absolute;
	top: 50%;
	right: 50%;
	padding: 1rem;
}
.user-menu {
	position: relative;
	flex-direction: column;
	gap: .5rem;
	padding: 3rem 2rem 1rem;
	box-shadow: 1px 1px 4px darkgray;
	background-color: white;
	border: 2px solid gray;
	border-radius: .8rem;
	border-top-right-radius: 0;
	display: none;
}
.user-menu .grayed {
	position: absolute;
	top: .5rem;
	left: .5rem;
	color: lightgray;
	letter-spacing: 1px;
	font-weight: bold;
	text-transform: uppercase;
}
.user-menu .title {
	font-weight: bold;
}
.user-menu a {
	background: rgba(255, 0, 0, 7%);
	padding: .5rem 2rem;
	border-radius: .6rem;
	line-height: 1rem;
	display: block;
	font-weight: bold;
	color: red;
	border: 2px solid red;
}
.user-menu a:hover {
	background: rgba(255, 0, 0, 10%);
}
.user-menu a.login {
    background: rgba(0, 0, 255, 7%);
    border: 2px solid royalblue;
    color: royalblue;
}
.user-menu a.login:hover {
    background: rgba(0, 0, 255, 10%);
}
</style>