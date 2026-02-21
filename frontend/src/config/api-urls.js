// Url base
export const API_BASE_URL = 'https://blackbuttonbackend.fjdev.icu';
// Urls endpoint
export const URLS = {
    // Obtiene todos los usuarios
    LISTAR_USUARIOS: `${API_BASE_URL}/usuarios/getAll`,
    // Url para listar todos los productos
    LISTAR_PRODUCTOS: `${API_BASE_URL}/catalogo/listado`,
    // Url para cambiar agregar un producto
    AGREGAR_PRODUCTO: `${API_BASE_URL}/catalogo/nuevo`,
    // Url para editar un producto
    EDITAR_PRODUCTO: `${API_BASE_URL}/catalogo/editar`,
    // Url para eliminar un producto
    ELIMINAR_PRODUCTO: `${API_BASE_URL}/catalogo/eliminar`,
    // Url para obtener producto por ID
    PRODUCTO_ID: `${API_BASE_URL}/catalogo/productoId`,
    // Url para agregar pedido
    AGREGAR_PEDIDO: `${API_BASE_URL}/catalogo/agregarPedido`,
    // Url para cambiar el estado del producto
    SETTER_ESTADO: `${API_BASE_URL}/catalogo/setterEstado`,
};