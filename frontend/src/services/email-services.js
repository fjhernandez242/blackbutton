import { useCartStore } from "@/store/cartStore";
const numberWhatsapp = import.meta.env.VITE_NUMBER;

export const sendMessage = (code) => {
    // Obtenemos los datos de Store
    const cartStore = useCartStore();
    const data = cartStore.items;
    // Se cataloga la información
    const productos = [];
    $.each(data, function (index, value) {
        productos.push(
            {
                'nombre': value.producto,
                "precio": value.precio,
                "cantidad": value.quantity,
                "tipo_entrega": value.tipo_entrega == 1 ? 'Inmediata' : 'Sobre pedido'
            });
    });
    // Envio de mensaje por WhatsApp
    const listaProductos = productos.map(p => {
        return `*• ${p.nombre}* ` +
            `\n      Cantidad: ${p.cantidad}` +
            `\n      Precio c/u: $ ${p.precio}` +
            `\n      Entrega: ${p.tipo_entrega}`
    }).join('\n');
    const subtotal = productos.reduce((acc, p) => acc + (p.precio * p.cantidad), 0);
    const subtotalFormateado = subtotal.toLocaleString('es-MX', {
        style: 'currency',
        currency: 'MXN'
    });
    let envio = 0;
    if (subtotal <= 700) {
        envio += 100;
    }
    const total = subtotal + envio;
    const totalFormateado = total.toLocaleString('es-MX', {
        style: 'currency',
        currency: 'MXN'
    });
    const mensaje = `*📦 ¡Nuevo Pedido! 📦*\n\n` +
        `Hola, me interesan los siguientes amigurumis:\n` +
        `${listaProductos}\n\n` +
        `*Código de pedido*: ${code}\n` +
        `*Subtotal*: ${subtotalFormateado}\n` +
        `*Envió*: $${envio}\n` +
        `*Total*: ${totalFormateado}\n\n` +
        `_Enviado desde BlackButton web_`;
    const url = `https://api.whatsapp.com/send?phone=${numberWhatsapp}&text=${encodeURIComponent(mensaje)}`;
    window.open(url, "_black");

};