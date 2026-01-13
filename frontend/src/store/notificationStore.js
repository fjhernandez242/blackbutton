// Script para el manejo de alertas
import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
    state: () => ({
        mostrarAlert: false,
        mensaje: ''
    }),
    actions: {
        lanzarAlerta(msj) {
            this.mensaje = msj;
            this.mostrarAlert = true;

            // Auto-cerrado opcional tras 1.5 segundos
            setTimeout(() => {
                this.mostrarAlert = false;
            }, 1500);
        }
    }
});