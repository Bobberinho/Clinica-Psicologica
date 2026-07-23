<script setup>
const props = defineProps([
    "title",
    "value"
])
</script>

<template>
<li class="statistics-item">
    <div class="title">{{ title }}</div>
    <div class="value">{{ value }}</div>
</li>
</template>

<style scoped>
.statistics-item {
    padding: 1rem;
    list-style-type: none;
    display: flex;
    justify-content: space-between;
    font-size: 1.1rem;
}
.statistics-item.hover:hover {
    background-color: whitesmoke;
}
.value {
    font-weight: bold;
    color: darkslategray;
}
</style>