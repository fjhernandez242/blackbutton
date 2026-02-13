import { useCartStore } from "@/store/cartStore";

export const sendMessage = () => {
    const cartStore = useCartStore();

    const data = cartStore.items;
    const productos = [];
    $.each(data, function (index, value) {
        productos.push(
            {
                'nombre': value.producto,
                "precio": value.precio,
                "cantidad": value.quantity,
                "disponibilidad": value.disponibilidad == 1 ? 'Inmediata' : 'Sobre pedido'
            });
    });
    // Envio de mensaje por WhatsApp
    const numero = "3922074261";
    const listaProductos = productos.map(p => {
        return `*• ${p.nombre}* \nPrecio: $ ${p.precio} \nEntrega: ${p.disponibilidad}`
    }).join('\n');
    const total = productos.reduce((acc, p) => acc + (p.precio * p.cantidad), 0);
    const totalFormateado = total.toLocaleString('es-MX', {
        style: 'currency',
        currency: 'MXN'
    });
    const mensaje = `*📦 ¡Nuevo Pedido! 📦*\n\n` +
        `Hola, me interesan los siguientes amigurumis:\n` +
        `${listaProductos}\n` +
        `*Total estimado*: ${totalFormateado}\n\n` +
        `_No incluye gastos de envío_\n` +
        `_Enviado desde BlackButton web_`;
    const url = `https://api.whatsapp.com/send?phone=${numero}&text=${encodeURIComponent(mensaje)}`;
    window.open(url, "_black");

};