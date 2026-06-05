<template>
    <section>
        <div class="container d-flex justify-content-center align-items-center vh-100">
            <div class="card shadow-lg p-4">
                <div class="card-header border-0 text-center">
                    <h3>¡Bienvenida!</h3>
                    <div id="img_bienvenida">
                        <img src="/src/assets/img/crocket.png" alt="">
                    </div>
                </div>
                <div class="card-body">
                    <form @submit.prevent="login" novalidate id="form_login">
                        <div class="form-floating mb-3">
                            <input type="text" class="form-control" id="floatingInput" placeholder="nombre@ejemplo.com"
                                v-model="v_user">
                            <label for="floatingInput">Usuario</label>
                        </div>
                        <div class="form-floating">
                            <input type="password" class="form-control" id="floatingPassword" placeholder="Contraseña"
                                v-model="v_pass">
                            <label for="floatingPassword">Contraseña</label>
                        </div>
                        <div class="col-auto">
                            <span id="passwordForgot" class="form-text mt-2" @click="recuperarContrasena()">
                            Olvide mi contraseña
                            </span>
                        </div>
                        <div>
                            <small v-if="error_vacio" class="error_campo">
                                No debes dejar campos vacíos.
                            </small>
                            <small v-if="error" class="error_campo">
                                {{ msg_error }}
                            </small>
                        </div>
                        <button type="submit" class="btn mt-2">Entrar</button>
                    </form>
                </div>
            </div>
        </div>
        <modalRecuperacion
            :producto=prodConsultado
            :visible="mostrarModal"
            @cerrar-modal="cerrarModal"/>
    </section>
</template>
<script setup>
    import { ref, onMounted } from 'vue';
    import alertas from '@/assets/js/notifications';
    import { inicioSesion } from '@/services/usuario-services';
    import { useCartStore } from '@/store/cartStore';
    import router from '@/router';
    import { useRoute } from 'vue-router';
    import modalRecuperacion from './modal/modalRecuperacion.vue';

    const route = useRoute();

    const cartStore = useCartStore();

    // Creación de variables del formulario
    const v_user = ref('');
    const v_pass = ref('');
    const error = ref(false);
    const msg_error = ref('Erro inesperado');
    const error_vacio = ref(false);
    const mostrarModal = ref(false);
    const prodConsultado = ref({});
    function cerrarModal() {
        mostrarModal.value = false;
        // idProducto.value = null;
    }
    // Función para recuperación de contraseña
    async function recuperarContrasena() {
        let response = await alertas.alertQuestion('¿Iniciar recuperación de contraseña?');
        if (response.isConfirmed) {

            mostrarModal.value = true;
        }
    }
    // Función de logeo
    async function login() {
        try {
            if (v_pass.value == '') {
                $('#floatingPassword').addClass('campoVacio');
                error_vacio.value = true;
                return;
            } else if (v_user.value == '') {
                $('#floatingInput').addClass('campoVacio');
                error_vacio.value = true;
                return;
            }
            $('.overlay-spinner').show();
            inicioSesion({'username': v_user.value, 'password': v_pass.value})
                .then((response) => {
                    $('.overlay-spinner').hide();
                    if (response.error) {
                        msg_error.value = response.error;
                        error.value = true;
                    } else {
                        localStorage.setItem('admin_token', `Token ${response.token}`);
                        localStorage.setItem('admin_user', response.user);
                        // Se calcula la hora de expiración
                        const duracionSesion = 86400000; // 24 horas en milisegundos
                        const tiempoExpiracion = Date.now() + duracionSesion;

                        localStorage.setItem('admin_token_expires', tiempoExpiracion);

                        router.push('panel');
                    }
            });
        } catch (error) {
            $('.overlay-spinner').hide();
            alertas.alertError(error.message);
        }
    }

    onMounted(() => {
        // Verificamos si en el URL viene ?mensaje=sesion_expirada
        if (route.query.mensaje === 'sesion_expirada') {
            alertas.alertWarning('Tú sesión ha expirado', false, 2000);

            // Limpieza de URL para que desaparezca la alertar al refrescar página
            router.replace({ query: {} });
        }
    });

    // Escucha evento focus
    $(document).on('focus', '#floatingPassword, #floatingInput' ,function (event) {
        error_vacio.value = false;
        error.value = false;
        $('#floatingPassword').removeClass('campoVacio');
        $('#floatingInput').removeClass('campoVacio');
    });
</script>
<style scoped>
    .card {
        width: 100%;
        max-width: 400px;
        border-radius: 15px;
    }

    .btn {
        background-color: #B53471;
    }

    .btn:hover {
        background-color: #c56cf0;
    }

    #img_bienvenida {
        position: absolute;
        top: -6rem;
        left: -15rem;
    }

    #img_bienvenida img {
        background-color: aliceblue;
        max-width: 25%;
        border-radius: 15px;
    }

    #passwordForgot {
        cursor: pointer;
        margin-top: 10rem !important;
    }

    #passwordForgot:hover {
        color: #c56cf0;
    }

    .error_campo {
        color: red;

    }

    .campoVacio {
        border: solid red 1px;
        box-shadow: 5px 5px 5px #888888;
    }
</style>