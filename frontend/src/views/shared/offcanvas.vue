<template>
    <!-- Zona de carro para compras -->
    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="msgInfo" id="msgEnvio">
            <h4><b>¿Cómo te llega tu producto?</b></h4>
            <small>
                Se hace envios a toda la Republica Méxicana, el envio se realiza por
                medio de Correos de México.
            </small>
        </div>
        <div class="msgInfo" id="msgEncargo">
            <h4><b>¿Cómo finalizo mi pago?</b></h4>
            <small>
                El proceso final se realizar con ayuda de WhatsApp, al presionar el botón <b>Completar pedido</b> se te
                redirigirá a WhatsApp para que puedas completar tu pedido.
            </small>
        </div>
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasRightLabel"><b>Mi carrito</b></h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
            <div class="card" id="temp_offcanvas">
                <div class="card-body">
                    <small><b>Tiempo de apartado:</b> {{ temp_offcanvas }}</small>
                </div>
            </div>
            <div v-if="cartStore.totalItemsCount == 0">
                <span>No hay amigurumis seleccionados </span>
                <i class="bi bi-emoji-frown"></i>
            </div>
            <div class="row">
                <div v-for="producto in productos" class="col-12 col-sm-12 mb-2 d-flex justify-content-center">
                    <div class="card" id="cardCarrito">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-10">
                                    <div class="d-flex">
                                    <img :src="rutaImagen(producto.imagen)" :alt="producto.producto"
                                    class="img-fluid" id="img_ref_carrito">
                                    <ul class="list-unstyled text-center">
                                        <li>
                                            <span>{{ producto.producto }}</span>
                                        </li>
                                        <li>
                                            <span>
                                                <b><i class="bi bi-currency-dollar"></i> {{ producto.precio }}</b>
                                            </span>
                                        </li>
                                        <li>
                                            <small>
                                                <i class="bi bi-rulers pe-1"></i> {{ producto.dimensiones }} cm
                                            </small>
                                        </li>
                                    </ul>
                                </div>
                                </div>
                                <div class="col-2 d-flex justify-content-end">
                                    <span v-if="producto.quantity > 1"
                                        class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                        {{ producto.quantity }}
                                        <span class="visually-hidden">Productos en carrito</span>
                                    </span>
                                    <button type="button" class="btn-close" @click="deleteProduct(producto.id, producto.tipo_entrega)" aria-label="Close"></button>
                                </div>
                            </div>
                        </div>
                        <div class="card-footer badge bg-warning text-dark" style="font-size: 13px;">
                            <small v-if="producto.tipo_entrega == 1"><b>Entrega inmediata</b></small>
                            <small v-if="producto.tipo_entrega == 2"><b>Sobre pedido</b></small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="cartStore.totalItemsCount > 0">
            <div class="p-3" id="total_info">
                <div class="row">
                    <div class="col-6">
                        <span><b>Amigurumis: </b></span>
                    </div>
                    <div class="col-6 d-flex justify-content-end">
                        <b>{{ cartStore.totalItemsCount }}</b>
                    </div>
                </div>
                <div class="row pt-2">
                    <div class="col-6">
                        <span><b>Total: </b></span>
                    </div>
                    <div class="col-6 d-flex justify-content-end">
                        <b>$ {{ cartStore.totalPrecio }}</b>
                    </div>
                </div>
                <div id="btn_pedido">
                    <button class="btn btn-sm" @click="solicitar()">Completar pedido</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { watch, ref } from 'vue';
    import { useCartStore } from '@/store/cartStore.js';
    import { API_BASE_URL } from '@/config/api-urls';
    import alertas from '@/assets/js/notifications';
    import { agregarPedido, setterProducto } from '@/services/catalogo-services';
    import { sendMessage } from '@/services/email-services';
    // Recopilado de productos cargados en carrito
    // Instancia del store
    const cartStore = useCartStore();

    const props = defineProps({
        productos: {
            type: Array,
            default: null
    }});
    const emit = defineEmits(['carga_lista']);
    const deleteProduct = (id, tipo_entrega) => {
        // Elimina el producto del carrito
        cartStore.deleteItem(id);
        if (tipo_entrega == 1) {
            let vaciado = {};
            if (cartStore.totalItemsCount === 0) {
                vaciado.tipo = 'total';
            } else {
                vaciado.id_prod = id;
                vaciado.tipo = 'parcial';
            }
            devolver(vaciado);
        }
        // Carga de nuevo los items en el Canvas
        emit('carga_lista');
    }
    // Saca el producto del carrito de producto
    const devolver = async (vaciado) => {
        let params = {
            "codigo_temp": cartStore.expiracion.id_temp
        };
        if (vaciado.tipo == 'parcial') {
            params.id_prod = vaciado.id_prod;
        }
        const response = await setterProducto(params);
        if (response.error) {
            alertas.alertError(response.error);
        }
        if (vaciado.tipo == 'total') {
            $('#temp_offcanvas').fadeOut();
            $('#temporizador').fadeOut();
            cartStore.detenerTemporizador();
        }
        emit('carga_lista');
    }
    // Contruye la ruta de la imagen
    const rutaImagen = (urlRelativa) => {
        return `${API_BASE_URL}${urlRelativa}`;
    }

    // Detecta el clic para pedido de productos
    const solicitar = async () => {
        const result = await alertas.alertQuestion('¿Completar pedido?');
        if (result.isConfirmed) {
            const data = cartStore.items;
            $.each(data, function (index, value) {
                agregarPedido(value, cartStore.expiracion.id_temp).then(
                    (response) => {
                         if (response.error) {
                        alertas.alertError(response.error);
                    } else {
                        sendMessage(response.code);
                        $('#temp_offcanvas').fadeOut();
                        $('#temporizador').fadeOut();
                        cartStore.detenerTemporizador();
                    }
                    }
                );
            });
            return false;
        }

    }

    const temp_offcanvas = ref('')
    watch(() => cartStore.segundos, (seg) => {
        temp_offcanvas.value = `${cartStore.minutos}:${seg < 10 ? '0' : ''}${seg}`;
    })
</script>

<style scoped>
    .msgInfo {
        position: absolute;
        background-color: rgb(238, 247, 255);
        padding: 2rem;
        border-radius: 50px 0 80px 20px;
        right: 26rem;
        left: -30rem;
        box-shadow: 0 7px 15px rgb(181, 52, 113);
    }

    #msgEnvio {
        top: 3rem;
    }

    #msgEncargo {
        top: 13rem;
    }

    #cardCarrito {
        border: none;
        max-width: 90%;
        box-shadow: 0 7px 15px rgb(181, 52, 113);
    }

    #img_ref_carrito {
        max-width: 27%;
        margin-inline: 2%;
        border-radius: 10px;
    }

    #btn_pedido {
        display: flex;
        justify-content: right;
        padding: 10px;
    }

    #btn_pedido button {
        background-color: #B53471;
    }

    #btn_pedido button:hover {
        background-color: #c56cf0;
    }

    #total_info {
        background-color: #c46cf0d8;
    }

    #offcanvasRight {
        background-image: url('/src/assets/img/logo1_sinFondo_50opaci.png');
        background-size: 100%;
        background-position: center;
    }

    #temp_offcanvas {
        display: none;
        margin: 1rem;
        z-index: 1;
        font-size: 20px;
        box-shadow: 0 7px 25px rgb(181, 52, 113);
    }
</style>