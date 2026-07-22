<script setup>
import { api_login, hash } from './util.js'
import router from './router/index.js'
import { useTemplateRef } from 'vue'

let email = ""
let password = ""
const emit = defineEmits(["login"])

async function login_form(event) {
    event.preventDefault()
    try {
        const res = await api_login(email, password)
        emit("login")
        router.push(`/profilo`)
    } catch (error) {
        email = ""
        password = ""
        document.getElementById("error").innerHTML = error
        document.getElementById('login_form').reset()
    }
}
</script>

<template>
<form id="login_form" @submit="login_form">
    <h3 class="form-title">Login</h3>
    <div id="error" style="color: red;"></div>
    <input type="text" v-model="email" name="email" id="login-elmail" placeholder="Email">
    <input type="password" v-model="password" name="password" id="login-password" placeholder="Password">
    <input type="submit" value="Accedi">
</form>
</template>

<style>

</style>