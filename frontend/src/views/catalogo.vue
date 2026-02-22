<template>
    <section class="container">
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
                                    <input type="number" :id="`cantProdPed_${producto.id}`" class="form-control"
                                    placeholder="0">
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
                        <div class="card-footer badge bg-warning text-dark" style="font-size: 17px;">
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
</template>

<script setup>
    import { ref, onMounted, watch, computed } from 'vue';
    import { API_BASE_URL } from '@/config/api-urls';
    // Importa modal
    import modalProducto from './modal/modalProducto.vue';
    // Importa el servicio para listar productos
    import { getProductos, productoById, setterProducto } from '@/services/catalogo-services';
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
    // Agrega a carrito
    const addTopCart = (params) => {
        const idSearch = params.tipo_entrega == 2 ? 'cantProdPed_' : 'cantProd_';
        const cantidad = $('#'+ idSearch + params.id).val();
        if (cantidad.length == 0) {
            alertas.alertWarning('Cantidad requerida', false);
            return false;
        }
        if (params.tipo_entrega == 1) {
            ctrlInventario(params, cantidad);
        } else {
            $('#'+ idSearch + params.id).val('');
        }
        cartStore.addItem(params, cantidad);
    };
    // Cambia el estado del producto
    const ctrlInventario = async (params, cantidad) => {
        const params_setter = {
            "id": params.id,
            "cantidad": cantidad
        }
        const response = await setterProducto(params_setter);
        if (response.error) {
            alertas.alertError(response.error);
        }

    };
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
        background-color: #B53471;
    }

    .btn_carrito:hover {
        background-color: #c56cf0;
    }

    /** media */
    @media (max-width: 768px) {
        .container-img {
            height: 200px;
        }
    }

    @media (max-width: 480px) {
        .container-img {
            height: 180px;
        }
    }
</style>