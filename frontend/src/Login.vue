<script setup>
import { fetch_path } from './requests.js'
import router from './router/index.js'

let username = ""
let password = ""

function login_form(event) {
    event.preventDefault()
    fetch_path(`/users/${username}`)
    router.push(`/user/${username}`)
}
</script>

<template>
<form id="login" @submit="login_form">
    <h3 class="form-title">Login</h3>
    <input type="text" v-model="username" name="username" id="login-username" placeholder="Username">
    <input type="password" v-model="password" name="password" id="login-password" placeholder="Password">
    <input type="submit" value="Accedi">
</form>
</template>

<style>

</style>