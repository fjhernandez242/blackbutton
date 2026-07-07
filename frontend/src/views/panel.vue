<template>
    <transition>
    <section>
        <div class="container">
            <div class="row">
                <div class="col-12 d-flex justify-content-end">
                    <button class="btn btn-sm" @click="logout()">Cerrar Sesión</button>
                </div>
            </div>
            <div class="row w-50 text-start d-flex align-items-center" id="filtroIndicadores">
                <div class="col-12 col-md-6">
                    <h4><b>Indicadores</b></h4>
                </div>
                <div class="col-12 col-md-6 pb-2">
                    <div class="form-floating">
                        <select class="form-select" id="indicadorFiltro" aria-label="Floating label select example"
                            v-model="v_filtro_indicador">
                            <option value="T" selected>Todos</option>
                            <option value="H" >Hoy</option>
                            <option value="E">Este mes</option>
                            <option value="A">Mes anterior</option>
                        </select>
                        <label for="indicadorFiltro">Filtrar indicadores</label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-4 position-relative">
                    <div class="translate-middle-y" id="icon-cash">
                        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-hourglass-split" viewBox="0 0 16 16">
                        <path d="M2.5 15a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1 0-1h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1zm2-13v1c0 .537.12 1.045.337 1.5h6.326c.216-.455.337-.963.337-1.5V2zm3 6.35c0 .701-.478 1.236-1.011 1.492A3.5 3.5 0 0 0 4.5 13s.866-1.299 3-1.48zm1 0v3.17c2.134.181 3 1.48 3 1.48a3.5 3.5 0 0 0-1.989-3.158C8.978 9.586 8.5 9.052 8.5 8.351z"/>
                        </svg>
                    </div>
                    <div class="card" id="ventasCompletas">
                        <div class="card-header ps-5 bg-transparent border-0">
                            <small class="text-muted fw-bold">Pedidos en proceso</small>
                        </div>
                        <div class="card-body ps-5">
                            <p class="mb-0" style="font-size: 20px;">{{ conteoVentas.ventas_proceso }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 position-relative">
                    <div class="translate-middle-y" id="icon-top">
                        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-cash-coin" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M11 15a4 4 0 1 0 0-8 4 4 0 0 0 0 8m5-4a5 5 0 1 1-10 0 5 5 0 0 1 10 0"/>
                        <path d="M9.438 11.944c.047.596.518 1.06 1.363 1.116v.44h.375v-.443c.875-.061 1.386-.529 1.386-1.207 0-.618-.39-.936-1.09-1.1l-.296-.07v-1.2c.376.043.614.248.671.532h.658c-.047-.575-.54-1.024-1.329-1.073V8.5h-.375v.45c-.747.073-1.255.522-1.255 1.158 0 .562.378.92 1.007 1.066l.248.061v1.272c-.384-.058-.639-.27-.696-.563h-.668zm1.36-1.354c-.369-.085-.569-.26-.569-.522 0-.294.216-.514.572-.578v1.1zm.432.746c.449.104.655.272.655.569 0 .339-.257.571-.709.614v-1.195z"/>
                        <path d="M1 0a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h4.083q.088-.517.258-1H3a2 2 0 0 0-2-2V3a2 2 0 0 0 2-2h10a2 2 0 0 0 2 2v3.528c.38.34.717.728 1 1.154V1a1 1 0 0 0-1-1z"/>
                        <path d="M9.998 5.083 10 5a2 2 0 1 0-3.132 1.65 6 6 0 0 1 3.13-1.567"/>
                        </svg>
                    </div>
                    <div class="card" id="ventasCompletas">
                        <div class="card-header ps-5 bg-transparent border-0">
                            <small class="text-muted fw-bold">Pedidos completados</small>
                        </div>
                        <div class="card-body ps-5">
                            <p class="mb-0" style="font-size: 20px;">{{ conteoVentas.ventas_completas }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 position-relative">
                    <div class="translate-middle-y" id="icon-cancel">
                        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-x-square" viewBox="0 0 16 16">
                        <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z"/>
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                        </svg>
                    </div>
                    <div class="card" id="ventasCompletas">
                        <div class="card-header ps-5 bg-transparent border-0">
                            <small class="text-muted fw-bold">Pedidos cancelados</small>
                        </div>
                        <div class="card-body ps-5">
                            <p class="mb-0" style="font-size: 20px;">{{ conteoVentas.ventas_canceladas }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <p class="line_horizontal"></p>
            <h4><b>Buscar pedido</b></h4>
            <div class="card">
                <div class="card-body">
                    <div class="row">
                        <div class="col-lg-7 col-md-12 col-sm-12">
                            <form @submit.prevent="rastrearProducto" class="row g-2 align-items-end needs-validation" novalidate>
                                <div class="col-md-5 col-12">
                                    <label for="cve_busqueda" class="form-label">Clave de pedido</label>
                                    <div class="input-group mb-3">
                                        <span class="input-group-text"><i class="bi bi-fingerprint"></i></span>
                                        <input type="text" class="form-control limpiarCampo" name="cve_busqueda" id="cve_busqueda"
                                            v-model="v_cve_busqueda" placeholder="Clave de pedido">
                                    </div>
                                </div>
                                <div class="col-md-1 col-12 d-flex justify-content-center align-items-center"
                                    style="height: 55px;">
                                    <p>Ó</p>
                                </div>
                                <div class="col-md-6 col-12">
                                    <label for="fech_busqueda" class="form-label">Rango de fechas (incial y final)</label>
                                    <div class="input-group mb-3">
                                        <input type="date" class="form-control limpiarCampo" name="fech_busqueda" id="fech_busqueda"
                                            v-model="v_fech_busqueda" placeholder="Fecha de pedido">
                                        <input type="date" class="form-control limpiarCampo ms-1" name="fech_busqueda" id="fech_busqueda"
                                            v-model="v_fech_busqueda_fin" placeholder="Fecha de pedido">
                                    </div>
                                </div>
                                <div class="row d-flex justify-content-center align-items-center">
                                    <div class="col-lg-6 col-md-6 col-sm-12 btn-group">
                                        <button type="submit" class="btn">
                                            Rastrear
                                        </button>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <p class="line_vertical"></p>
                        <div class="col-lg-4 col-md-12 col-sm-12 d-flex justify-content-center align-items-center">
                            <table class="table-responsive">
                                <thead>
                                    <tr>
                                        <th colspan="3" class="text-center">Filtros rápidos de búsqueda</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>
                                            <button class="btn m-1" @click="filtrar('h')">Hoy</button>
                                        </td>
                                        <td>
                                            <button class="btn m-1" @click="filtrar('e')">Este mes</button>
                                        </td>
                                        <td>
                                            <button class="btn m-1" @click="filtrar('a')">Mes anterior</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div v-if="prod_reastreado != ''" >
                        <div class="row mt-3">
                            <div class="col">
                                <div class="col-12 d-flex justify-content-end mb-2">
                                    <button type="button" @click="limpiarCampo('tabla')" class="btn"
                                        data-bs-toggle="tooltip" data-bs-placement="top" title="Limpiar busqueda">
                                        Limpiar
                                    </button>
                                </div>
                                <div v-for="(ventas, fecha) in prod_reastreado" :key="fecha" class="card mb-2">
                                    <div class="card-header">
                                        <b>Fecha:</b> {{ fecha }}
                                    </div>
                                    <div class="card-body">
                                        <div v-for="(datosProducto, claveVenta) in ventas" :key="claveVenta" class="p-1">
                                            <div class="row">
                                                <div class="col-md-3 col-12">
                                                    <h6 class="text-secondary">
                                                        Código Pedido: <span style="background-color: #B53471;" class="badge text-white">{{ claveVenta }}</span>
                                                    </h6>
                                                </div>
                                                <div class="col-md-4 col-12">
                                                    <h6 class="ms-md-3">
                                                        Estado del pedido:
                                                        <span class="badge text-white fondoEnProceso"
                                                            v-if="datosProducto.productos[0].estado == 1">EN PROCESO</span>
                                                        <span class="badge text-white fondoFinaliado"
                                                            v-if="datosProducto.productos[0].estado == 2">FINALIZADO</span>
                                                        <span class="badge text-white fondoCancelada"
                                                            v-if="datosProducto.productos[0].estado == 3">CANCELADO</span>
                                                    </h6>
                                                </div>
                                                <div class="col-md-5 col-12 d-flex justify-content-center align-items-center" v-if="datosProducto.productos[0].estado == 1">
                                                    <h6 class="ms-md-3">
                                                        Marcar como:
                                                    </h6>
                                                    <div class="btn-group mb-2 ms-md-2">
                                                        <button type="button" class="btn btn-sm"
                                                            @:click="cambiarEstadoPedido('completar', claveVenta)" :disabled="completado"
                                                            data-bs-toggle="tooltip" data-bs-placement="top" title="Marcar finalizado">
                                                            <span>Finalizado</span> <i class="bi bi-check-circle"></i></button>
                                                        <button type="button" class="btn btn-sm"
                                                            @:click="cambiarEstadoPedido('cancelar', claveVenta)" :disabled="cancelado"
                                                            data-bs-toggle="tooltip" data-bs-placement="top" title="Marcar cancelado">
                                                            <span>Cancelado</span> <i class="bi bi-x-circle"></i></button>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="table-responsive">
                                                <table class="table table-striped table-bordered">
                                                    <thead>
                                                        <tr>
                                                            <th scope="col" class="text-center">Amigurumi</th>
                                                            <th scope="col" class="text-center">Tipo de entrega</th>
                                                            <th scope="col" class="text-center">Precio(c/u)</th>
                                                            <th scope="col" class="text-center">Cantidad</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(prod, index) in datosProducto.productos" :key="index">
                                                            <td class="text-start">{{ prod.nombre }}</td>
                                                            <td class="text-start" v-if="prod.tipo_entrega == 2">Sobre Pedido</td>
                                                            <td class="text-start" v-else>Entrega Inmediata</td>
                                                            <td class="text-end">{{ formatearMoneda(prod.precio) }}</td>
                                                            <td class="text-end">{{ prod.cantidad }}</td>
                                                        </tr>
                                                    </tbody>
                                                    <tfoot>
                                                        <tr id="fTotales">
                                                            <td colspan="2">Total</td>
                                                            <td class="text-end">{{ formatearMoneda(datosProducto.total_costo) }}</td>
                                                            <td class="text-end">{{ datosProducto.total_productos }}</td>
                                                        </tr>
                                                    </tfoot>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 d-flex justify-content-end">
                                    <button type="button" @click="limpiarCampo('tabla')" class="btn"
                                        data-bs-toggle="tooltip" data-bs-placement="top" title="Limpiar busqueda">
                                        Limpiar
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <p class="line_horizontal"></p>
            <h4>
                <b style="cursor: pointer;"
                   :class="[activarAgregar ? '' : 'btnOpacity']" @click="cambioProceso('agregar')">Agrega Amigurumi</b> |
                <b style="cursor: pointer;"
                   :class="[activarEditar ? '' : 'btnOpacity']" @click="cambioProceso('editar')">Editar Amigurumi</b>
            </h4>
            <div class="card">
                <div class="card-body p-4">
                    <form id="addProd" @submit.prevent="nuevoProducto" class="row g-3 needs-validation" novalidate>
                        <div class="col-md-5 col-12" :class="[activarAgregar ? 'ocultarFormulario' : '']">
                            <label for="tipo_entrega" class="form-label fw-semibold">Eligé el amigurumi a editar<span class="required">*</span></label>
                            <div class="input-group has-validation">
                                <span class="input-group-text"><i class="bi bi-pencil-square"></i></span>
                                <select class="form-select limpiarCampo" name="tipo_entrega" id="tipo_entrega"
                                    v-model="v_escogeEdicion" required>
                                    <option value="0" selected disabled>- Eligé uno -</option>
                                    <option v-for="prod in catalogo" :value="prod.id">{{ prod.producto }}</option>
                                </select>
                                <div class="invalid-feedback">
                                Por favor indique el tipo de entrega!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 col-12" :class="[activarAgregar ? 'ocultarFormulario' : '']">
                            <label for="estado" class="form-label fw-semibold">Estado del producto<span class="required">*</span></label>
                            <div class="input-group has-validation">
                                <span class="input-group-text"><i class="bi bi-cart-check"></i></span>
                                <select class="form-select limpiarCampo" name="estado" id="estado"
                                    v-model="v_estado" required :disabled="!elementoActEdit">
                                    <option value="" selected disabled>- Indica el estado -</option>
                                    <option value="D">Disponible</option>
                                    <option value="R">Reservado</option>
                                    <option value="A">Agotado</option>
                                </select>
                                <div class="invalid-feedback">
                                Por favor indica el estado!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4 col-12 text-center" :class="[activarAgregar ? 'ocultarFormulario' : '']">
                            <div class="container-img">
                                <img v-if="elementoActEdit" :src="rutaImagen(v_prod_select['imagen'])" :alt="v_prod_select['producto']"
                                    class="img-fluid img_ref_edit">
                            </div>
                        </div>
                        <div class="col-lg-6 col-md-6 col-sm-12">
                            <label for="producto" class="form-label fw-semibold">¿Qué nombre le pondrás?<span class="required">*</span></label>
                            <div class="input-group has-validation">
                                <span class="input-group-text"><i class="bi bi-alphabet-uppercase"></i></span>
                                <input type="text" class="form-control limpiarCampo" name="producto" id="producto"
                                    v-model="v_producto" placeholder="Nombre" required :disabled="!elementoActEdit"
                                    :class="[nombreLargo ? 'borderRed' : '']">
                                <span id="msgNombre" v-if="nombreLargo">El nombre es muy lago</span>
                                <div class="invalid-feedback">
                                Por favor indica su nombre!
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-6 col-sm-6">
                            <label for="precio" class="form-label fw-semibold">¿Qué valor le colocaras?<span class="required">*</span></label>
                            <div class="input-group has-validation">
                                <span class="input-group-text">$</span>
                                <input type="number" step="any" class="form-control limpiarCampo" name="precio" id="precio"
                                v-model="v_precio" placeholder="0" required :disabled="!elementoActEdit">
                                <div class="invalid-feedback">
                                Por favor indique el precio!
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-6 col-sm-6">
                            <label for="inventario" class="form-label fw-semibold">¿Cuántos hay en existencia?<span class="required">*</span></label>
                            <div class="input-group has-validation">
                                <span class="input-group-text"><i class="bi bi-box-seam-fill"></i></span>
                                <input type="number" class="form-control limpiarCampo" name="inventario" id="inventario"
                                v-model="v_inventario" placeholder="0" required :disabled="!elementoActEdit">
                                <div class="invalid-feedback">
                                Por favor indique la cantidad en existencia!
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-6 col-md-6 col-sm-12">
                            <label for="dimensiones" class="form-label fw-semibold">¿Cuál es su medida en cm?<span class="required">*</span></label>
                            <div class="input-group has-validation">
                                <span class="input-group-text"><i class="bi bi-rulers"></i></span>
                                <input type="number" step="any" class="form-control limpiarCampo" name="dimensiones"
                                    id="dimensiones" v-model="v_dimensiones" placeholder="Medida" required :disabled="!elementoActEdit">
                                <div class="invalid-feedback">
                                Por favor indique las dimensiones!
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-6 col-md-12 col-sm-12">
                            <label for="tipo_entrega" class="form-label fw-semibold">Tipo de Entrega<span class="required">*</span></label>
                            <div class="input-group has-validation">
                                <span class="input-group-text"><i class="bi bi-cart-fill"></i></span>
                                <select class="form-select limpiarCampo" name="tipo_entrega" id="tipo_entrega"
                                    v-model="v_disponible" required :disabled="!elementoActEdit">
                                    <option value="" selected disabled>- Indica el tipo de entrega -</option>
                                    <option value="1">Entrega Inmediata</option>
                                    <option value="2">Sobre pedido</option>
                                </select>
                                <div class="invalid-feedback">
                                Por favor indique el tipo de entrega!
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-6 col-md-12 col-sm-12">
                            <label for="img_ref" class="form-label fw-semibold">Muestra su mejor foto<span v-if="!editar" class="required">*</span></label>
                            <div class="input-group mb-3">
                                <span class="input-group-text"><i class="bi bi-card-image"></i></span>
                                <input type="file" id="img_ref" class="form-control limpiarCampo" ref="archivoInput" :disabled="!elementoActEdit">
                            </div>
                        </div>
                        <div class="col-lg-6 col-md-12 col-sm-12">
                            <label for="comentario" class="form-label fw-semibold">Agrega un comentario</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text"><i class="bi bi-chat-dots-fill"></i></span>
                                <textarea id="comentario" class="form-control limpiarCampo" v-model="v_comentario"
                                placeholder="Comentario" :disabled="!elementoActEdit"></textarea>
                            </div>
                        </div>
                        <div class="col-12 d-flex justify-content-end mt-4">
                            <button type="submit" class="btn" :disabled="enviando">
                                {{ enviando ? 'Cargando...' : textoBoton }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
    </transition>
</template>

<script setup>
    import { ref, onMounted, watch } from 'vue';
    import { cargarProducto, editarProducto, obtenerPedido, procesarPedido, calculoVentas, getProductos } from '@/services/catalogo-services';
    import { cerrarSesion } from '@/services/usuario-services';
    // Importa script para notificaciones SweetAlert2
    import alertas from '@/assets/js/notifications';
    // Importa archivo de errores
    import { getErrorMessages } from '@/assets/errorMessages';
    import router from '@/router';
    import { API_BASE_URL } from '@/config/api-urls';

    // Variable busqueda
    const v_cve_busqueda = ref('');
    const v_fech_busqueda = ref('');
    const v_fech_busqueda_fin = ref('');
    // Variables formularios
    const v_producto = ref('');
    const v_precio = ref(0);
    const v_dimensiones = ref(0);
    const v_disponible = ref('');
    const v_inventario = ref(0);
    const v_comentario = ref('');

    const archivoInput = ref(null);
    const enviando = ref(false);
    // Variable para texto de botón
    const textoBoton = ref('Cargar producto');
    // Contiene el producto buscado
    const prod_reastreado = ref([]);
    const sumaProdCantidad = ref({
        totalCosto: 0,
        totalCantidad: 0
    });
    // Variables para manejo de pedido
    const completado = ref(false);
    const cancelado = ref(false);
    // Vartiable para conteo
    const conteoVentas = ref({});
    // Escucha el cambio del tipo de producto
    onMounted(() => {
        // Recarga de catalogo
        obtenerConteoVentas({'periodo': 'T'});
    });
    // Función para rastrear produto
    async function rastrearProducto() {
        $('.overlay-spinner').show();
        limpiarCampo('busqueda');

        let paramsSearch = '';
        let refBusqueda = 'cve';
        if (v_cve_busqueda.value !== '' && (v_fech_busqueda.value !== '' || v_fech_busqueda_fin.value !== '')) {
            paramsSearch = v_cve_busqueda.value;
        } else if (v_cve_busqueda.value === '' && (v_fech_busqueda.value !== '' && v_fech_busqueda_fin.value !== '')) {
            paramsSearch = { 'fini': v_fech_busqueda.value, 'ffin': v_fech_busqueda_fin.value };
            refBusqueda = 'fecha';
        } else if (v_cve_busqueda.value !== '' && (v_fech_busqueda.value === '' && v_fech_busqueda_fin.value === '')) {
            paramsSearch = v_cve_busqueda.value;
        }
        if (paramsSearch == '') {
            $('.overlay-spinner').hide();
            alertas.alertWarning(getErrorMessages(104), false, 1500);
            return;
        }
        await obtenerPedido(
            {
                'tipo': refBusqueda,
                'dato': paramsSearch
            }
        ).then(
            (response) => {
                if (response.error) {
                    alertas.alertError(response.error);
                    limpiarCampo('tabla');
                } else {
                    if (response?.pedido) {
                        // $('.overlay-spinner').hide();
                        prod_reastreado.value = response.pedido;
                    } else {
                        alertas.alertWarning(response.info);
                        limpiarCampo('tabla');
                    }
                }
                $('.overlay-spinner').hide();
            }
        );
    }
    // Función para marcar como completado o venta finalizada
    async function cambiarEstadoPedido(estado, cve) {
        let pregunta, mensaje;
        if (estado == 'completar') {
            pregunta = '¿Completar venta?';
            mensaje = 'Venta completada';
        }
        if (estado == 'cancelar') {
            pregunta = '¿Cancelar venta?';
            mensaje = 'Venta cancelada';
        }
        const completar = await alertas.alertQuestion(pregunta);
        $('.overlay-spinner').show();
        if (completar.isConfirmed) {
            await procesarPedido({
                'cve': cve,
                'estado': estado
            }).then(
                (response) => {
                    if (response.error) {
                        alertas.alertError(response.error);
                    } else {
                        alertas.alertSuccess(mensaje);
                        limpiarCampo('tabla');
                    }
                }
            );
        }
        $('.overlay-spinner').hide();
        obtenerConteoVentas({'periodo': 'T'});
    }
    const formatearMoneda = (valor) => {
        if (valor == null) return '$0.00';
            return new Intl.NumberFormat('es-MX', {
                style: 'currency',
                currency: 'MXN',
                minimumFractionDigits: 2, // Fuerza a que siempre tenga mínimo 2 decimales
                maximumFractionDigits: 2  // Redondea a máximo 2 decimales
        }).format(valor);
    };
    // Función para obtener conteo de ventas
    const obtenerConteoVentas = async (params) => {
        calculoVentas(params).then(
            (data) => {
                conteoVentas.value = data;
            }
        ).catch(error => {
            console.log("Error al obtener los datos: ", error);
            alertas.alertError('Error al obtener las ventas');
        });
    };// Llama los archivos al iniciar la página

    // Función para el cerrado de sesion
    async function logout() {
        const params = {
            'user': localStorage.getItem('admin_user'),
            'token': localStorage.getItem('admin_token')
        };
        $('.overlay-spinner').show();
        try {
            const response = await cerrarSesion(params);

            if (response.error) {
                alertas.alertError(response.error);
            } else if (response.detail) {
                alertas.alertError(response.detail);
            }
        } catch (error) {
            console.log('No fue posible cerrar sesión en el servidor: ', error);
            alertas.alertError('Sesión local finalizada (Servidor no disponible).');
        } finally {
            // Este bloque siempre se ejecuta (falle o tenga éxito la petición)
            $('.overlay-spinner').hide();
            localStorage.removeItem('admin_token');
            localStorage.removeItem('admin_token_expires');
            localStorage.removeItem('admin_user');

            router.push('login_panel');
        }
    }
    // Función para filtrar busqueda de pedido
    async function filtrar(filtro) {
        $('.overlay-spinner').show();

        await obtenerPedido(
            {
                'tipo': 'fecha',
                'dato': filtro,
                'filtro': true
            }
        ).then(
            (response) => {
                if (response.error) {
                    alertas.alertError(response.error);
                    limpiarCampo('tabla');
                } else {
                    if (response?.pedido) {
                        prod_reastreado.value = response.pedido;
                    } else {
                        alertas.alertWarning(response.info);
                        limpiarCampo('tabla');
                    }
                }
                $('.overlay-spinner').hide();
            }
        );
    }

    // Proceso para cambio de formulario
    const activarAgregar = ref(true);
    const activarEditar = ref(false);
    const elementoActEdit = ref(true);
    const editar = ref(false);
    const v_estado = ref('D');
    const v_escogeEdicion = ref('0');
    const catalogo = ref({});
    const v_prod_select = ref({});
    const nombreLargo = ref(false);

    const cambioProceso = async (proceso) => {
        if (proceso == 'agregar') {
            activarAgregar.value = true;
            activarEditar.value = false;

            // Se vacian los campos del formulario
            editar.value = false;
            elementoActEdit.value = true;
            limpiarCampo('add');
        } else if (proceso == 'editar') {
            editar.value = true;
            elementoActEdit.value = false;
            activarAgregar.value = false;
            activarEditar.value = true;
            textoBoton.value = 'Editar producto';
            obtieneProductos();
        }
    };

    const obtieneProductos = async () => {
        $('.overlay-spinner').show();
        await getProductos(
            {'cambioTipo': 0, 'todos': true}
        ).then(
                (data) => {
                    catalogo.value = data.productos;
                }
            ).catch(error => {
                console.log("Error al obtener los datos: ", error);
                alertas.alertError('Error al obtener los datos');
            });

        $('.overlay-spinner').hide();
    }
    // Escucha cuando se elige el cambio a edición
    watch(() => v_escogeEdicion.value, (val) => {
        let arrCatalogo = catalogo.value;
        if (arrCatalogo.length > 0) {
            catalogo.value.forEach( function(element, index, array) {
                if (element.id == val) {
                    elementoActEdit.value = true;
                    v_prod_select.value = element;
                    v_producto.value = element.producto;
                    v_precio .value = String(element.precio).replace(',','.');
                    v_dimensiones .value = String(element.dimensiones).replace(',','.');
                    v_disponible.value = element.tipo_entrega;
                    v_inventario .value = String(element.inventario).replace(',','.');
                    v_comentario.value = element.comentario;
                    v_estado.value = element.estado;
                    return true;
                }
            });
        }
    });
    // Escucha el ingreso de datos al campo de nombre
    watch(() => v_producto.value, (val) => {
        if (val.length > 30) {
            nombreLargo.value = true;
        } else {
            nombreLargo.value = false;
        }
    });
    // Contruye la ruta de la imagen
    const rutaImagen = (urlRelativa) => {
        return `${API_BASE_URL}${urlRelativa}`;
    }

    // Función para limpiar los campos
    function limpiarCampo(section) {
        if (section == 'add') {
            v_producto.value = '';
            v_precio.value = '';
            v_dimensiones.value = '';
            v_disponible.value = 1;
            v_inventario.value = 0;
            v_comentario.value = '';
            archivoInput.value.value = '';
            if (elementoActEdit.value) {
                v_prod_select.value = '';
                v_escogeEdicion.value = 0;
            }
        } else if (section == 'tabla') {
            v_cve_busqueda.value = '';
            v_fech_busqueda.value = '';
            v_fech_busqueda_fin.value = '';
            prod_reastreado.value = [];
            sumaProdCantidad.value = {
                totalCosto: 0,
                totalCantidad: 0
            };
        } else if (section == 'busqueda') {
            prod_reastreado.value = [];
            sumaProdCantidad.value = {
                totalCosto: 0,
                totalCantidad: 0
            };
        }
    }
    // Función para agregar un nuevo producto
    async function nuevoProducto() {
        if (nombreLargo.value === true) {
            alertas.alertWarning('El nombre del producto es demasiado grande', false, 3000);
            return;
        }
        $('.overlay-spinner').show();
        const camposCompletos = ref(true);
        enviando.value = true;
        const producto = {
            "producto": v_producto.value,
            "precio": v_precio.value,
            "dimensiones": v_dimensiones.value,
            "tipo_entrega": v_disponible.value,
            "inventario": v_inventario.value,
            "comentario": v_comentario.value,
            "imagen": archivoInput.value.files[0]
        }
        // Control formulario
        if (producto['inventario'] <= 0 && producto['tipo_entrega'] == '') {
            producto['tipo_entrega'] = 2;
        }
        if (producto['inventario'] <= 0 && producto['tipo_entrega'] == 1) {
            camposCompletos.value = false;
            alertas.alertWarning(getErrorMessages(100), false, 2500);
            enviando.value = false;
            $('.overlay-spinner').hide();
        }
        if (producto['precio'] <= 0) {
            camposCompletos.value = false;
            alertas.alertWarning(getErrorMessages(102), false, 2500);
            enviando.value = false;
            $('.overlay-spinner').hide();
        }
        if (producto['dimensiones'] <= 0) {
            camposCompletos.value = false;
            alertas.alertWarning(getErrorMessages(103), false, 2500);
            enviando.value = false;
            $('.overlay-spinner').hide();
        }
        // Menejo de formulario, campos vacios
        $.each(producto, function (index, element) {
            // Campos requeridos
            let requeridos = ['precio', 'dimensiones', 'producto'];
            if (!editar.value) {
                requeridos.push('imagen');
            }
            if (requeridos.includes(index)) {
                if (element === undefined || element === '') {
                    camposCompletos.value = false;
                    alertas.alertWarning(getErrorMessages(101) + ` ${index}`, false);
                    enviando.value = false;
                    $('.overlay-spinner').hide();
                }
            }
        });
        // Entra si se valida que los campos viene completos
        if (camposCompletos.value) {
            if (editar.value) {
                producto['id'] = v_escogeEdicion.value;
                producto['estado'] = v_estado.value;
                editarProducto(producto).then(
                    (response) => {
                        if (response.error) {
                            alertas.alertError(response.error);
                        } else {
                            limpiarCampo('add');
                            elementoActEdit.value = false;
                            obtieneProductos();
                            alertas.alertSuccess(getErrorMessages(201));
                        }
                    }
                );
                obtieneProductos();
            } else {
                cargarProducto(producto).then(
                    (response) => {
                        if (response.error) {
                            alertas.alertError(response.error);
                        } else {
                            limpiarCampo('add');
                            alertas.alertSuccess(getErrorMessages(200));
                        }
                    }
                );
            }
        }
        enviando.value = false;
        $('.overlay-spinner').hide();
    }

    // Funciones para el filtrado de indicadores
    const v_filtro_indicador = ref('T');
    watch(() => v_filtro_indicador.value, (val) => {
        obtenerConteoVentas({'periodo': val});
    });
</script>

<style scoped>
    .btn {
        background-color: #B53471;
    }

    .btn:hover {
        background-color: #c56cf0;
    }

    .container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        padding-inline: 4rem;
        background-color: rgba(238, 247, 255, 0.705);
    }

    .line_horizontal {
        height: 2px;
        margin-top: 1rem;
        background-color: rgba(0, 0, 0, 0.185);
    }

    .line_vertical {
        display: inline-block;
        width: 2px;
        margin-top: 1rem;
        background-color: rgba(0, 0, 0, 0.185);
        padding: 0;
        vertical-align: middle;
    }

    .required {
        color: red;
        margin-left: 2px;
    }

    #fTotales td{
        background: #b5347050 !important;
        font-weight: bold;
    }

    #ventasCompletas,
    #ventasCanceladas,
    #masSolicitados {
        font-weight: bold;
    }

    #ventasCompletas {
        background-color: #b5347050;
    }

    #icon-cash,
    #icon-cancel,
    #icon-top {
        padding: 7px;
        position: absolute;
        top: 3rem;
        left: 18rem;
    }

    #icon-cash svg,
    #icon-cancel svg,
    #icon-top svg {
        opacity: 0.5;
    }

    .fondoFinaliado {
        background-color: rgb(0, 126, 0);
    }

    .fondoEnProceso {
        background-color: rgb(51, 134, 228);
    }

    .fondoCancelada {
        background-color: rgb(158, 18, 18);
    }

    .ocultarFormulario {
        display: none;
    }

    .btnOpacity {
        opacity: 0.5;
    }

    .img_ref_edit {
        max-width: 30%;
        border-radius: 15px;
    }

    .borderRed {
        border: 1px solid red;
    }

    #msgNombre {
        position: absolute;
        top: -2rem;
        left: 15rem;
        color: red;
    }

    /** media */
    @media (max-width: 1400px) {
        #icon-cash,
        #icon-cancel,
        #icon-top {
            left: 15rem !important;
        }
    }

    @media (max-width: 1200px) {
        #icon-cash,
        #icon-cancel,
        #icon-top {
            left: 12.5rem !important;
        }

        #addProd {
            font-size: 12px;
        }
    }

    @media (max-width: 990px) {
        .line_vertical {
            visibility: hidden;
        }
    }

    @media (min-width: 768px) and (max-width: 990px) {
        #icon-cash,
        #icon-cancel,
        #icon-top {
            left: 33rem !important;
        }
    }

    @media (min-width: 500px) and (max-width: 766px) {
        #icon-cash,
        #icon-cancel,
        #icon-top {
            left: 18rem !important;
        }

        .container {
            padding-inline: 0.5rem;
        }
    }

    @media (min-width: 430px) and (max-width: 500px) {
        #icon-cash,
        #icon-cancel,
        #icon-top {
            left: 15rem !important;
        }

        #filtroIndicadores {
            max-width: 100%;
        }

        .container {
            padding-inline: 0.5rem;
        }
    }

    @media (min-width: 381px) and (max-width: 429px) {
        .container {
            padding-inline: 0.5rem;
        }
    }

    @media (max-width: 380px) {
        #icon-cash,
        #icon-cancel,
        #icon-top {
            top: 4rem;
            left: 11rem !important;
        }

        .container {
            padding-inline: 0.5rem;
        }

        .img_ref_edit {
            max-width: 50%;
        }

        #filtroIndicadores {
            max-width: 100%;
        }
    }

</style>