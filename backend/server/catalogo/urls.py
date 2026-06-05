from django.urls import re_path
from . import views

urlpatterns = [
    re_path('listado', views.productos),
    re_path('nuevo', views.agregar_producto),
    re_path('editar', views.editar_producto),
    re_path('eliminar', views.eliminar_producto),
    re_path('productoId', views.getProductoById),
    re_path('agregarPedido', views.agregar_pedido),
    re_path('setterProducto', views.setterProducto),
    re_path('apartarProducto', views.apartados),
    re_path('obtenerExpiracion', views.obtener_expiracion),
    re_path('obtenerPedidco', views.getPedidoByClave),
    re_path('cambioEstadoVenta', views.cambioEstadoVenta),
    re_path('calculoMovimientos', views.calculoMovimientos),
]
