// stores/cartStore.js

import { defineStore } from 'pinia';
import { useNotificationStore } from './notificationStore';
import alertas from '@/assets/js/notifications';

export const useCartStore = defineStore('cart', {

    // El 'state' es donde se guarda la información (el carrito en sí)
    state: () => {
        const savedCart = localStorage.getItem('miCarrito');
        const parsed = savedCart ? JSON.parse(savedCart) : null;

        return {
            // Si 'parsed' tiene 'items', los usa; si no, array vacío
            items: parsed?.items || [],
            tipoEntrega: parsed?.tipoEntrega || { "cambioTipo": 0 },
            // Si 'parsed' tiene 'expiracion', la usa; si no, valores por defecto
            expiracion: parsed?.expiracion || { 'id_temp': "", "time_expira": "" },
            minutos: parsed?.minutos || 15,
            segundos: parsed?.segundos || 60,
            intervalo: parsed?.intervalo || null,
        }
    },

    // Los 'actions' son las funciones que modifican el estado (añadir, quitar, etc.)
    actions: {
        /**
         * Agrega un producto al carrito. Si ya existe, incrementa la cantidad.
         * @param {Object} product - El producto a añadir (debe tener id, nombre, precio, etc.)
         */
        saveToLocalStorage() {
            const dataSave = {
                items: this.items,
                expiracion: this.expiracion,
                tipoEntrega: this.tipoEntrega,
                // minutos: this.minutos,
                // segundos: this.segundos,
                intervalo: this.intervalo
            };
            localStorage.setItem('miCarrito', JSON.stringify(dataSave));
        },

        addItem(product, cantidad) {

            const notify = useNotificationStore();
            const existingItem = this.items.find(item => item.id === product.id);

            if (existingItem) {
                // Si el producto ya existe, solo aumentamos la cantidad
                existingItem.quantity = parseInt(existingItem.quantity) + parseInt(cantidad);
            } else {
                // Si es un producto nuevo, lo agregamos con quantity: 1
                this.items.push({
                    ...product,
                    quantity: parseInt(cantidad),
                });
            }
            notify.lanzarAlerta(`Se añadio ${product.producto} al carrito`);
            this.saveToLocalStorage();
        },
        deleteItem(id) {
            const listadoItems = this.items.filter(item => item.id === id);

            if (listadoItems[0].quantity > 1) {
                listadoItems[0].quantity--;
            } else {
                this.items = this.items.filter(item => item.id !== id);
            }

            this.saveToLocalStorage();
            return id;
        },
        cambiarTipoEntrega(params) {
            this.tipoEntrega = params;
            this.saveToLocalStorage();
        },
        setTemp(id_temp, time_expira) {
            this.expiracion.id_temp = id_temp;
            this.expiracion.time_expira = time_expira;
            this.saveToLocalStorage();

        },
        detenerTemporizador() {
            if (this.intervalo) {
                clearInterval(this.intervalo);
                this.intervalo = null; // Limpiamos la referencia
            }
            this.$reset();
            localStorage.removeItem('miCarrito');
            setTimeout(() => location.reload(), 1000);
        },
        // Dentro de actions en cartStore.js
        iniciarTemporizador() {

            // Evitar múltiples intervalos si se llama a la función varias veces
            if (this.intervalo) {
                clearInterval(this.intervalo);
            }

            this.intervalo = setInterval(() => {
                if (this.expiracion.time_expira) {
                    const ahora = new Date();
                    const fechaExpira = new Date(this.expiracion.time_expira);

                    if (ahora > fechaExpira) {
                        // TIEMPO AGOTADO
                        this.detenerTemporizador();
                        alertas.alertWarning("¡Tiempo agotado!", false);
                        setTimeout(() => location.reload(), 1000);
                    } else {
                        // CALCULAR TIEMPO RESTANTE REAL
                        const diferenciaMs = fechaExpira - ahora;

                        // Convertimos la diferencia real en minutos y segundos
                        // Esto es mucho más seguro que restar manualmente
                        this.minutos = Math.floor((diferenciaMs / 1000 / 60) % 60);
                        this.segundos = Math.floor((diferenciaMs / 1000) % 60);

                        // Formateo visual opcional en consola
                        // console.log(`${this.minutos}:${this.segundos < 10 ? '0' : ''}${this.segundos}`);

                        // NOTA: No recomiendo saveToLocalStorage aquí cada segundo.
                        // El tiempo ya está seguro en "time_expira" dentro del storage.
                    }
                }
            }, 1000);
        },
        resetStore() {
            this.$reset();
            localStorage.removeItem('miCarrito');
        }
    },

    // Los 'getters' son como propiedades computadas para el store (para leer información)
    getters: {
        /**
         * Devuelve el número total de productos en el carrito.
         * Esto es lo que usarás para el contador en tu header.
         */
        totalItemsCount: (state) => {
            // Usamos .reduce para sumar la propiedad 'quantity' de todos los items
            return state.items.reduce((total, item) => total + item.quantity, 0);
        },

        loadedProducts: (state) => {
            return state.items;
        },

        /**
         * Realiza la suma de todos los productos
         */
        totalPrecio: (state) => {
            const totalCentimos = state.items.reduce((total, item) => {
                // Obtiene el costo asignado al producto
                const precio_relativo = parseFloat(item.precio);
                // Realiza el calculo de precio con la cantidad de productos seleccionados
                const precio_calculado = precio_relativo * item.quantity;

                return total + (precio_calculado * 100);
            }, 0);

            return (totalCentimos / 100).toFixed(2);
        },
    },
});