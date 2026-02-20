from rest_framework import serializers
from .models import catalogo_model, pedidos_model

class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = catalogo_model
        fields = ['id', 'producto', 'precio', 'dimensiones', 'imagen', 'tipo_entrega', 'inventario', 'comentario', 'estado']

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = pedidos_model
        fields = [  'id', 'codigo_venta', 'id_producto', 'cantidad_vendida', 'tipo_entrega', 'estado']