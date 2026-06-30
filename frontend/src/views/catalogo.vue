<template>
    <Transition>
        <section class="container">
            <div class="card" id="temporizador">
                <div id="msgTempExp">
                    <h6><b>Los Amigurumis con etiqueta "Sobre pedido" son apartados por 15 minutos</b></h6>
                    <small>Al expirar el tiempo saldrán de tu carrito y de apartados.</small>
                </div>
                <div class="card-body d-flex">
                    <i class="bi bi-info-circle py-2 pe-2" @click="infoTiempo(true)" style="font-size: 1rem; cursor: pointer;"></i>
                    <small>{{ temporizador }}</small>
                </div>
            </div>
            <div v-if="catalogo.length" class="row row-cols-1 row-cols-sm-2 row-cols-md-4 g-1">
                <div v-for="producto in catalogo" :key="producto.id">
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-header">
                                <div class="container-img">
                                    <img :src="rutaImagen(producto.imagen)" :alt="producto.producto"
                                        class="img-fluid" @click="selecProducto(producto.id)" :id="`img_${producto.id}`">
                                </div>
                            </div>
                            <div class="card-body">
                                <h5>{{ producto.producto }}</h5>
                                <div class="row pb-2">
                                    <div class="col-md-6 text-start">
                                        <span>
                                            <b><i class="bi bi-currency-dollar"></i>{{ producto.precio }}</b>
                                        </span>
                                    </div>
                                    <div class="col-md-6 text-end">
                                        <small>
                                            <i class="bi bi-rulers pe-1"></i> {{ producto.dimensiones }} cm
                                        </small>
                                    </div>
                                </div>
                                <div v-if="producto.tipo_entrega == 2">
                                    <div class="input-group mb-1">
                                        <span class="input-group-text">Cantidad</span>
                                        <select class="form-select" :id="`cantProdPed_${producto.id}`">
                                            <option value="1" selected>1</option>
                                            <option value="2">2</option>
                                            <option value="3">3</option>
                                            <option value="4">4</option>
                                            <option value="5">5</option>
                                        </select>
                                    </div>
                                </div>
                                <div v-else>
                                    <div class="input-group mb-1">
                                        <label class="input-group-text" for="cantProd">Cantidad</label>
                                        <select class="form-select" :id="`cantProd_${producto.id}`">
                                            <option v-for="cantidad in producto.inventario" :value="cantidad">
                                                {{ cantidad }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <div class="input-group">
                                    <button class="btn btn_carrito w-100" @click="addTopCart(producto)">
                                        <i class="bi bi-cart-plus"></i>
                                        Agregar a carrito
                                    </button>
                                </div>
                            </div>
                            <div class="card-footer badge text-dark footerInfo">
                                <small v-if="producto.tipo_entrega == 1"><b>Entrega inmediata</b></small>
                                <small v-if="producto.tipo_entrega == 2"><b>Sobre pedido</b></small>
                            </div>
                        </div>
                    </div>
                </div>
                <modalProducto
                    :producto=prodConsultado
                    :visible="mostrarModal"
                    @cerrar-modal="cerrarModal"/>
            </div>
            <div v-else class="row g-1">
                <div class="col-12">
                    <h4 class="text-center pb-2">No se encontraron amigurumis</h4>
                </div>
            </div>
        </section>
    </Transition>
</template>

<script setup>
    import { ref, onMounted, watch, computed } from 'vue';
    import { API_BASE_URL } from '@/config/api-urls';
    // Importa modal
    import modalProducto from './modal/modalProducto.vue';
    // Importa el servicio para listar productos
    import { getProductos, productoById, setterProducto, apartarProducto } from '@/services/catalogo-services';
    // import mensajes de error
    import alertas from '@/assets/js/notifications';
    // props
    import { useCartStore } from '@/store/cartStore';
    // Info para edición
    const idProducto = ref(null);
    const mostrarModal = ref(false);
    // Variable para almacenar productos
    const catalogo = ref([]);
    const cartStore = useCartStore();
    const temporizador = ref('');
    // Agrega a carrito
    const addTopCart = (params) => {
        $('.overlay-spinner').show();
        // ID del temporizador
        const idSearch = params.tipo_entrega == 2 ? 'cantProdPed_' : 'cantProd_';
        const cantidad = $('#'+ idSearch + params.id).val();
        if (params.tipo_entrega == 1) {
            $('#'+ idSearch + params.id).val('1');
            if (!cartStore.expiracion.id_temp) {
                infoTiempo();
            }
            ctrlInventario(params, cantidad);
        } else {
            $('#'+ idSearch + params.id).val('1');
        }
        cartStore.addItem(params, cantidad);
        $('.overlay-spinner').hide();
    };
    // Cambia el estado del producto
    const ctrlInventario = async (params, cantidad) => {
        const response = await setterProducto({
            "id": params.id,
            "cantidad": cantidad
        });
        if (response.error) {
            alertas.alertError(response.error);
        }
        // Si ya existe un codigo de temporal para el usuario se agrega
        let param_apartado = {
            "id_prod": params.id,
            "cantidad": cantidad,
            "codigo_temp": ""
        }
        if (cartStore.expiracion.id_temp != '') {
            param_apartado.codigo_temp = cartStore.expiracion.id_temp || null;
        }

        const apartado = await apartarProducto(param_apartado);
        if (apartado.error) {
            alertas.alertError(response.error);
        } else {
            // Guarda el codigo temporal y la fecha de expración
            if (!cartStore.expiracion.id_temp) {
                cartStore.setTemp(apartado.cod_tem, apartado.time_expired);
                if (cartStore.expiracion.id_temp) {
                    $('#temporizador').show();
                    $('#temp_offcanvas').show();
                }
            }
        }
        listarProductos({'cambioTipo': 0});
    };
    const infoTiempo = (click) => {
        if (click) {
            $('#msgTempExp').stop(true, true).show();
        } else {
            setTimeout(() => $('#msgTempExp').stop(true, true).show(), 1500);
        }
        setTimeout(() => $('#msgTempExp').fadeOut(), 5000);
    }
    const currentTipo = computed(() => cartStore.tipoEntrega);

    watch(() => cartStore.tipoEntrega, (params) => {
        listarProductos(params);
    })
    watch(() => cartStore.segundos, (seg) => {
        temporizador.value = `${cartStore.minutos}:${seg < 10 ? '0' : ''}${seg}`;
        if (cartStore.minutos == 0 && seg == 0) {
            $('#temporizador').fadeOut();
            $('#temp_offcanvas').fadeOut();
            devolver();
        }
    })
    // Señal entrante para recargar catalogo al quitar productos del carrito
    watch(() => cartStore.recarga, () => {
        listarProductos({'cambioTipo': 0});
    })
    // Retorna de producto
    const devolver = async () => {
        const response = await setterProducto({
            "codigo_temp": cartStore.expiracion.id_temp
        });
        if (response.error) {
            alertas.alertError(response.error);
        }
    }
    const listarProductos = async (params) => {
        getProductos(params).then(
            (data) => {
                catalogo.value = data.productos;
            }
        ).catch(error => {
            console.log("Error al obtener los datos: ", error);
            alertas.alertError('Error al obtener los datos');
        });
    };
    // Contruye la ruta de la imagen
    const rutaImagen = (urlRelativa) => {
        return `${API_BASE_URL}${urlRelativa}`;
    }
    // Llama los archivos al iniciar la página
    // Escucha el cambio del tipo de producto
    onMounted(() => {
        // Recarga de catalogo
        listarProductos({'cambioTipo': 0});
        cartStore.iniciarTemporizador();
        if (cartStore.expiracion.id_temp) {
            $('#temporizador').show();
            $('#temp_offcanvas').show();
        }

    });
    // obtenemos el id del producto
    const selecProducto = (id) => {
        idProducto.value = id;
        mostrarModal.value = true;
        obtenerProducto(id);
    }
    // Se hace consulta el producto
    // Arreglo para almacenar producto
    const prodConsultado = ref({});
    const obtenerProducto = async (idprod) => {
        $('.overlay-spinner').show();
        // Espera la respuesta del servicio
        const response = await productoById(idprod);
        if (response?.producto) {
            const data = response.producto;
            prodConsultado.value = {
                'id': data['id'],
                'imagen': data['imagen'],
                'producto': data['producto'],
                'precio': data['precio'],
                'dimensiones': data['dimensiones'],
                'tipo_entrega': data['tipo_entrega'],
                'inventario': data['inventario'],
                'comentario': data['comentario']
            };
            $('.overlay-spinner').hide();
        }
    }
    const cerrarModal = ([accion, datos]) => {
        mostrarModal.value = false;
        idProducto.value = null;

        if (accion == 'addProd' && datos) {
            addTopCart(datos);
        }
    }

</script>

<style scoped>
    .container {
        padding: 1rem;
        padding-inline: 4rem;
        background-color: rgba(238, 247, 255, 0.705);
    }

    .card {
        margin-inline: 0.2rem;
    }

    #cardProducto {
        box-shadow: 0 7px 15px rgb(0 0 0 / 0.2);
        cursor: pointer;
    }

    .container-img {
        width: 100%;
        max-width: 400px;
        height: 300px;
        margin-left: auto;
        margin-right: auto;
        border-radius: 6px;
        overflow: hidden;
    }

    .container-img img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
        cursor: pointer;
    }

    .color1 {
        background-color: #c56cf0;
    }
    .color2 {
        background-color: #B53471;
    }
    .color3 {
        background-color: #6D214F;
    }

    .acciones {
        top: 35%;
        left: 35%;
        background-color: #6D214F;
        border-radius: 10px;
    }

    #btnVerProducto,
    #btnCarrito {
        transform: scale3d(0);
        transition: all 0.5s;
    }

    #btnVerProducto:hover,
    #btnCarrito:hover {
        color: white;
        transform: scale3d(1.9, 1.9, 1.9);
        transition: all 0.5s;
    }

    .desenfocarImagen {
        transition: all 0.5s;
        filter: blur(15px);
        transform: scale(1.2,1.4);
    }


    .btn_carrito {
        box-shadow: 0 2px 10px rgb(181, 52, 113);
    }

    .btn_carrito:hover {
        background-color: #c56cf0;
    }

    .footerInfo {
        font-size: 17px;
        /*background: linear-gradient(to right, rgba(76, 0, 255, 0.685), #B53471);*/
        box-shadow: 0 7px 25px rgb(181, 52, 113);
    }

    #temporizador {
        display: none;
        position: fixed;
        right: 0;
        top: 6rem;
        margin: 1rem;
        z-index: 1;
        box-shadow: 0 7px 25px rgb(181, 52, 113);
    }

    #temporizador .card-body {
        font-size: 28px;
        font-weight: bold;
        padding-top: 2px;
        padding-bottom: 2px;
    }

    #msgTempExp {
        display: none;
        position: fixed;
        background-color: rgb(238, 247, 255);
        padding: 1.5rem;
        border-radius: 50px 0 80px 20px;
        right: 7rem;
        left: 68rem;
        box-shadow: 0 7px 15px rgb(181, 52, 113);
        top: 8.3rem;
        transition: all 0.7ms;
    }

    /** media */
    @media (min-width: 1700px) and (max-width: 1800px) {
        #msgTempExp {
            left: 70rem;
        }
    }

    @media (min-width: 1300px) and (max-width: 1700px) {
        #msgTempExp {
            left: 50rem;
        }
    }

    @media (min-width: 1125px) and (max-width: 1300px) {
        #msgTempExp {
            left: 40rem;
        }
    }

    @media (min-width: 800px) and (max-width: 1125px) {
        #msgTempExp {
            left: 20rem;
        }
    }

    @media (min-width: 481px) and (max-width: 800px) {
        #msgTempExp {
            /* Este estilo NO afectará a móviles (menos de 480px) */
            /* NI a laptops (más de 768px) */
            left: 10rem;
        }
    }

    @media screen and (max-width: 480px) {
        #msgTempExp {
            left: 1rem;
        }

        .container {
            padding-inline: 0.5rem;
        }
    }

</style>