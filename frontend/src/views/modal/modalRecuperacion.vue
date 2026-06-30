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
                                <h4 class="text-center">Restablecer contraseña</h4>
                                <div v-if="!mostrarFormRecup">
                                    <form @submit.prevent="validarCodigo" novalidate>
                                        <div class="mb-3 row text-center">
                                            <label for="staticEmail" class="col-lg-12 col-md-10 col-sm-8 col-form-label">
                                                El código fue enviado a tu correo electrónico. El código es valido por 5 minutos</label>
                                        </div>
                                        <div class="mb-1 row text-center" v-if="faltaCodigo">
                                            <label for="staticEmail" style="color: red;" class="col-lg-12 col-md-10 col-sm-8 col-form-label">
                                                Debes ingresar el código de verificación.</label>
                                        </div>
                                        <div class="mb-1 row text-center" v-if="codigoCorrecto">
                                            <label for="staticEmail" style="color: green;" class="col-lg-12 col-md-10 col-sm-8 col-form-label">
                                                Código de verificación correcto.</label>
                                        </div>
                                        <div class="mb-3 row d-flex justify-content-center aling-items-center">
                                            <div class="col-lg-7 mb-3">
                                                <div class="input-group flex-nowrap">
                                                    <span class="input-group-text" id="code_restart"><i class="bi bi-key"></i></span>
                                                    <input type="text" class="form-control" placeholder="0 0 0 0 0 0" aria-label="code"
                                                    aria-describedby="addon-wrapping"
                                                    v-model="v_code"
                                                    :class="[faltaCodigo ? 'inputCodeBad' : [codigoCorrecto ? 'inputCodeGood' : '']]">
                                                </div>
                                            </div>
                                            <div class="col-lg-12 d-flex justify-content-center align-items-center">
                                                <div class="btn-group" role="group"  id="btn_pedido">
                                                    <button type="submit" class="btn btn-sm">Restablecer</button>
                                                    <button type="button" class="btn btn-sm" @click="reenviarCodigo()">Reenviar código</button>
                                                </div>
                                            </div>
                                        </div>
                                    </form>
                                    <div class="row">
                                        <span class="text-center">Recuerda revisar la bandeja de spam.</span>
                                    </div>
                                </div>
                                <div v-else>
                                    <form @submit.prevent="restartPass" novalidate>
                                        <div class="mb-3 row text-center">
                                            <label for="staticEmail" class="col-lg-12 col-md-10 col-sm-8 col-form-label">
                                                Ingresa tu nueva contraseña.</label>
                                        </div>
                                        <div class="mb-1 row text-center" v-if="faltaContrasena">
                                            <label for="staticEmail" style="color: red;" class="col-lg-12 col-md-10 col-sm-8 col-form-label">
                                                {{ msgError }}</label>
                                        </div>
                                        <div class="form-floating mb-3">
                                            <input type="password" class="form-control dataInput" id="floatingInput" placeholder="Contraseña"
                                                v-model="v_nPass1">
                                            <label for="floatingInput">Nueva contraseña</label>
                                        </div>
                                        <div class="form-floating">
                                            <input type="password" class="form-control dataInput" id="floatingInput" placeholder="Contraseña"
                                                v-model="v_nPass2">
                                            <label for="floatingInput">Ingresa la contraseña de nuevo</label>
                                        </div>
                                        <div class="col-lg-12 d-flex justify-content-center align-items-center mt-3">
                                            <div class="btn-group" role="group"  id="btn_pedido">
                                                <button type="submit" class="btn btn-sm">Cambiar contraseña</button>
                                                <button type="button" @click="togglePassword()" class="btn btn-sm">
                                                    <span v-if="btnInput">Ocultar contraseñas <i class="bi bi-eye-slash"></i></span>
                                                    <span v-else>Mostrar contraseñas <i class="bi bi-eye"></i></span>
                                                </button>
                                            </div>
                                        </div>
                                    </form>
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
    import { validarCodigoRecuperacion, cambiarContrasena, enviarCodigo, cerrarSesion } from '@/services/usuario-services';
    import alertas from '@/assets/js/notifications';
    const v_code = ref('');
    const faltaCodigo = ref(false)
    const codigoCorrecto = ref(false)
    const mostrarFormRecup = ref(false);
    const btnInput = ref(false);
    const msgError = ref('');
    // Define emits
    const emit = defineEmits(['cerrar-modal']);
    const props = defineProps({
        visible: {
            type: Boolean,
            default: false
        }
    });
    function modalClose() {
        emit('cerrar-modal');
    }

    async function validarCodigo() {
        $('.overlay-spinner').show();
        try {
            if (v_code.value == '') {
                faltaCodigo.value = true;
                $('.overlay-spinner').hide();
                return;
            }
            await validarCodigoRecuperacion({
                'codigo': v_code.value
            }).then(
                (response) => {
                    if (response.error) {
                        $('.overlay-spinner').hide();
                        limpiarCampo();
                        if (response.mensaje == 'expirado') {
                            alertas.alertError(response.error);
                            setTimeout(() => modalClose(), 1000);
                        } else if (response.mensaje == 'inexistente') {
                            console.log('entra');
                            alertas.alertError(response.error);
                            return;
                        }
                    } else {
                        faltaCodigo.value = false;
                        codigoCorrecto.value = true;
                        $('.overlay-spinner').hide();
                        setTimeout(() => mostrarFormRecup.value = true, 1000);
                    }
                }
            );
        } catch (error) {
            $('.overlay-spinner').hide();
            console.log(error);
        }
    }

    // Variables para cambio de contraseña
    const faltaContrasena = ref(false);
    const v_nPass1 = ref('');
    const v_nPass2 = ref('');

    async function restartPass() {
        $('.overlay-spinner').show();
        if (v_nPass1.value == '' || v_nPass2.value == '') {
            msgError.value = 'Debes completar los campos.';
            faltaContrasena.value = true;
            $('.overlay-spinner').hide();
            return;
        } else if (v_nPass1.value != v_nPass2.value) {
            msgError.value = 'Las contraseñas no coinciden.';
            faltaContrasena.value = true;
            $('.overlay-spinner').hide();
            return;
        }
        await cambiarContrasena({
            'password1': v_nPass1.value,
            'password2': v_nPass2.value
        }).then(
            (response) => {
                if (response.error) {
                    $('.overlay-spinner').hide();
                    alertas.alertError(response.error);
                } else {
                    alertas.alertSuccess('Contraseña cambiada con exito');
                    $('.overlay-spinner').hide();
                    setTimeout(() => location.reload(), 1000);
                }
            }
        );
    }

    // Función para mostrar contraseña
    function togglePassword() {
        let pass = $('.dataInput');
        let btnMostrar = $('#btnInput');

        if (pass[0].type === 'password') {
            pass[0].type = 'text';
            pass[1].type = 'text';
            btnInput.value = true;
        } else {
            pass[0].type = 'password';
            pass[1].type = 'password';
            btnInput.value = false;
        }
    }

    // Variables para reenvio de contraseña
    async function reenviarCodigo() {
        let response = await alertas.alertQuestion('¿Reenviar código de recuperación?');
        if (response.isConfirmed) {
            $('.overlay-spinner').show();
            const resulEnvio = await enviarCodigo();
            if (resulEnvio.error) {
                alertas.alertWarning(resulEnvio.error, true, 3500);
            }
            $('.overlay-spinner').hide();
        }
    }
    //  Función para limpiar campos
    function limpiarCampo () {
        v_nPass1.val = '';
        v_nPass2.val = '';
        v_code.value = ''
        faltaCodigo.value = false;
        codigoCorrecto.value = false;
        mostrarFormRecup.value = false;
        btnInput.value = false;
        msgError.value = '';
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
    }

    #btn_pedido button:hover {
        background-color: #c56cf0;
    }

    .inputCodeBad {
        border: 1px solid red;
    }

    .inputCodeGood {
        border: 1px solid rgba(0, 128, 0, 0.795);
    }
</style>