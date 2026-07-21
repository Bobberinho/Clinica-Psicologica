<script setup>
import { api_get, hash } from './util.js'
import router from './router/index.js'

let email = ""
let password = ""

async function login_form(event) {
    event.preventDefault()
    const params = new URLSearchParams()
    params.append("email", email)
    params.append("password", await hash(password))
    api_get(`/utente`, params)
    router.push(`/cerca`) // TODO
}
</script>

<template>
<form id="login" @submit="login_form">
    <h3 class="form-title">Login</h3>
    <input type="text" v-model="email" name="email" id="login-elmail" placeholder="Email">
    <input type="password" v-model="password" name="password" id="login-password" placeholder="Password">
    <input type="submit" value="Accedi">
</form>
</template>

<style>

</style>