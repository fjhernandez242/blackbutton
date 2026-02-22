from django.urls import re_path
from . import views

urlpatterns = [
    re_path('listado', views.productos),
    re_path('nuevo', views.agregar_producto),
    re_path('editar', views.editar_producto),
    re_path('eliminar', views.eliminar_producto),
    re_path('productoId', views.getProductoById),
    re_path('agregarPedido', views.agregar_pedido),
    re_path('setterProducto', views.setterProduto),
]
