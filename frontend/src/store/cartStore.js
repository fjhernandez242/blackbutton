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
            segundos: parsed?.segundos || 0,
            intervalo: parsed?.intervalo || null,
            recarga: parsed?.recarga || 0,
        }
    },

    actions: {
        /**
         * Agrega un producto al carrito. Si ya existe, incrementa la cantidad.
         * @param {Object} product
         */
        saveToLocalStorage() {
            const dataSave = {
                items: this.items,
                expiracion: this.expiracion,
                tipoEntrega: this.tipoEntrega,
                minutos: this.minutos,
                segundos: this.segundos,
                intervalo: this.intervalo
            };
            localStorage.setItem('miCarrito', JSON.stringify(dataSave));
        },

        addItem(product, cantidad) {

            const notify = useNotificationStore();
            const existingItem = this.items.find(item => item.id === product.id && item.tipo_entrega === product.tipo_entrega);

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
            this.saveToLocalStorage();
            notify.lanzarAlerta(`Se añadio ${product.producto} al carrito`);
        },
        deleteItem(id, tipo_entrega) {

            const listadoItems = this.items.find(item => item.id == id && item.tipo_entrega == tipo_entrega);

            if (listadoItems.quantity > 1) {
                listadoItems.quantity--;
            } else {
                // Indica que dejo todo los elementos que sean diferentes al que se desea eliminar del carrito
                this.items = this.items.filter(item => (item.id != id));
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
        detenerTemporizador(restantes = false, finalizado = false) {
            // if (this.intervalo) {
            // }
            // clearInterval(this.intervalo);
            // this.intervalo = null; // Limpiamos la referencia
            if (!finalizado) {
                this.items = this.items.filter(item => (item.tipo_entrega !== 1));
            } else {
                this.items = [];
            }

            this.expiracion.id_temp = '';
            this.expiracion.time_expira = '';
            this.tipoEntrega.cambioTipo = 0;
            this.minutos = 15;
            this.segundos = 0;
            this.saveToLocalStorage();
            if (!restantes || finalizado) {
                this.$reset();
                localStorage.removeItem('miCarrito');
            }
            // setTimeout(() => location.reload(), 1000);
        },
        // Dentro de actions en cartStore.js
        iniciarTemporizador() {
            // Evitar múltiples intervalos si se llama a la función varias veces
            if (this.intervalo) {
                clearInterval(this.intervalo);
            }

            // this.detenerTemporizador();
            this.intervalo = setInterval(() => {
                // console.log('entra');
                // console.log(this.expiracion.time_expira);

                if (this.expiracion.time_expira) {
                    const ahora = new Date();
                    const fechaExpira = new Date(this.expiracion.time_expira);

                    if (ahora > fechaExpira) {
                        let restantes = false;
                        if ((this.items).length > 0) {
                            restantes = true;
                        }
                        // Tiempo agotado
                        this.detenerTemporizador(restantes);
                        alertas.alertWarning("¡Tiempo agotado!\nLos amigurumis de entrega inmediada\nSaldrán de tu carrito", false);
                        setTimeout(() => location.reload(), 1000);
                    } else {
                        // Calcular tiempo real
                        const diferenciaMs = fechaExpira - ahora;
                        this.minutos = Math.floor((diferenciaMs / 1000 / 60) % 60);
                        this.segundos = Math.floor((diferenciaMs / 1000) % 60);
                    }
                }
            }, 1000);
        },
        recargaCatalogo() {
            let cambio = this.recarga == 0 ? 1 : 0;
            this.recarga = cambio;
        }
    },

    getters: {
        /**
         * Devuelve el número total de productos en el carrito.
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