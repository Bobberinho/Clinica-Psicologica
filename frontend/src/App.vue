<script setup>

</script>

<template>
	<header>
		<h1>PsicOk <span>clinica psicologica e psichiatrica</span></h1>
	</header>
	<nav>
		<a>Statistiche</a>
		<a>Ricerca</a>
		<a>Profilo</a>
	</nav>
	<main style="height: 100%;">
		<section style="grid-column: 2; height: 100%;">
			<Suspense><RouterView></RouterView></Suspense>
		</section>
	</main>
</template>

<style>
* {
	box-sizing: border-box;
	font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
#app {
	height: 100%;
}
body {
	background-color: whitesmoke;
	margin: 0;
}
main {
	display: grid;
	grid-template-rows: 1fr;
	grid-template-columns: 1fr 2fr 1fr;
}
header {
	padding: 2rem;
	background: white;
	border-bottom: 2px solid darkgreen;
}
header h1 {
	color: limegreen;
	font-size: 3rem;
	line-height: 3rem;
	margin: 0;
}
header span {
	color: darkgray;
	font-size: 2rem;
}
nav {
	display: flex;
	flex-direction: row;
	justify-content: center;
	background-color: limegreen;
}
nav a {
	padding: 1rem;
	font-size: 1.2rem;
	cursor: pointer;
}
nav a:hover {
	background-color: rgba(0,0,0,0.1);
}

form {
	padding: 1rem;
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
	margin-top: 2rem;
	margin-bottom: 2rem;
}
.form-title {
	font-size: 1.6rem;
	margin: 0;
	border-bottom: 1px solid black;
	text-align: center;
}
form input {
	padding: 0.8rem;
	border-radius: .5rem;
	font-size: 1rem;
	border: 2px solid darkslategray;
}
form input:focus {
	outline: 3px solid palegreen;
}
form input[type=submit] {
	font-weight: bold;
	color: white;
	background-color: limegreen;
}
form input[type=submit]:hover {
	background-color: color-mix(in srgb, limegreen 90%, rgba(0,0,0,0.5) 10%);
}
</style>
