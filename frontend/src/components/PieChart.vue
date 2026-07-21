<script setup>
import { ref, onMounted } from 'vue'

const pie_data = [
    { title: "Margherita", percentage: 0.35, color: "brown" },
    { title: "Americana", percentage: 0.30, color: "royalblue" },
    { title: "Salsiccia", percentage: 0.20, color: "orange" },
    { title: "Quattro Stagioni", percentage: 0.10, color: "green" },
    { title: "Diavola", percentage: 0.05, color: "gray" },
]

const css_colors = ["DarkSlateGray", "MidnightBlue", "Teal", "ForestGreen", "DarkOliveGreen", "OliveDrab", "SaddleBrown", "Sienna", "Peru", "FireBrick", "Crimson", "Coral", "DarkOrange", "Goldenrod", "SandyBrown", "DarkOrchid", "MediumSlateBlue", "SlateGray", "CadetBlue", "RosyBrown"];

onMounted(() => {
    let rotation = 0
    pie_data.forEach(slice => {
        const el = document.getElementById(slice.title)
        el.style.setProperty("--percentage", slice.percentage)
        el.style.setProperty("--color", css_colors[Math.floor(Math.random() * css_colors.length)])
        el.style.setProperty("--rotation", rotation)
        el.style.setProperty("--title", "\"" + slice.title + "\"")
        console.log(el.style.getPropertyValue("--title"))
        rotation += slice.percentage
    })
})
</script>

<template>

<div class="pie-chart">
    <li v-for="slice in pie_data" :id="slice.title"></li>
</div>

</template>


<style scoped>
.pie-chart {
    display: grid;
    place-items: center;
    margin: 4rem;
}
li {
    display: grid;
    place-items: center;
    grid-row: 1;
    grid-column: 1;
    list-style-type: none;
    --title: "Title"; /* SET VIA JS */
    --radius: 6rem;
    --percentage: 0.35; /* SET VIA JS */
    --percentage-deg: calc(var(--percentage) * 360deg);
    --color: red; /* SET VIA JS */
    --rotation: 0.10; /* SET VIA JS */
    --rotation-deg: calc(var(--rotation) * 360deg);
    width: calc(var(--radius) * 2);
    aspect-ratio: 1;
    border-radius: 50%;
    background: conic-gradient(from var(--rotation-deg), var(--color) 0, var(--color) var(--percentage-deg), transparent var(--percentage-deg));
}
li::after {
    content: var(--title);
    grid-row: 1;
    grid-column: 1;
    --angle: calc(calc(var(--percentage-deg) / 2) + var(--rotation-deg));
    --distance: calc(var(--radius) + 2.7rem);
    --x: calc(cos(calc(var(--angle) - 90deg)) * var(--distance));
    --y: calc(sin(calc(var(--angle) - 90deg)) * var(--distance));
    transform: translateX(var(--x)) translateY(var(--y));
}
</style>