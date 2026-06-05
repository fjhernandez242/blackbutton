// Script para el manejo de alertas
import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
    state: () => ({
        notifications: [] // Cambiamos variables únicas por un arreglo
    }),
    actions: {
        lanzarAlerta(msj) {
            const id = Date.now(); // ID único basado en tiempo

            // Añadimos la nueva notificación al arreglo
            this.notifications.push({
                id,
                mensaje: msj
            });
            // Auto-cerrado opcional tras 1.5 segundos
            setTimeout(() => {
                this.eliminarAlerta(id);
            }, 3000);
        },
        eliminarAlerta(id) {
            this.notifications = this.notifications.filter(n => n.id !== id);
        }
    }
});