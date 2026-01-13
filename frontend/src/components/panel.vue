<template>
    <section>
        <div class="container">
            <div class="card w-60">
                <div class="card-body">
                    <form @submit.prevent="nuevoProducto" class="row g-3 needs-validation" novalidate>
                        <div class="col-md-6">
                            <label for="producto" class="form-label">Nombre del producto</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text"><i class="bi bi-pen"></i></span>
                                <input type="text" class="form-control limpiarCampo" name="producto" id="producto"
                                    v-model="v_producto" required>
                                <div class="invalid-feedback">
                                Por favor indique el producto!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <label for="precio" class="form-label">Precio del producto</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text">$</span>
                                <input type="text" class="form-control limpiarCampo" name="precio" id="precio"
                                v-model="v_precio" required>
                                <div class="invalid-feedback">
                                Por favor indique el precio!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <label for="dimensiones" class="form-label">Dimensiones del producto</label>
                            <div class="input-group md-3">
                                <span class="input-group-text"><i class="bi bi-rulers"></i></span>
                                <input type="text" class="form-control limpiarCampo" name="dimensiones" id="dimensiones"
                                    v-model="v_dimensiones" required>
                                <div class="invalid-feedback">
                                Por favor indique las dimensiones!
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <label for="img_ref" class="form-label">Imagen</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text"><i class="bi bi-card-image"></i></span>
                                <input type="file" id="img_ref" class="form-control limpiarCampo" ref="archivoInput">
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

    const archivoInput = ref(null);
    const enviando = ref(false);
    // Variable para texto de botón
    const textoBoton = ref('Cargar producto');

    async function nuevoProducto() {
        enviando.value = true;

        const producto = {
            "producto": v_producto.value,
            "precio": v_precio.value,
            "dimensiones": v_dimensiones.value,
            "imagen": archivoInput.value.files[0]
        }
        cargarProducto(producto).then(
            (response) => {
                if (response.error) {
                    alertas.alertError('Error al cargar producto');
                } else {
                    enviando.value = false;
                    alertas.alertSuccess('¡Producto agregado!');
                }
            }
        );
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