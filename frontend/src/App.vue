<template>
    <header_vue />
    <section id="content">
        <catalogo_vue />
    </section>
</template>

<script setup>
    // Importa Header
    import header_vue from './components/shared/header.vue';
    // Importar pantalla de catalogo
    import catalogo_vue from './components/catalogo.vue';

</script>


<style scoped>
    #content {
        padding-top: 70px;
        padding-left: 160px;
        padding-right: 160px;
    }
</style>