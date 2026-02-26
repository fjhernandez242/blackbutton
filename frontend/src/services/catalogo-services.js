import { URLS } from "@/config/api-urls";

// Listar productos
export function getProductos(params) {
    return fetch(URLS.LISTAR_PRODUCTOS, {
        method: 'POST',
        body: JSON.stringify(params),
        headers: {
            "Content-Type": "application/json"
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
    formData.append("tipo_entrega", params.tipo_entrega);
    formData.append("inventario", params.inventario);
    formData.append("comentario", params.comentario);
    formData.append("imagen", params.imagen);

    return fetch(URLS.AGREGAR_PRODUCTO, {
        method: 'POST',
        body: formData,
        headers: {
            'Authorization': "Token ba272486f37c7250b28ff645d6d0d31ef34e49b1" // VPS
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
            "Content-Type": "application/json"
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
// Agrega un nuevo pedido
export function agregarPedido(params, codigo_temp) {
    return fetch(URLS.AGREGAR_PEDIDO, {
        method: 'POST',
        body: JSON.stringify({
            "id": params.id,
            "cantidad": params.quantity,
            "tipo_entrega": params.tipo_entrega,
            "codigo_temp": codigo_temp
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(
        (response) => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(`Error ${response.status}: ${JSON.stringify(errorData)}`);
                });
            }
            return response.json()
        }
    );
}
// Cambia estado del producto
export function setterProducto(params) {
    return fetch(URLS.SETTER_PRODUCTO, {
        method: 'POST',
        body: JSON.stringify(params),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(
        (response) => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(`Error ${response.status}: ${JSON.stringify(errorData)}`);
                });
            }
            return response.json()
        }
    )
}
// Apartar producto
export function apartarProducto(params) {
    return fetch(URLS.APARTAR_PRODUCTO, {
        method: 'POST',
        body: JSON.stringify(params),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(
        (response) => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(`Error ${response.status}: ${JSON.stringify(errorData)}`);
                });
            }
            return response.json()
        }
    );
}