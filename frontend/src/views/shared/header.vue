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
                <div class="collapse navbar-collapse navbar-push" id="navbarSupportedContent">
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
                        <li class="nav-item pe-3">
                            <a href="https://www.facebook.com/share/1CS1VTt2wB/" target="_blank" class="d-flex">
                                <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" class="bi bi-facebook" viewBox="0 0 16 16">
                                    <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"/>
                                </svg>
                            </a>
                        </li>
                    </ul>
                    <form class="d-flex" id="form_search">
                        <!--input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"-->
                        <div class="form-floating me-2">
                            <input type="text" class="form-control" id="floatingInput" placeholder="" v-model="v_search">
                            <label for="floatingInput">Buscar...</label>
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
        // Envia señal para recarga en catalogo
        cartStore.recargaCatalogo();
    }
    // Cambio de tipo de producto
    const cambiarTipo = (nuevoTipo) => {
        const params = ref({ 'cambioTipo': nuevoTipo });
        cartStore.cambiarTipoEntrega(params);
    }
    // Sección: Busqueda
    const v_search = ref('');
    watch(v_search, (nuevoValor, viejoValor) => {
        if (cartStore.tipoEntrega.search == undefined || cartStore.tipoEntrega.search == '' || nuevoValor == '') {
            cartStore.cambiarTipoEntrega(ref({'cambioTipo': 0}));
        }
        if (nuevoValor !== '') {
            cartStore.cambiarTipoEntrega(ref({'search': nuevoValor}));
        }
    });

    // Escucha cuando cambia el valor para tipo de entrega, limpia campo search
    watch(() => cartStore.tipoEntrega, (nuevoValor, viejoValor) => {
        if (nuevoValor.cambioTipo != undefined) {
            v_search.value = '';
        }
    })

</script>

<style scoped>

    @media (max-width: 991.98px) {
    /* 1. Quitamos el comportamiento fijo en móvil para que pueda empujar el contenido */
        .encabezado.fixed-top {
            position: relative !important;
            top: auto;
            height: auto !important;
            display: block !important; /* Cambiamos a block para que el logo y el menú colapsen uno abajo del otro si es necesario */
        }

        /* 2. Forzamos a que el menú desplegable use el flujo normal del documento */
        .navbar-collapse.navbar-push {
            position: relative !important;
            width: 100%;
            clear: both;
            padding-top: 15px;
            padding-bottom: 15px;
        }

        /* Optativo: Asegura que el buscador no quede pegado al final del menú */
        #form_search {
            margin-top: 15px;
            width: 100%;
        }
    }

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

    #form_search input {
        height: 45px;
        min-height: 45px;
    }

    #form_search label {
        padding-top: 10px;
    }

    #form_search button:hover {
        box-shadow: 0 7px 5px rgb(181, 52, 113);
    }

    .campoVacio {
        border: 1px solid red;
        border-radius: 6px;
    }

</style>