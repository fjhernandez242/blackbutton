export const ERROR_MESSAGES = {
    100: "Entrega inmediata requiere inventario mayor a 0",
    101: "Campos faltantes",
    200: "¡Producto agregado!"
};

export const getErrorMessages = (code) => {
    return ERROR_MESSAGES[code] || "Ha ocurrido un error inesperado (Código: " + code + ")";
};