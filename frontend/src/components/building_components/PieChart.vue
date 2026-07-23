<script setup>
import { ref, onMounted, useTemplateRef, computed } from 'vue'
import StatisticsEntry from './StatisticsEntry.vue';

const css_colors = ["DarkSlateGray", "MidnightBlue", "Teal", "ForestGreen", "DarkOliveGreen", "OliveDrab", "SaddleBrown", "Sienna", "Peru", "FireBrick", "Crimson", "Coral", "DarkOrange", "Goldenrod", "SandyBrown", "DarkOrchid", "MediumSlateBlue", "SlateGray", "CadetBlue", "RosyBrown"];
const props = defineProps(['pie_data'])
const computed_data = computed(function () {
    let rotation = 0
    let idx = 0
    const res = []
    props.pie_data.forEach((s) => {
        res.push({
            idx: idx,
            title: s.title,
            percentage: s.percentage,
            color: random_color(idx),
            rotation: rotation,
        })
        rotation += s.percentage
        idx++
    })
    return res
})


const slice_info_el = useTemplateRef('slice_info')
const show_info_el = ref(false)
const slice_info_title = ref("")
const slice_info_percent = ref(0)
const slice_info_percent_print = computed(() => pretty_percent(slice_info_percent.value))

onMounted(() => {
    let rotation = 0
    computed_data.value.forEach(slice => {
        const el = document.getElementById(slice.title)
        const mid_angle = slice.percentage / 2 + rotation
        const distance = 0.05
        const translate_x = get_x(mid_angle) * distance * 100
        const translate_y = get_y(mid_angle) * distance * 100
        // console.log(translate_x, translate_y)
        el.style.setProperty("--translate-x", translate_y + "%")
        el.style.setProperty("--translate-y", translate_x + "%")
        rotation += slice.percentage
    })
})

function get_x(percent) {
    return Math.sin(2 * Math.PI * percent)
}
function get_y(percent) {
    return Math.cos(2 * Math.PI * percent)
}
function draw_path(percentage, starting_percentage) {
    const move = `M ${get_y(starting_percentage)} ${get_x(starting_percentage)}`
    const arc = `A 1 1 0 ${percentage > .5 ? 1 : 0} 1 ${get_y(percentage + starting_percentage)} ${get_x(percentage + starting_percentage)}`
    const center = "L 0 0"
    // console.log("FROM: ", starting_percentage, "PATH: ", move, arc, center)
    return `${move} ${arc} ${center}`
}
function random_color(idx) {
    if (idx < css_colors.length) return css_colors[idx]
    else return css_colors[idx % css_colors.length]
}
function pretty_percent(percent) {
    return Math.round(percent * 100) / 100 + "%"
}
function hover_in(item) {
    show_info_el.value = true

    const el = document.getElementById(item.title)
    el.classList.add("hover")
    slice_info_percent.value = item.percentage
    slice_info_title.value = item.title
    slice_info_el.value.style.setProperty("--color", item.color)

    const path_box = el.getBoundingClientRect() // posizionamento assoluto della PATH
    const container_box = el.closest('.chart').getBoundingClientRect() // posizionamento assoluto del container

    const info_x = path_box.left + path_box.width / 2 - container_box.left
    const info_y = path_box.top + path_box.height / 2 - container_box.top

    slice_info_el.value.style.left = `${info_x}px`
    slice_info_el.value.style.top = `${info_y}px`
    slice_info_el.value.style.opacity = '1'
}
function hover_out(item) {
    document.getElementById(item.title).classList.remove("hover")
    show_info_el.value = false
}
</script>

<template>
<!-- 
<div class="pie-chart">
    <li v-for="slice in pie_data" :id="slice.title"></li>
</div> -->


<section class="chart-container">
    
    <section class="chart">
        <svg viewBox="-1 -1 2 2" style="transform: rotate(-90deg);">
            <!-- <circle r="1" fill="tomato"></circle> -->
            <path v-for="slice in computed_data" @mouseenter="hover_in(slice)" @mouseleave="hover_out(slice)" :id="slice.title" :fill="slice.color" :d="draw_path(slice.percentage, slice.rotation)"></path>
        </svg>
        <div ref="slice_info" class="hover-info" :class="show_info_el ? 'show' : ''">
            <div class="title">{{ slice_info_title }}</div>
            <div class="percentage">{{ slice_info_percent_print }}</div>
        </div>
    </section>
    <section class="scroll-list">
        <StatisticsEntry class="hover" v-for="item in computed_data" @mouseenter="hover_in(item)" @mouseleave="hover_out(item)" :title="item.title" :value="pretty_percent(item.percentage)"></StatisticsEntry>
    </section>
</section>


</template>


<style scoped>
.chart-container {
    /* display: flex; */
}
.scroll-list {
    max-height: 20rem;
    overflow: scroll;
}
.chart {
    margin: 2rem 20%;
    flex-grow: 1;
    overflow: visible;
    position: relative;
}
.hover-info {
    position: absolute;
    --x: 0;
    --y: 0;
    top: var(--y);
    left: var(--x);
    --color: red;
    color: var(--color);
    font-size: 1.2rem;
    /* display: flex; */
    display: none;
    flex-direction: column;
    align-items: center;
    background-color: contrast-color(var(--color));
    box-shadow: 1px 1px 4px var(--color);
    padding: .5rem;
    border-radius: .6rem;
}
.hover-info.show {
    display: flex;
}
.hover-info .title {

}
.hover-info .percentage {
    font-weight: bold;
}
svg {
    overflow: visible;
}
svg path {
    transform-box: fill-box;
    transform-origin: center;
    --translate-x: 0;
    --translate-y: 0;
    transition: .1s transform linear;
}
svg path.hover {
    transform: translate(var(--translate-x), var(--translate-y)) !important;
}
svg path title {
    
}
/* .pie-chart {
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
    --title: "Title";
    --radius: 6rem;
    --percentage: 0.35;
    --percentage-deg: calc(var(--percentage) * 360deg);
    --color: red;
    --rotation: 0.10;
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
} */
</style>