<template>
    <header_vue v-if="!$route.meta.hideHeader" />

    <section :id="!$route.meta.hideHeader ? 'content' : 'panel-full'">
        <router-view />
    </section>
</template>

<script setup>
    import header_vue from './views/shared/header.vue';
    import { useRoute } from 'vue-router';
    import { useCartStore } from './store/cartStore';
    import { onMounted } from 'vue';
    import alertas from './assets/js/notifications';

    const cartStore = useCartStore();

    const route = useRoute(); // Esto nos permite acceder a la info de la URL actual

    onMounted(() => {
        cartStore.iniciarTemporizador();
        // if (cartStore.expiracion.time_expira) {
        //     const ahora = new Date();
        //     const expiracion = new Date(cartStore.expiracion.time_expira);
        //     if (ahora > expiracion) {
        //         // El tiempo pasó mientras la página estaba cerrada/recargando
        //         cartStore.$reset(); // Limpia el store
        //         localStorage.removeItem('miCarrito');
        //         alertas.alertWarning("Tu reserva de muñecos ha expirado", false);
        //     }
        // }
    });
</script>


<style scoped>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        margin: 0;
        padding: 0;
        background-color: #f4f4f4;
        text-align: center;
    }

    #content {
        padding-top: 70px;
        height: 100%;
    }

    #panel-full {
        padding: 0;
        margin: 0;
        width: 100%;
        min-height: 100vh;
    }


</style>