import { URLS } from "@/config/api-urls";

export function inicioSesion(params) {
    return fetch(URLS.INICIO_SESION, {
        method: 'POST',
        body: JSON.stringify(params),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(async (response) => {
        if (response.ok) {
            return response.json();
        }

        let textoMensaje = '';
        try {
            const datosError = await response.json();

            textoMensaje = 'Error en el formato de respuesta del servidor';
        } catch (e) {
            textoMensaje = 'Error inesperado en el servidor';
        }

        const errorFinal = new Error(textoMensaje);
        errorFinal.status = response.status; // Se guarda el número 401

        throw errorFinal; // Rompe la promesa y activa el catch
    });
}

export function cerrarSesion(params) {
    return fetch(URLS.CERRAR_SESION, {
        method: 'POST',
        body: JSON.stringify(params),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': params.token
        }
    }).then(async (response) => {
        if (!response.ok) {
            const datosError = await response.json();
            return datosError;
        }
        return response.json();
    });
}