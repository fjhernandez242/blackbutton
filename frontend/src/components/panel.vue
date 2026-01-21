<template>
    <section>
        <div class="container">
            <div class="card w-60">
                <div class="card-body">
                    <form @submit.prevent="nuevoProducto" class="row g-3 needs-validation" novalidate>
                        <div class="col-md-12">
                            <h4>Agrega un Amigurumi</h4>
                        </div>
                        <div class="col-md-6">
                            <label for="producto" class="form-label">¿Qué nombre le pondrás?</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text"><i class="bi bi-pen"></i></span>
                                <input type="text" class="form-control limpiarCampo" name="producto" id="producto"
                                    v-model="v_producto" required>
                                <div class="invalid-feedback">
                                Por favor indica su nombre!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <label for="precio" class="form-label">¿Qué valor le colocaras?</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text">$</span>
                                <input type="text" class="form-control limpiarCampo" name="precio" id="precio"
                                v-model="v_precio" required>
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
                                v-model="v_inventario" required>
                                <div class="invalid-feedback">
                                Por favor indique la cantidad en existencia!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <label for="dimensiones" class="form-label">¿Cuál es su medida?</label>
                            <div class="input-group md-3">
                                <span class="input-group-text"><i class="bi bi-rulers"></i></span>
                                <input type="text" class="form-control limpiarCampo" name="dimensiones" id="dimensiones"
                                    v-model="v_dimensiones" required>
                                <div class="invalid-feedback">
                                Por favor indique las dimensiones!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <label for="disponibilidad" class="form-label">Disponibilidad</label>
                            <div class="input-group md-3">
                                <span class="input-group-text"><i class="bi bi-cart-fill"></i></span>
                                <select class="form-select limpiarCampo" name="disponibilidad" id="disponibilidad"
                                    v-model="v_disponible" required>
                                    <option selected>- Indica la disponibilidad -</option>
                                    <option value="1">Entrega Inmediata</option>
                                    <option value="2">Sobre pedido</option>
                                </select>
                                <div class="invalid-feedback">
                                Por favor indique la disponibilidad!
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
                                <textarea id="comentario" class="form-control limpiarCampo" v-model="v_comentario"></textarea>
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

    const v_producto = defineModel('producto');
    const v_precio = defineModel('precio');
    const v_dimensiones = defineModel('dimensiones');
    const v_disponible = defineModel('disponibilidad');
    const v_inventario = defineModel('inventario');
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
            "disponibilidad": v_disponible.value,
            "inventario": v_inventario.value,
            "comentario": v_comentario.value,
            "imagen": archivoInput.value.files[0]
        }
        $.each(producto, function (index, element) {
            if (element == undefined) {
                camposCompletos.value = false;
                alertas.alertWarning('Campos faltantes');
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
                        alertas.alertSuccess('¡Producto agregado!');
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
    section {
        margin-top: 4rem;
    }
    .btn {
        background-color: #B53471;
    }

    .btn:hover {
        background-color: #c56cf0;
    }
</style>