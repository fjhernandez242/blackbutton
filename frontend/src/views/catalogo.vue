<template>
    <div v-if="catalogo.length">
        <div class="row g-1" id="catalogo">
            <div v-for="producto in catalogo" :key="producto.id" class="col-12 col-sm-6 col-lg-2-4-custom mb-4">
                <div class="card h-100" id="cardProducto">
                    <div class="card-header">
                        <img :src="rutaImagen(producto.imagen)" :alt="producto.producto"
                            class="img-fluid producto-img" @click="acciones(producto.id)" :id="`img_${producto.id}`"
                            :class="{ 'desenfocarImagen': imagenDesenfocada }">
                        <div class="position-absolute acciones" :id="`accion_${producto.id}`" style="display: none;">
                            <div class="btn-goup-vertical" role="group">
                                <button type="button" id="btnVerProducto" class="btn" data-bs-toggle="tooltip"
                                    data-bs-placement="top" title="Ver producto" @click="selecProducto(producto.id)">
                                    <i class="bi bi-eye"></i>
                                </button>
                                <button class="btn" id="btnCarrito" @click="addTopCart(producto)">
                                    <i class="bi bi-cart-plus" data-bs-toggle="tooltip"
                                        data-bs-placement="top" title="Agregado a carrito"></i>
                                </button>
                            </div>
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
                    </div>
                    <div class="card-footer">
                        <small v-if="producto.tipo_entrega == 1">Entrega inmediata</small>
                        <small v-if="producto.tipo_entrega == 2">Sobre pedido</small>
                    </div>
                </div>
            </div>
        </div>
        <modalProducto
            :producto=prodConsultado
            :visible="mostrarModal"
            @cerrar-modal="cerrarModal"/>
    </div>
    <div v-else class="row g-1" id="catalogo">
        <div class="col-12">
            <h4 class="text-center pb-2">No se encontraron amigurumis</h4>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, watch, computed } from 'vue';
    import { API_BASE_URL } from '@/config/api-urls';
    // Importa modal
    import modalProducto from './modal/modalProducto.vue';
    // Importa el servicio para listar productos
    import { getProductos, productoById } from '@/services/catalogo-services';
    // import mensajes de error
    import alertas from '@/assets/js/notifications';
    // props
    import { useCartStore } from '@/store/cartStore';
    const cartStore = useCartStore();
    const addTopCart = (params) => {
        cartStore.addItem(params);
        // Cambia estado del producto
        //setterEstadoProducto({
        //    "id": id,
        //    "estado":
        //});
        // Ocultalos botones de acción al agregar a carrito
        ocultaBotones();
    };

    const carrito = ref(false);
    // Info para edición
    const idProducto = ref(null);
    const mostrarModal = ref(false);
    const imagenDesenfocada = ref(false);
    // Variable para almacenar productos
    const catalogo = ref([]);
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
        listarProductos({'cambioTipo': 0});
    });
    const currentTipo = computed(() => cartStore.tipoEntrega);

    watch(() => cartStore.tipoEntrega, (params) => {
        listarProductos(params);
    })
    // obtenemos el id del producto
    const selecProducto = (id) => {
        idProducto.value = id;
        mostrarModal.value = true;
        obtenerProducto(id);
        // Oculta los botones de acción
        ocultaBotones();
    }
    // Se hace consulta el producto
    // Arreglo para almacenar producto
    const prodConsultado = ref({});
    const obtenerProducto = async (idprod) => {
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
        }
    }
    function cerrarModal() {
        mostrarModal.value = false;
        idProducto.value = null;
    }
    // Función para el manejo de botones de acción
    function acciones(idProducto) {
        // Oculta los botones de acción de todas las tarjetas
        ocultaBotones();
        // const claseImagen = $('#img_' + idProducto);
        if (!imagenDesenfocada.value) {
            // Muestra los botones de acción solo de la tarjeta seleccionada
            muestraBotones(idProducto);
        }
    }
    // Identifica al darse un click fuera de la imagen
    $(window).on('click', function (event) {
        // Valida que no se hayda dado click en una imagen de producto+
        if (!event.target.classList.contains('desenfocarImagen')) {
            ocultaBotones();

        }
    });

    // Acción para ocultar botones de acción
    const ocultaBotones = () => {

        $('.acciones').hide();
        $('.producto-img').removeClass("desenfocarImagen");
    }
    // Acción para mostrar botones de acción
    const muestraBotones = (id) => {
        $('#accion_' + id).show();
        $('#img_' + id).addClass("desenfocarImagen");
    }
</script>

<style scoped>
    #logoMarca {
        max-width: 8%;
    }

    #catalogo {
        padding-top: 3rem;
        padding-inline: 3rem;
        background-color: rgba(238, 247, 255, 0.705);
    }

    #cardProducto {
        border-radius: 10px;
        max-width: 100%;
        max-height: 100%;
        margin-inline: 0.7rem;
        box-shadow: 0 7px 15px rgb(0 0 0 / 0.2);
        cursor: pointer;
    }

    .card-header {
        width: 100%;
        height: 300px;
        overflow: hidden;
        background-color: rgba(238, 247, 255, 0.856);
        border-radius: 10px;
        border: none;
    }

    .producto-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 10px;
        transition: all 0.7s;
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

    @media (min-width: 992px) {
    /* Aplica solo en el breakpoint "lg" (escritorio) de Bootstrap */
    .col-lg-2-4-custom {
        flex: 0 0 auto;
        /* Cada columna ocupa el 20% del ancho del row */
        width: 25%;
    }
}
</style>