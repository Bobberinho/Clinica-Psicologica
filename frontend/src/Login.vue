<script setup>
import { login } from './endpoint.js'

let username = ""
let password = ""

function login_form() {
    login(username, password)
}
</script>

<template>
<form id="login" v-on:submit="login_form()">
    <h3 class="form-title">Login</h3>
    <input type="text" v-model="username" name="username" id="login-username" placeholder="Username">
    <input type="password" v-model="password" name="password" id="login-password" placeholder="Password">
    <input type="submit" value="Accedi">
</form>
</template>

<style>

</style>