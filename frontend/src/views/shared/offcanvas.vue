<template>
    <!-- Zona de carro para compras -->
    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasRightLabel"><b>Mi carrito</b></h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="row ms-4 me-4 text-center" id="btn_mas_info">
            <div class="btn-group" role="group">
                <button class="btn" type="button" data-bs-toggle="collapse" data-bs-target="#collapseS"
                    aria-expanded="false" aria-controls="collapseS">
                    ¿Qué es Sobre pedido?
                </button>
                <button class="btn" type="button" data-bs-toggle="collapse" data-bs-target="#collapseE"
                    aria-expanded="false" aria-controls="collapseE">
                    ¿Qué es Entrega inmediata?
                </button>
            </div>
            <div class="collapse" id="collapseS">
                <div class="card card-body">
                    <h6><b>Sobre pedido:</b></h6>
                    Son Amigurumis que aún necesitan ser tejidos. El tiempo de espera dependerá de la complejidad del diseño.
                </div>
            </div>
            <div class="collapse" id="collapseE">
                <div class="card card-body">
                    <h6><b>Entrega inmediata:</b></h6>
                    Son Amigurumi que ya estan tejidos y listos para ser enviados.
                </div>
            </div>
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
            <div v-for="producto in productos" class="col-12 col-sm-12 mb-2 d-flex justify-content-center">
                <div class="card h-100" id="cardCarrito">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-4">
                                <div class="container-img">
                                    <img :src="rutaImagen(producto.imagen)" :alt="producto.producto"
                                    class="img-fluid img_ref_carrito">
                                </div>
                            </div>
                            <div class="col-8">
                                <ul class="list-unstyled text-left">
                                    <li>
                                        <span>{{ producto.producto }}</span>
                                    </li>
                                    <li>
                                        <span>
                                            <b><i class="bi bi-currency-dollar"></i>{{ producto.precio }}</b>
                                        </span>
                                    </li>
                                    <li>
                                        <small>
                                            <i class="bi bi-rulers pe-1"></i>{{ producto.dimensiones }} cm
                                        </small>
                                    </li>
                                    <li class="text-end">
                                        <div class="conteoProductos">
                                            <button class="btn" @click="deleteProduct(producto.id, producto.tipo_entrega)">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">
                                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                                                    <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8"/>
                                                </svg>
                                            </button>
                                            <small class="text-center">{{ producto.quantity }}</small>
                                            <button class="btn" @click="addTopCart(producto)">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
                                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                                                    <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                                                </svg>
                                            </button>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer badge text-dark" style="font-size: 13px;"
                    :class="[producto.tipo_entrega == 1 ? 'styleEntrega' : 'stylePedido']">
                        <small v-if="producto.tipo_entrega == 1"><b>Entrega inmediata</b></small>
                        <small v-if="producto.tipo_entrega == 2"><b>Sobre pedido</b></small>
                        <!-- Despliegue de información -->
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
    <modalPedido
        :ticket=ticketVenta
        :codigo=codigoVentaGenerado
        :visible="mostrarModal"
        @cerrar-modal="cerrarModal"/>
</template>

<script setup>
    import { watch, ref } from 'vue';
    import { useCartStore } from '@/store/cartStore.js';
    import { API_BASE_URL } from '@/config/api-urls';
    import alertas from '@/assets/js/notifications';
    import { setterProducto, generaCodigoVenta } from '@/services/catalogo-services';
    import { sendMessage } from '@/services/email-services';
    import modalPedido from '../modal/modalPedido.vue';
    const mostrarModal = ref(false);
    const ticketVenta = ref('');
    const codigoVentaGenerado = ref('');
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
        cartStore.deleteItem(id, tipo_entrega);
        if (tipo_entrega == 1) {
            let vaciado = {};
            vaciado.tipo = 'total';
            vaciado.restantes = false
            $.each(cartStore.items, (key, element) => {
                if (element.tipo_entrega == '1') {
                    vaciado.id_prod = id;
                    vaciado.tipo = 'parcial';
                    return false;
                }
            });
            if (vaciado.tipo == 'total' && (cartStore.items).length > 0) {
                vaciado.id_prod = id;
                vaciado.tipo = 'parcial';
                vaciado.restantes = true
            }
            devolver(vaciado);
        }
        // Carga de nuevo los items en el Canvas
        emit('carga_lista');
    }
    // Saca el producto del carrito
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
        if (vaciado.tipo == 'total' || vaciado.restantes) {
            $('#temp_offcanvas').fadeOut();
            $('#temporizador').fadeOut();
            cartStore.detenerTemporizador(vaciado.restantes);
        }
        emit('carga_lista');
    }
    // Contruye la ruta de la imagen
    const rutaImagen = (urlRelativa) => {
        return `${API_BASE_URL}${urlRelativa}`;
    }

    // Detecta el clic para pedido de productos
    const solicitar = async () => {
        // Se genera un códgio de venta
        const codigoGenerado = await generaCodigoVenta();
        // Construye el ticket
        let ticket = sendMessage(codigoGenerado['codigoVenta'], true);

        ticketVenta.value = ticket;
        codigoVentaGenerado.value = codigoGenerado['codigoVenta'];
        mostrarModal.value = true;
    }

    const temp_offcanvas = ref('')
    watch(() => cartStore.segundos, (seg) => {
        temp_offcanvas.value = `${cartStore.minutos}:${seg < 10 ? '0' : ''}${seg}`;
    })

    function cerrarModal() {
        mostrarModal.value = false;
        ticketVenta.value = '';
    }

    // Función para aumentar la cantidad de productos
    const addTopCart = (params) => {
        const producto = {
            'id': params.id,
            'producto': params.producto,
            'precio': params.precio,
            'dimensiones': params.dimensiones,
            'tipo_entrega': params.tipo_entrega
        }
        cartStore.addItem(producto, 1);
        if (params.tipo_entrega == 1) {

            console.log(cartStore.items);

        }
        // ID del temporizador
        // const idSearch = tipo_entrega == 2 ? 'cantProdPed_' : 'cantProd_';
        // const cantidad = $('#'+ idSearch + id).val();
        // if (tipo_entrega == 1) {
        //     $('#'+ idSearch + id).val('1');
        //     if (!cartStore.expiracion.id_temp) {
        //         infoTiempo();
        //     }
        //     ctrlInventario(params, cantidad);
        // } else {
        //     $('#'+ idSearch + params.id).val('1');
        // }
        // cartStore.addItem(params, cantidad);
        // $('.overlay-spinner').hide();
    };
</script>

<style scoped>
    .collapseBtnInfo {
        padding: 1px;
        margin-inline: 3px;
        background-color: aliceblue;
        box-shadow: 0 7px 15px rgb(181, 52, 113);
    }

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
        width: 90%;
        box-shadow: 0 7px 15px rgb(181, 52, 113);
    }

    .container-img {
        width: 100%;
        max-width: 250px;
        height: 100px;
        border-radius: 6px;
        overflow: hidden;
    }

    .img_ref_carrito {
        width: 100%;
        height: 100%;
        border-radius: 10px;
        object-fit: cover;
        object-position: center;
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

    #btn_mas_info button {
        background-color: white;
        font-weight: bold;
        margin-bottom: 7px;
        border: 1px solid rgba(0, 0, 0, 0.432);
    }

    #btn_mas_info button:hover {
        color: white;
        background-color: rgb(181, 52, 113);
    }

    .clickInfo {
        color: white;
        background-color: rgb(181, 52, 113);
    }

    #btn_mas_info .card {
        box-shadow: 0 7px 25px rgb(181, 52, 113);
        margin-bottom: 5px;
    }

    .stylePedido {
        background-color: #c46cf0d8;
    }

    .stylePedido .collapse {
        margin-top: 5px;
    }

    #collapseE .card h6 {
        text-shadow: 0 7px 15px rgb(181, 52, 113);
    }

    .stylePedido .card span {
        text-shadow: 0 7px 15px rgb(181, 52, 113);
    }

    .styleEntrega {
        background-color: #528ad4;
    }

    .styleEntrega .collapse {
        margin-top: 5px;
    }

    #collapseS .card h6 {
        text-shadow: 0 7px 15px rgb(181, 52, 113);
    }

    .styleEntrega .card span {
        text-shadow: 0 7px 15px rgb(19, 104, 214);
    }

    .conteoProductos small {
        border: 1px solid grey;
        padding-top: 5px;
        padding-bottom: 5px;
        padding-inline: 20px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>