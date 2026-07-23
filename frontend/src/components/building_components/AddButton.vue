<script setup>
const props = defineProps(['text'])
</script>
<template>
<button class="add-button">
    <svg height="200px" width="200px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 309.059 309.059" xml:space="preserve" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <g> <path style="fill:#010002;" d="M280.71,126.181h-97.822V28.338C182.889,12.711,170.172,0,154.529,0S126.17,12.711,126.17,28.338 v97.843H28.359C12.722,126.181,0,138.903,0,154.529c0,15.621,12.717,28.338,28.359,28.338h97.811v97.843 c0,15.632,12.711,28.348,28.359,28.348c15.643,0,28.359-12.717,28.359-28.348v-97.843h97.822 c15.632,0,28.348-12.717,28.348-28.338C309.059,138.903,296.342,126.181,280.71,126.181z"></path> </g> </g> </g></svg>
    <span>{{ text }}</span>
</button>
</template>


<style scoped>
.add-button {
    display: block;
    width: 100%;
    padding: 1rem;
    border: none;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    line-height: 1.2rem;
    gap: 1rem;
    border-radius: .8rem;
    box-shadow: 1px 1px 4px gray;
    transition: transform .1s linear;
}
.add-button.simple {
    box-shadow: none;
}
.add-button:hover {
    transform: scale(1.03);
}
.add-button.simple:hover {
    background: white;
    box-shadow: 1px 1px 4px gray;
    transform: none;
}
.add-button svg {
    width: 1rem;
    height: 1rem;
}
.add-button path {
    stroke: darkslategray !important;
    fill: darkslategray !important;
}
</style>