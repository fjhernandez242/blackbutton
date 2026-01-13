<template>
    <Transition name="fade-slide">
        <div v-if="props.visible" class="modal" id="trabajoModal" tabindex="-1" aria-labelledby="trabajoModalLabel"
            style="display: block;" aria-modal="true" role="dialog">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-body">
                        <div class="d-flex justify-content-end pb-2">
                            <button type="button" class="btn-close" @click="modalClose()" aria-label="Close"></button>
                        </div>
                        <div class="card h-100" id="cardinfo">
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-xl-6" id="imgContent">
                                        <img :src="rutaImagen(v_imagen)" alt="" id="imgEdit">
                                    </div>
                                    <div class="col-xl-6">
                                        <h3>{{ v_producto }}</h3>
                                        <table class="table">
                                            <tbody>
                                                <tr>
                                                    <th>
                                                        <label for="precio">Precio($): </label>
                                                    </th>
                                                    <th>{{ v_precio }}</th>
                                                </tr>
                                                <tr>
                                                    <th>
                                                        <i class="bi bi-rulers pe-1"></i>
                                                        <label for="dimensiones">Tamaño: </label>
                                                    </th>
                                                    <th>{{ v_dimensiones }} cm</th>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    <div class="d-flex justify-content-end">
                                       <button class="btn" @click="addProduct()" id="btnCerrar">
                                            <i class="bi bi-cart-plus"></i>
                                            Agregar a carrito
                                        </button>
                                   </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
    import { ref, watch } from 'vue';
    import { productoById } from '@/services/catalogo-services';
    import { API_BASE_URL } from '@/config/api-urls';
    // props
    import { useCartStore } from '@/store/cartStore';

    const id_prod = ref();
    const v_imagen = defineModel('imagen');
    const v_producto = defineModel('producto');
    const v_precio = defineModel('precio');
    const v_dimensiones = defineModel('dimensiones');


    // Define emits
    const emit = defineEmits(['cerrar-modal']);
    // Variable reactiva par ID dentro del modal
    const idLocal = ref(null);
    // Define Props
    const props = defineProps({
        productoId: {
            type: [Number, String, null],
            default: null
        }, visible: {
            type: Boolean,
            default: false
        }
    });
    function obtenerProducto(idprod) {
        productoById(idprod).then(
            (response) => {
                const data = response.producto;

                id_prod.value = data['id'];
                v_imagen.value = data['imagen'];
                v_producto.value = data['producto'];
                v_precio.value = data['precio'];
                v_dimensiones.value = data['dimensiones'];
            }
        );
    }
    // 4. Observador (watcher) para reaccionar cuando el ID o la visibilidad cambian
    watch(
        () => props.productoId,
        (idprod) => {
            if (idprod) {
                // Lógica para cargar los datos del trabajo con este ID
                idLocal.value = idprod;
                obtenerProducto(idprod);
            } else {
                // Modo agregar: limpiar o preparar el formulario
                idLocal.value = null;
            }
        },
        { immediate: true } // Ejecutar inmediatamente la primera vez
    );
    const cartStore = useCartStore();
    const addTopCart = () => {
        const params = {
            'id': id_prod.value,
            'producto': v_producto.value,
            'precio': v_precio.value,
            'dimensiones': v_dimensiones.value,
            'imagen': v_imagen.value
        }
        cartStore.addItem(params);
    };

    // Función para cerrar el modal y notificar al padre
    function modalClose() {
        cerrarmodal();
        emit('cerrar-modal');
    }
    function addProduct() {
        addTopCart();
        cerrarmodal();
        emit('cerrar-modal');
    }
    // Contruye la ruta de la imagen
    const rutaImagen = (urlRelativa) => {
        return `${API_BASE_URL}${urlRelativa}`;
    }

    // Función para limpiar campos
    function cerrarmodal() {
        v_imagen.value = '';
        v_producto.value = '';
        v_precio.value = '';
        v_dimensiones.value = '';

    }
</script>

<style scoped>
    .modal-content {
        background-color: rgb(238, 247, 255);
    }

    .modal {
        background: rgba(0, 0, 0, 0.5);
    }
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1040;
        width: 100vw;
        height: 100vh;
    }

    /* 1. Estado inicial del elemento al entrar (antes de que 'visible' sea true)
        o estado final al salir (cuando 'visible' pasa a ser false) */
    .fade-slide-enter-from,
    .fade-slide-leave-to {
    opacity: 0;
    }

    /* 2. Estado de la transición. Define la duración y la función de temporización. */
    .fade-slide-enter-active,
    .fade-slide-leave-active {
    transition: opacity 0.5s ease;
    }

    /* 3. Estado final al entrar (cuando la transición de entrada termina)
        o estado inicial al salir (antes de que 'visible' pase a ser false) */
    .fade-slide-enter-to,
    .fade-slide-leave-from {
    opacity: 1;
    }

    /* Puedes aplicar efectos de transformación al contenido dentro del modal */
    .modal-body {
        transition: transform 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }

    .fade-slide-enter-from .modal-body {
        transform: translateY(-50px);
    }

    #cardinfo {
        width: 100%;
        height: 300px;
        overflow: hidden;
        background-color: rgb(238, 247, 255);
        border-radius: 10px;
        border: none;
    }

    #imgContent {
        max-height: 10%;
    }

    #imgEdit {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 10px;
        box-shadow: 0 7px 15px rgb(181, 52, 113);
    }

    .table {
        margin-top: 2rem;
    }

    .table tr th {
        padding-top: 2rem;
        background-color: rgb(238, 247, 255);
    }

    #btnCerrar {
        background-color: #B53471;
    }

    #btnCerrar:hover {
        background-color: #c56cf0;
    }
</style>
