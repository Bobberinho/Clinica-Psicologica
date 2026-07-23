<script setup>
const props = defineProps(["title"])
</script>

<template>
<section class="statistics-container">
    <h2 class="title">{{ title }}</h2>
    <slot></slot>
</section>
</template>

<style scoped>
.statistics-container {
    background-color: white;
    display: flex;
    flex-direction: column;
    padding: 2rem;
    border-radius: .8rem;
    box-shadow: 1px 1px 4px gray;
}
.title {
    margin: 0;
    text-align: center;
    color: darkslategray;
    border-bottom: 1px solid darkslategray;
}
</style>