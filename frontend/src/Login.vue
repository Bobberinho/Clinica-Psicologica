<script setup>
import { api_login, hash } from './util.js'
import router from './router/index.js'
import { ref, useTemplateRef } from 'vue'

const email = ref("")
const password = ref("")
const emit = defineEmits(["login"])
const error_info = ref("")

async function login_form(event) {
    event.preventDefault()
    try {
        const res = await api_login(email.value, password.value)
        emit("login")
        router.push(`/profilo`)
    } catch (error) {
        email.value = ""
        error_info.value = error
    }
}
</script>

<template>
<form id="login_form" @submit="login_form">
    <h3 class="form-title">Login</h3>
    <div class="error">{{ error_info }}</div>
    <input required type="text" v-model="email" name="email" id="login-elmail" placeholder="Email">
    <input required type="password" v-model="password" name="password" id="login-password" placeholder="Password">
    <input type="submit" value="Accedi">
</form>
</template>

<style>

</style>