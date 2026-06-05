<template>
    <Transition name="fade-slide">
        <div v-if="props.visible" class="modal" id="trabajoModal" tabindex="-1" aria-labelledby="trabajoModalLabel"
            style="display: block;" aria-modal="true" role="dialog">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content h-50">
                    <div class="modal-body">
                        <div class="d-flex justify-content-end pb-2">
                            <button type="button" class="btn-close" @click="modalClose()" aria-label="Close"></button>
                        </div>
                        <div class="card h-100 shadow-sm" id="cardinfo">
                            <div class="card-body d-flex flex-column" style="overflow-y: auto;">
                                <h4 class="text-center">Recuperación de contraseña</h4>
                                <form action="">
                                    <div class="mb-3 row">
                                        <label for="staticEmail" class="col-lg-12 col-md-10 col-sm-8 col-form-label">Ingresa el código que fue enviado a tu correo electrónico.</label>
                                    </div>
                                    <div class="mb-3 row">
                                        <label for="inputPassword" class="form-label">Código</label>
                                        <div class="col-lg-6">
                                            <input type="text" class="form-control" id="inputPassword">
                                        </div>
                                        <div class="col-lg-6 d-flex justify-content-center align-items-center">
                                            <div id="btn_pedido">
                                                <button class="btn btn-sm">Restablecer</button>
                                                <button class="btn btn-sm">Cancelar</button>
                                            </div>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
    import { useCartStore } from '@/store/cartStore';
    const cartStore = useCartStore();
    const nombre = defineModel('nombre');
    // Define emits
    const emit = defineEmits(['cerrar-modal']);
    const props = defineProps({
        visible: {
            type: Boolean,
            default: false
        }
    });
    function modalClose() {
        // cerrarmodal();
        emit('cerrar-modal');
    }
</script>

<style scoped>
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
    #cardinfo {
        width: 100%;
        height: 200px;
        overflow: hidden;
        background-color: rgb(238, 247, 255);
        border-radius: 10px;
        border: none;
    }

    #btn_pedido button {
        background-color: #B53471;
        margin-inline: 2px;
    }

    #btn_pedido button:hover {
        background-color: #c56cf0;
    }
</style>