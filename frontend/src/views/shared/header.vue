<template>
    <div class="encabezado d-flex align-items-center fixed-top">
        <alerts_success/>
        <img id="logoMarca" src="../../assets/img/logo1_sinFondo.png" alt="" class="img-fluid me-3"></img>
        <nav class="navbar navbar-expand-lg flex-grow-1">
            <div class="container-fluid">
                <h3 id="titleNavbar">BlackButton</h3>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <a class="nav-link" aria-current="page" @click="cambiarTipo(0)"
                                :class="[cartStore.tipoEntrega['cambioTipo'] == 0 ? 'hoverLink' : '']">Todos</a>
                        </li>
                        <li class="nav-item ps-1">
                            <a class="nav-link" aria-current="page" @click="cambiarTipo(1)"
                                :class="[cartStore.tipoEntrega['cambioTipo'] == 1 ? 'hoverLink' : '']">Entrega inmediata</a>
                        </li>
                        <li class="nav-item ps-1">
                            <a class="nav-link" aria-current="page" @click="cambiarTipo(2)"
                                :class="[cartStore.tipoEntrega['cambioTipo'] == 2 ? 'hoverLink' : '']">Sobre pedido</a>
                        </li>
                        <li class="nav-item pe-4 ps-1">
                            <button type="button" class="nav-link btn position-relative" data-bs-toggle="offcanvas"
                                data-bs-target="#offcanvasRight" aria-controls="offcanvasRight" @click="loadedProducts">
                                <i class="bi bi-cart2"></i>
                                <span v-if="cartStore.totalItemsCount > 0"
                                    class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                    {{ cartStore.totalItemsCount }}
                                <span class="visually-hidden">Productos en carrito</span>
                                </span>
                            </button>
                        </li>
                    </ul>
                    <form class="d-flex" role="search">
                        <div class="col-12">
                            <input class="form-control me-2" type="search" placeholder=""
                                name="search" v-model="v_search" id="searchAnimation">
                            <label>Buscar</label>
                        </div>
                    </form>
                </div>
            </div>
        </nav>
    </div>
    <offcanvas
        :productos="loader"
        @carga_lista="loadedProducts()"/>
</template>

<script setup>
    import { ref, watch } from 'vue';
    import { useCartStore } from '@/store/cartStore.js';
    import alerts_success from './alerts_success.vue';
    import offcanvas from './offcanvas.vue';
    const loader = ref([]);
    // Instancia del store
    const cartStore = useCartStore();
      // Función para cargar los productos en el carrito
    const loadedProducts = () => {
        loader.value = cartStore.loadedProducts;
    }
    // Cambio de tipo de producto
    const cambiarTipo = (nuevoTipo) => {
        const params = ref({ 'cambioTipo': nuevoTipo });
        cartStore.cambiarTipoEntrega(params);
    }
    // Sección: Busqueda
    const v_search = ref('');
    watch(v_search, (nuevoValor, viejoValor) => {
        if (cartStore.tipoEntrega.search == undefined || cartStore.tipoEntrega.search == '') {
            cartStore.cambiarTipoEntrega(ref({'cambioTipo': 0}));
        }
        cartStore.cambiarTipoEntrega(ref({'search': nuevoValor}));
    });

    // Escucha cuando cambia el valor para tipo de entrega, limpia campo search
    watch(() => cartStore.tipoEntrega, (nuevoValor, viejoValor) => {

        if (nuevoValor.cambioTipo != undefined) {
            v_search.value = '';
        }
    })

</script>

<style scoped>
    .encabezado {
        background-color: rgb(238, 247, 255);;
        padding: 10px 15px;
        box-shadow: 0 7px 15px rgb(181, 52, 113);
    }

    #logoMarca{
        padding-left: 1rem;
        height: 50px;
        transition: all 0.9s;
    }

    #logoMarca:hover {
        transform: scale3d(1.9, 1.9, 1.9);
        transition: all 0.9s;
    }

    .nav-link {
        cursor: pointer;
    }

    .navbar #titleNavbar {
        font-weight: bold;
        color: #6D214F;
    }

    .navbar .nav-item .nav-link.active {
        border-radius: 10px;
        box-shadow: 0 7px 10px rgb(181, 52, 113);
        transition: all 0.9s;
    }

    .navbar .nav-item .nav-link:hover {
        border-radius: 10px;
        box-shadow: 0 7px 5px rgb(181, 52, 113);
        transition: all 0.9s;
    }

    .hoverLink {
        border-radius: 10px;
        box-shadow: 0 7px 5px rgb(181, 52, 113);
        transition: all 0.9s;
    }

    #searchAnimation {
        border: 0;
        padding: 4px 0;
        border-bottom: 1px solid #ccc;
        background-color: transparent;
    }

    #searchAnimation ~ label {
        position: absolute;
        left: 0;
        width: 100%;
        top: 9px;
        color: #aaa;
        transition: 0.3s;
        z-index: -1;
        letter-spacing: 0.5px;
    }

    #searchAnimation:focus ~ label, .has-content#searchAnimation ~ label {
        top: -16px;
        font-size: 12px;
        color: #6D214F;
        transition: 0.3s;
    }

    .col-12 {
        float: left;
        position: relative;
    }

    input[type="text"] {
        color: #333;
        width: 100%;
        box-sizing: border-box;
        letter-spacing: 1px;
    }

    :focus {
        outline: none;
    }
</style>