// Url base
export const API_BASE_URL = 'https://blackbuttonbackend.fjdev.icu/api';
// export const API_BASE_URL = 'http://localhost:8000';
// Urls endpoint
export const URLS = {
    // Url para inicio de sesion
    INICIO_SESION: `${API_BASE_URL}/usuarios/login`,
    // Url para cerrar sesión
    CERRAR_SESION: `${API_BASE_URL}/usuarios/logout`,
    // Obtiene todos los usuarios
    LISTAR_USUARIOS: `${API_BASE_URL}/usuarios/getAll`,
    // Url para reestablecer contraseña
    SEND_CODE: `${API_BASE_URL}/usuarios/enviarCodigo`,
    // Url para validar código
    VALID_CODE: `${API_BASE_URL}/usuarios/validarCodigo`,
    // Url para cambiar contrasena
    RESTAR_PASS: `${API_BASE_URL}/usuarios/restartPass`,
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
    SETTER_PRODUCTO: `${API_BASE_URL}/catalogo/setterProducto`,
    // Url para el apartado de producto
    APARTAR_PRODUCTO: `${API_BASE_URL}/catalogo/apartarProducto`,
    // Url para obtener expiracion
    OBTENER_EXPIRACION: `${API_BASE_URL}/catalogo/obtenerExpiracion`,
    // Url para obtener un pedido por medio de su clave
    OBTENER_PEDIDO: `${API_BASE_URL}/catalogo/obtenerPedidco`,
    // Url para completar la venta
    ESTADO_VENTA: `${API_BASE_URL}/catalogo/cambioEstadoVenta`,
    // Url para obtener el calculo de ventas
    CALCULO_VENTAS: `${API_BASE_URL}/catalogo/calculoMovimientos`,
    // Url para generar código de venta
    CODIGO_VENTA: `${API_BASE_URL}/catalogo/generaCodigoVenta`,
};