<template>
    <Transition name="fade-slide">
        <div v-if="props.visible" class="modal" id="trabajoModal" tabindex="-1" aria-labelledby="trabajoModalLabel"
            style="display: block;" aria-modal="true" role="dialog">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content h-50">
                    <div class="modal-body">
                        <div class="d-flex justify-content-end pb-2">
                            <button type="button" class="btn-close" @click="modalClose()" aria-label="Close"></button>
                        </div>
                        <div class="row">
                            <h4 class="text-center" id="pedido_success">
                                Casí listo, solo queda un último paso.
                            </h4>
                            <div class="col-sm-6">
                                <div class="card h-100 shadow-sm cardinfo">
                                    <div class="card-body d-flex flex-column" style="overflow-y: auto;">
                                        <div class="mt-4">
                                            <h4 class="text-center"><b>¿Cómo finalizo mi pedido?</b></h4>
                                            <ul class="list-group list-group-flush" style="border-radius: 15px;">
                                                <li class="list-group-item">
                                                    <p><b>Opción 1</b></p>
                                                    <div class="row">
                                                        <div class="d-flex align-items-center">
                                                            <small>
                                                                Enviar de forma directa por WhatsApp.
                                                            </small>
                                                        </div>
                                                    </div>
                                                    <div class="row d-flex justify-content-center">
                                                        <a @click="enviarPedido('whatsapp')" class="btn btn-sm" id="btn_pedido_whatsapp">
                                                            <span class="me-2">Enviar por WhatsApp</span>
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-whatsapp" viewBox="0 0 16 16">
                                                                <path d="M13.601 2.326A7.85 7.85 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.9 7.9 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.9 7.9 0 0 0 13.6 2.326zM7.994 14.521a6.6 6.6 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.56 6.56 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592m3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.73.73 0 0 0-.529.247c-.182.198-.691.677-.691 1.654s.71 1.916.81 2.049c.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232"/>
                                                            </svg>
                                                        </a>
                                                    </div>
                                                </li>
                                                <li class="list-group-item">
                                                    <p><b>Opción 2</b></p>
                                                    <div class="row">
                                                        <div class="d-flex justify-content-center">
                                                            <small>
                                                                Puedes copiar el ticket y enviarlo por la página oficial de
                                                                BlackButton.
                                                            </small>
                                                        </div>
                                                    </div>
                                                    <div class="row d-flex justify-content-center">
                                                        <a @click="enviarPedido('facebook')" href="https://www.facebook.com/share/1CS1VTt2wB/" target="_blank" class="btn btn-sm" id="btn_pedido_face">
                                                            <span class="me-2">Enviar por Facebook</span>
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-facebook" viewBox="0 0 16 16">
                                                                <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"/>
                                                            </svg>
                                                        </a>
                                                    </div>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-sm-6">
                                <div class="card h-100 shadow-sm cardinfo">
                                    <div class="card-body">
                                        <div class="mt-3">
                                            <h4 class="text-center">Ticket</h4>
                                            <ul class="list-group list-group-flush">
                                                <li class="list-group-item d-flex">
                                                    <small class="mx-auto" style="white-space: pre-wrap;">{{ props.ticket }}</small>
                                                </li>
                                                <button
                                                @click="copiarAlPortapapeles"
                                                class="btn btn-sm mt-2"
                                                :class="copiado ? 'btn-success' : 'btn-outline-primary'">
                                                    <span v-if="copiado">¡Copiado al portapapeles!</span>
                                                    <span v-else>Copiar ticket</span>
                                                </button>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
    import { ref } from 'vue';
    import { useCartStore } from '@/store/cartStore';
    import { sendMessage } from '@/services/email-services';
    import { agregarPedido } from '@/services/catalogo-services';
    const cartStore = useCartStore();
    // Define emits
    const emit = defineEmits(['cerrar-modal']);
    const props = defineProps({
        visible: {
            type: Boolean,
            default: false
        },
        ticket: {
            type: String,
            default: false
        },
        codigo: {
            type: String,
            default: false
        }
    });

    function modalClose() {
        // cerrarmodal();
        emit('cerrar-modal');
    }
    // Estado para cambiar el texto del botón temporalmente
    const copiado = ref(false);
    const copiarAlPortapapeles = async () => {
        try {
            await navigator.clipboard.writeText(props.ticket);

            // Se cambia el estado a verdadedo
            copiado.value = true;

            // Regresamos el botón a su estado original despés de 2 segundos
            setTimeout(() => {
                copiado.value = false;
            }, 2000);
        } catch (err) {
            console.error('Error al copiar el texto: ', err);
        }
    };

    // Función para envio por WhatsApp
    const enviarPedido = async (redSocial) => {
        if (redSocial == 'whatsapp') {
            // Llama la función para envio de mensaje por WhatsApp
            sendMessage(props.ticket, false, true);
        }
        const data = cartStore.items;
        for(const value of data) {
                value.pedido = props.codigo;
                try {
                    const response = await agregarPedido(value, cartStore.expiracion.id_temp);
                    if (response.error) {
                        alertas.alertError(response.error);
                        break;
                    } else {
                        $('#temp_offcanvas').fadeOut();
                        $('#temporizador').fadeOut();
                        cartStore.detenerTemporizador(false, true);
                        cartStore.recargaCatalogo();
                        setTimeout(() => location.reload(), 1000);
                    }
                } catch (err) {
                    console.error("Error en la petición: ", err);
                    break;
                }
            };
    };
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

    .cardinfo {
        width: 100%;
        height: 200px;
        overflow: hidden;
        background-color: rgb(238, 247, 255);
        border-radius: 10px;
        border: none;
        display: flex;
        align-items: center;
    }

    .ocultarElemento {
        visibility: hidden;
    }

    #btn_pedido_whatsapp {
        margin-top: 1rem;
        max-width: 80%;
        color: #128c7e;
        border: 1px solid #128c7e;
    }

    #btn_pedido_whatsapp:hover {
        background-color: #128c7e;
        color: white;
    }

    #btn_pedido_whatsapp:hover icon {
        color: white;
    }

    #btn_pedido_face {
        margin-top: 1rem;
        max-width: 80%;
        border: 1px solid #3b5998;
        color: #3b5998;
    }

    #btn_pedido_face:hover {
        background-color: #3b5998;
        color: white;
    }

    #btn_pedido_face:hover icon {
        color: white;
    }

    #pedido_success {
        margin-bottom: 1rem;
        box-shadow: 0 0 0.4em #B53471;
    }
</style>