// stores/cartStore.js

import { defineStore } from 'pinia';
import { useNotificationStore } from './notificationStore';

export const useCartStore = defineStore('cart', {
    // El 'state' es donde se guarda la información (el carrito en sí)
    state: () => ({
        // 'items' será un array de objetos, donde cada objeto es un producto en el carrito
        items: [],
    }),

    // Los 'actions' son las funciones que modifican el estado (añadir, quitar, etc.)
    actions: {
        /**
         * Agrega un producto al carrito. Si ya existe, incrementa la cantidad.
         * @param {Object} product - El producto a añadir (debe tener id, nombre, precio, etc.)
         */
        addItem(product) {

            const notify = useNotificationStore();
            const existingItem = this.items.find(item => item.id === product.id);

            if (existingItem) {
                // Si el producto ya existe, solo aumentamos la cantidad
                existingItem.quantity++;
            } else {
                // Si es un producto nuevo, lo agregamos con quantity: 1
                this.items.push({
                    ...product,
                    quantity: 1,
                });
            }
            notify.lanzarAlerta(`Se añadio ${product.producto} al carrito`);
        },
        deleteItem(id) {
            const listadoItems = this.items.filter(item => item.id === id);

            if (listadoItems[0].quantity > 1) {
                listadoItems[0].quantity--;
            } else {
                this.items = this.items.filter(item => item.id !== id);
            }


            return id;
        },

        // Podrías añadir más acciones como removeItem, clearCart, etc.
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