<script setup>
import { api_get } from '@/util';
import { ref } from 'vue';

const props = defineProps(['query', 'title'])

const list = ref([])
const error = ref(false)
const error_info = ref({})

const refresh = async () => {
    try {
        list.value = await api_get(props.query)
    } catch (err) {
        error.value = true
        error_info.value = err
    }
    console.log("REFRESHED LIST: ", list.value)
}
refresh()
defineExpose({
    refresh
})
</script>

<template>
<div v-if="!error" class="list fill-window">
    <li v-for="item in list" class="list-item">
        <slot name="item" v-bind="item"></slot> <!-- IMPORTANTE CHE name E v-bind SIANO UGUALI -->
    </li>
</div>
<div v-else class="error">{{ error_info }}</div>

</template>


<style>
.list {
    display: flex;
    margin-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    gap: .5rem;
    flex-direction: column;
    overflow-y: scroll;
}
.list-item {
    color: black;
    text-decoration: none;
    padding: .8rem;
    border: 2px solid darkgreen;
    border-radius: .5rem;
    background-color: white;
    cursor: pointer;
    flex-grow: 1;
	list-style-type: none;
	position: relative;
}
.list-item:hover {
    background: white;
}
.hover .list-item:hover {
    /* background-color: color-mix(in srgb, white 95%, black 5%); */
    box-shadow: 1px 1px 4px gray;
}

.list-item-title {
    font-size: 1.1rem;
    margin-bottom: .5rem;
    line-height: 1.3rem;
    display: flex;
    align-items: center;
    gap: .5rem;
    font-weight: bold;
}
.list-item-title.large {
    font-size: 1.3rem;
}
.grayed {
    color: gray;
}
.list-item-subtitle {
    color: gray;
    margin-top: .5rem;
    text-justify: distribute;
}

.list-item-info-wseparator {
    margin-top: .2rem;
    display: flex;
    gap: 1rem;
}
.list-item-info-wseparator span {
    position: relative;
}
.list-item-info-wseparator span ~ span::before {
    content: "";
    width: 8px;
    height: 8px;
    border-radius: 100%;
    background-color: lightgray;
    position: absolute;
    top: calc(50% - 4px);
    left: calc(-0.5rem - 4px);
}

.list-item-title :deep(svg) {
    width: 2rem;
    height: 2rem;
}
.list-item-title :deep(svg) path {
    stroke: darkgreen;
}

.info-btn {
    position: absolute;
    top: .5rem;
    right: .5rem;
    background: none;
    border: none;
    padding: .5rem;
    border-radius: 50%;
    aspect-ratio: 1;
}
.info-btn:hover {
    background: rgba(0, 0, 0, 0.05);
}
.info-btn path {
    stroke: gray;
    fill: gray;
}
.info-btn svg {
    margin: none;
    padding: none;
    width: 1rem;
    height: 1rem;
}
</style>