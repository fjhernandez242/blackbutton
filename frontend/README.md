# E-Commerce Frontend - BlackButton

Esta es la interfaz de usuario desarrollada en Vue 3 y Vite, se encarga de la
gestión de catálogo, carrito de compras e integración con la API de Django para
la generación de pedido con el uso de Whatsapp.

* Framework: Vue 3
* Build Tool: Vite
* Estado Global: Pinia
* Estilos: Bootstrap 5 / CSS puro
* HTTP Client: Fetch (para conectar con Django)

## Estructura de carpetas

* src/assests/ : Imagenes, funciones de SweetAlert y minificados.
* src/views/ : Páginas principales.
* src/router/ : Rutas para las vistas principal y panel de administación.
* src/config/ : Urls para la comunicación con Django.
* src/services/ : Servicio fetch, llamadas a Django y servicio de envio de
  mensajes por WhatsApp.
* src/store/ : Uso de LocalStore para la función de carrito.

## Características implementadas

* Integración con WhatsApp: Generación de dinámica de menajes formateados.
* Gestión de carrito: Uso de reduce para el cálculo de totales en tiempo real.
* Asincronía: Manejo de alertas con SweetAlert2 y promesas.
* Consumo de API: Comunicación fluida con Django REST Framework.

## Proximas mejoras

* Agregar validación de stock en tiempo real.
* Adaptar el panel de administración para la visualización de estadisticas de venta.
* Rastreo de pedidos en el panel de adminstración.
* El panel de administración deberá tener su acceso independiente, e implementar
  un login.

## Instalación y configuración

### Iniciar proyecto

```sh
npm install
```

### Compilar para desarrollo

```sh
npm run dev
```
