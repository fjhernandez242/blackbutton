import { URLS } from "@/config/api-urls";

// Listar productos
export function getProductos() {
    return fetch(URLS.LISTAR_PRODUCTOS, {
        headers: {
            "Authorization": "Token 6970ab58d53f6bd8c94183a3360512762ac52a06"
        }
    }).then(
        (response) => {
            if (!response.ok) {
                throw new Error('Error al cargar los productos: ' + response.statusText);
            }
            return response.json();
        }
    );
}
// Servicio para cargar nuevo producto
export function cargarProducto(params) {

    const formData = new FormData();
    formData.append("producto", params.producto);
    formData.append("precio", params.precio);
    formData.append("dimensiones", params.dimensiones);
    formData.append("imagen", params.imagen);

    return fetch(URLS.AGREGAR_PRODUCTO, {
        method: 'POST',
        body: formData,
        headers: {
            'Authorization': "Token 6970ab58d53f6bd8c94183a3360512762ac52a06"
        }
    }).then(
        (response) => {
            if (!response.ok) {
                // Mejora: Es útil incluir el body de error si es posible
                return response.json().then(errorData => {
                    throw new Error(`Error ${response.status}: ${JSON.stringify(errorData)}`);
                });
            }
            return response.json();
        }
    )

}
// Obtener producto por ID
export function productoById(id) {
    return fetch(URLS.PRODUCTO_ID, {
        method: 'POST',
        body: JSON.stringify({
            "id": id
        }),
        headers: {
            "Content-Type": "application/json",
            'Authorization': "Token 6970ab58d53f6bd8c94183a3360512762ac52a06"
        }
    }).then(
        (response) => {
            if (!response.ok) {
                // Mejora: Es útil incluir el body de error si es posible
                return response.json().then(errorData => {
                    throw new Error(`Error ${response.status}: ${JSON.stringify(errorData)}`);
                });
            }
            return response.json();
        }
    )
}