<template>
    <header_vue v-if="!$route.meta.hideHeader" />

    <section :id="!$route.meta.hideHeader ? 'content' : 'panel-full'">
        <router-view />
    </section>
</template>

<script setup>
    import header_vue from './views/shared/header.vue';
    import { useRoute } from 'vue-router';

    const route = useRoute(); // Esto nos permite acceder a la info de la URL actual
</script>


<style scoped>
    #content {
    padding-top: 70px;
    padding-left: 160px;
    padding-right: 160px;
    }

    #panel-full {
        padding: 0;
        margin: 0;
        width: 100%;
        min-height: 100vh;
    }
</style>