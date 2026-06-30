export const ERROR_MESSAGES = {
    100: "Entrega inmediata requiere inventario mayor a 0",
    101: "Campos faltantes",
    102: "El valor del producto debe ser mayor de 0",
    103: "Las dimensiones del producto deben ser mayor de 0",
    104: "Debes agregar la clave o fecha del pedido",
    200: "¡Producto agregado!",
    201: "¡Producto actualizado!",
};

export const getErrorMessages = (code) => {
    return ERROR_MESSAGES[code] || "Ha ocurrido un error inesperado (Código: " + code + ")";
};