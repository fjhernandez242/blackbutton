<template>
    <section>
        <div class="container">
            <h4><b>Buscar pedido</b></h4>
            <div class="card w-60">
                <div class="card-body">
                     <form class="row g-3 needs-validation" novalidate>
                        <div class="col-md-4">
                            <label for="cve_pedido" class="form-label">Clave de pedido</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text"><i class="bi bi-search"></i></span>
                                <input type="text" class="form-control limpiarCampo" name="cve_pedido" id="cve_pedido"
                                    v-model="v_producto" placeholder="ingresa la clave depedido" required>
                            </div>
                        </div>
                        <div class="col-md-1 d-flex justify-content-center align-items-center pt-2">
                            <button type="submit" class="btn" :disabled="enviando">
                                Rastrear
                            </button>
                        </div>
                     </form>
                </div>
            </div>
            <p class="line"></p>
            <h4><b>Agrega un Amigurumi</b></h4>
            <div class="card w-60">
                <div class="card-body">
                    <form @submit.prevent="nuevoProducto" class="row g-3 needs-validation" novalidate>
                        <div class="col-md-6">
                            <label for="producto" class="form-label">¿Qué nombre le pondrás?</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text"><i class="bi bi-pen"></i></span>
                                <input type="text" class="form-control limpiarCampo" name="producto" id="producto"
                                    v-model="v_producto" placeholder="Nombre" required>
                                <div class="invalid-feedback">
                                Por favor indica su nombre!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <label for="precio" class="form-label">¿Qué valor le colocaras?</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text">$</span>
                                <input type="number" step="any" class="form-control limpiarCampo" name="precio" id="precio"
                                v-model="v_precio" placeholder="0" required>
                                <div class="invalid-feedback">
                                Por favor indique el precio!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <label for="inventario" class="form-label">¿Cuántos hay en existencia?</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text"><i class="bi bi-box-seam-fill"></i></span>
                                <input type="number" class="form-control limpiarCampo" name="inventario" id="inventario"
                                v-model="v_inventario" placeholder="0" required>
                                <div class="invalid-feedback">
                                Por favor indique la cantidad en existencia!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <label for="dimensiones" class="form-label">¿Cuál es su medida en cm?</label>
                            <div class="input-group md-3">
                                <span class="input-group-text"><i class="bi bi-rulers"></i></span>
                                <input type="number" step="any" class="form-control limpiarCampo" name="dimensiones"
                                    id="dimensiones" v-model="v_dimensiones" placeholder="Medida" required>
                                <div class="invalid-feedback">
                                Por favor indique las dimensiones!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <label for="tipo_entrega" class="form-label">Tipo de Entrega</label>
                            <div class="input-group md-3">
                                <span class="input-group-text"><i class="bi bi-cart-fill"></i></span>
                                <select class="form-select limpiarCampo" name="tipo_entrega" id="tipo_entrega"
                                    v-model="v_disponible" required>
                                    <option value="" selected disabled>- Indica el tipo de entrega -</option>
                                    <option value="1">Entrega Inmediata</option>
                                    <option value="2">Sobre pedido</option>
                                </select>
                                <div class="invalid-feedback">
                                Por favor indique el tipo de entrega!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <label for="img_ref" class="form-label">Muestra su mejor foto</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text"><i class="bi bi-card-image"></i></span>
                                <input type="file" id="img_ref" class="form-control limpiarCampo" ref="archivoInput">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <label for="comentario" class="form-label">Agrega un comentario</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text"><i class="bi bi-chat-dots-fill"></i></span>
                                <textarea id="comentario" class="form-control limpiarCampo" v-model="v_comentario"
                                placeholder="Comentario"></textarea>
                            </div>
                        </div>
                        <div class="col-md-10"></div>
                        <div class="col-md-2 d-flex btn-group">
                            <button type="submit" class="btn" :disabled="enviando">
                                {{ enviando ? 'Cargando...' : textoBoton }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>

    import { ref } from 'vue';
    import { cargarProducto } from '@/services/catalogo-services';
    // Importa script para notificaciones SweetAlert2
    import alertas from '@/assets/js/notifications';
    // Importa archivo de errores
    import { getErrorMessages } from '@/assets/errorMessages';

    const v_producto = defineModel('producto');
    const v_precio = defineModel('precio');
    const v_dimensiones = defineModel('dimensiones');
    const v_disponible = ref("");
    const v_inventario = defineModel('invetnario');
    const v_comentario = defineModel('comentario');

    const archivoInput = ref(null);
    const enviando = ref(false);
    // Variable para texto de botón
    const textoBoton = ref('Cargar producto');


    async function nuevoProducto() {
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
        if (v_inventario.value <= 0 && v_disponible.value == 1) {
            camposCompletos.value = false;
            alertas.alertWarning(getErrorMessages(100), false, 2500);
            enviando.value = false;
        }
        // Menejo de formulario, campos vacios
        $.each(producto, function (index, element) {
            // Campos requeridos
            if ((element == undefined && index != 'comentario') || element == '') {
                camposCompletos.value = false;
                alertas.alertWarning(getErrorMessages(101), false);
                enviando.value = false;
            }
        });
        // Entra si se valida que los campos viene completos
        if (camposCompletos.value) {
            cargarProducto(producto).then(
                (response) => {
                    if (response.error) {
                        alertas.alertError(response.error);
                        enviando.value = true;
                    } else {
                        enviando.value = false;
                        limpiarCampo();
                        alertas.alertSuccess(getErrorMessages(200));
                    }
                }
            );
        }
    }
    // Función para limpiar los campos
    function limpiarCampo() {
        v_producto.value = '';
        v_precio.value = '';
        v_dimensiones.value = '';
        v_disponible.value = 1;
        v_inventario.value = 0;
        v_comentario.value = '';
        archivoInput.value.value = '';
    }
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

    .line {
        height: 2px;
        margin-top: 1rem;
        background-color: rgba(0, 0, 0, 0.185);
    }
</style>