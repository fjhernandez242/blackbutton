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
                        <div class="row" v-if="!pedidoExitoso">
                            <h2 class="text-center" id="pedido_success">
                                ¡Casí listo!
                            </h2>
                            <div class="col-sm-6">
                                <div class="card h-100 shadow-sm cardinfo">
                                    <div class="card-body">
                                        <div class="mt-3">
                                            <h4 class="text-center"><b>Ticket</b></h4>
                                            <ul class="list-group list-group-flush">
                                                <li class="list-group-item d-flex" style="border-radius: 15px;">
                                                    <small class="mx-auto" style="white-space: pre-wrap;">{{ props.ticket }}</small>
                                                </li>
                                            </ul>
                                            <ul class="list-group list-group-flush">
                                                <span id="nota_pedido"><b>Nota:</b> El envío es gratis en pedidos mayores a $700.</span>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-sm-6">
                                <div class="card h-100 shadow-sm cardinfo">
                                    <div class="card-body d-flex flex-column" style="overflow-y: auto;">
                                        <div class="mt-4">
                                            <h4 class="text-center"><b>¿Cómo finalizo mi pedido?</b></h4>
                                            <h6 class="text-start pt-2"><b>Selecciona la forma de envio</b></h6>
                                            <ul class="list-group list-group-flush" style="border-radius: 15px;">
                                                <li class="list-group-item">
                                                    <p><b>Opción 1</b></p>
                                                    <div class="row">
                                                        <div class="d-flex align-items-center">
                                                            <small>
                                                                Te redirigiremos a WhatsApp con tu mensaje listo. Por seguridad, también copiamos
                                                                el ticket a tu portapapeles por si necesitas pegarlo manualmente.
                                                            </small>
                                                        </div>
                                                    </div>
                                                    <div class="row m-2">
                                                        <div class="form-check form-check-inline">
                                                            <input class="form-check-input" type="radio" name="inlineRadioOptions"
                                                                id="inlineRadio1" value="whatsapp" v-model="v_modoenvio">
                                                            <label class="form-check-label" for="inlineRadio1" id="btn_pedido_whatsapp">
                                                                <span class="me-2">Enviar por WhatsApp</span>
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-whatsapp" viewBox="0 0 16 16">
                                                                    <path d="M13.601 2.326A7.85 7.85 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.9 7.9 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.9 7.9 0 0 0 13.6 2.326zM7.994 14.521a6.6 6.6 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.56 6.56 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592m3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.73.73 0 0 0-.529.247c-.182.198-.691.677-.691 1.654s.71 1.916.81 2.049c.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232"/>
                                                                </svg>
                                                            </label>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li class="list-group-item">
                                                    <p><b>Opción 2</b></p>
                                                    <div class="row">
                                                        <div class="d-flex justify-content-center">
                                                            <small>
                                                                Copiamos el ticket a tu portapapeles. Te redirigiremos a chat de Messenger de la página oficial de BlackButton,
                                                                para que puedas simplemente pegar tu pedido.
                                                            </small>
                                                        </div>
                                                    </div>
                                                    <div class="row m-2">
                                                        <div class="form-check form-check-inline">
                                                            <input class="form-check-input" type="radio" name="inlineRadioOptions"
                                                                id="inlineRadio2" value="facebook" v-model="v_modoenvio">
                                                            <label class="form-check-label" for="inlineRadio2" id="btn_pedido_face">
                                                                <span class="me-2">Enviar por Facebook</span>
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-facebook" viewBox="0 0 16 16">
                                                                    <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"/>
                                                                </svg>
                                                            </label>
                                                        </div>
                                                    </div>
                                                </li>
                                                <span class="text-center pt-2"
                                                    style="color: red;"
                                                    v-if="!envioseleccionado">Selecciona una opción de envio</span>
                                                <button id="btn_envio"
                                                class="btn_action mt-2"
                                                @click="enviarPedido()">Enviar pedido</button>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row" v-else>
                            <h2 class="text-center" id="pedido_success">
                                ¡Pedido realizado con exito!
                            </h2>
                            <div class="col-sm-6">
                                <div class="card h-100 shadow-sm cardinfo">
                                    <div class="card-body d-flex flex-column" style="overflow-y: auto;">
                                        <div class="mt-4">
                                            <h4 class="text-center"><b>¿No pudiste enviar el ticket en el paso anterior?</b></h4>
                                            <h6 class="text-start pt-2"><b>Sigue los siguientes pasos</b></h6>
                                            <ul class="list-group list-group-flush" style="border-radius: 15px;">
                                                <li class="list-group-item">
                                                    <div class="row">
                                                        <div class="d-flex justify-content-center">
                                                            <ol class="list-group list-group-numbered">
                                                                <li class="list-group-item" style="border-radius: 15px;">
                                                                    <small>
                                                                        Revisa que el ticket esté en tu portapeletes, o vuelve a copiarlo en la sección de <b>Ticket</b>.
                                                                    </small>
                                                                </li>
                                                                <li class="list-group-item mt-2" style="border-radius: 15px;">
                                                                    <small>
                                                                        Ve a la página oficial de Black Button en Facebook, inicia un chat con la vendedora,
                                                                        pega y envía el ticket que ya copiaste anteriormente.
                                                                    </small>
                                                                    <div class="m-2 d-flex justify-content-center">
                                                                        <a href="https://www.facebook.com/share/1CS1VTt2wB/" target="_blank" class="form-check-label" for="inlineRadio2" id="btn_pedido_face">
                                                                            <span class="me-2">BlackButton</span>
                                                                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-facebook" viewBox="0 0 16 16">
                                                                                <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"/>
                                                                            </svg>
                                                                        </a>
                                                                    </div>
                                                                </li>
                                                            </ol>
                                                        </div>
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
                                            <h4 class="text-center"><b>Ticket</b></h4>
                                            <ul class="list-group list-group-flush">
                                                <li class="list-group-item d-flex" style="border-radius: 15px;">
                                                    <small class="mx-auto" style="white-space: pre-wrap;">{{ props.ticket }}</small>
                                                </li>
                                                <button id="btn_envio"
                                                    class="mt-2"
                                                    :class="[copiado == true ? 'btn btn-success' : 'btn_action']"
                                                    @click="copiarAlPortapapeles(true)">
                                                    <span v-if="!copiado">Copiar ticket <i class="bi bi-clipboard"></i></span>
                                                    <span v-else>Ticket copiado <i class="bi bi-clipboard-check"></i></span>
                                                </button>
                                            </ul>
                                            <ul class="list-group list-group-flush">
                                                <span id="nota_pedido"><b>Nota:</b> El envío es gratis en pedidos mayores a $700.</span>
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
    import { ref, watch } from 'vue';
    import { useCartStore } from '@/store/cartStore';
    import { sendMessage } from '@/services/email-services';
    import { agregarPedido } from '@/services/catalogo-services';
    import alertas from '@/assets/js/notifications';
    const cartStore = useCartStore();
    const pedidoExitoso = ref(false);
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
        if (pedidoExitoso.value) {
            location.reload();
        } else {
            // cerrarmodal();
            emit('cerrar-modal');
        }
    }
    // Estado para cambiar el texto del botón temporalmente
    const copiado = ref(false);
    const copiarAlPortapapeles = async (forBtn = false) => {
        try {
            await navigator.clipboard.writeText(props.ticket);
            if (forBtn) {
                copiado.value = true;
                setTimeout(() => copiado.value = false, 1500);
            }
        } catch (err) {
            console.error('Error al copiar el texto: ', err);
        }
    };
    const v_modoenvio = ref('')
    const envioseleccionado = ref(true);
    // Escucha cuando se selecciona una forma de envio
    watch(() => v_modoenvio.value, (val) => {
        if (val !== '') {
            envioseleccionado.value = true;
        }
    });
    // Función para envio por WhatsApp
    const enviarPedido = async () => {
        if (v_modoenvio.value === '') {
            envioseleccionado.value = false;
            return;
        }
        // Copia el ticket al portapapeles
        await copiarAlPortapapeles();
        // Se crea la ventana vacía inmediatamente al clic
        const nuevaVentana = window.open('','_blank');
        try {
            // Se llama la función de copiar a portapapeles si esta no ha sido accionada
            const data = cartStore.items;
            const response = await agregarPedido(data, cartStore.expiracion.id_temp, props.codigo);
            if (response.error) {
                alertas.alertError(response.error);
            } else {
                if (v_modoenvio.value == 'whatsapp') {
                    // Llama la función para envio de mensaje por WhatsApp
                    const urlWharsapp = sendMessage(props.ticket, false, true);
                    nuevaVentana.location.href = urlWharsapp;
                } else if (v_modoenvio.value == 'facebook') {
                    // nuevaVentana.location.href = "https://www.facebook.com/share/1CS1VTt2wB/";
                    nuevaVentana.location.href = "https://m.me/BlackButtonn";
                }
                // Detenemos el temporizador que pueda haber
                $('#temp_offcanvas').fadeOut();
                $('#temporizador').fadeOut();
                cartStore.detenerTemporizador(false, true);
                cartStore.recargaCatalogo();
                // Marcamos el pedido como correcto
                pedidoExitoso.value = true;
                // setTimeout(() => location.reload(), 1000);
            }
        } catch (err) {
            console.error("Error en la petición: ", err);
        }
    };
    // Función para dar aviso de un pedido completo y mantener el ticket activo hasta carga
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
        max-width: 80%;
        color: #128c7e;
    }

    #btn_pedido_face {
        max-width: 80%;
        color: #3b5998;
    }

    #pedido_success {
        margin-bottom: 1rem;
        box-shadow: 0 0 0.4em #B53471;
        border-radius: 5px;
    }

    .btn_action {
        border: 1px solid #B53471;
        color: #B53471;
        border-radius: 5px;
        padding: 6.7px;
        font-size: 15px;
        background-color: transparent;
    }

    .btn_action:hover {
        background-color: #B53471;
        color: white;
    }

    #nota_pedido {
        opacity: 0.8;
        margin-top: 1rem;
    }

    .btn-close {
        background-color: red;
        border-radius: 100%;
    }

    @media (max-width: 380px) {
        #btn_pedido_whatsapp {
            max-width: 100%;
        }

        #btn_pedido_face {
            max-width: 100%;
        }
    }
</style>