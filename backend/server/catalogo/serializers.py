from rest_framework import serializers
from .models import catalogo_model, pedidos_model, cookietem_body_model, cookietem_header_model

class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = catalogo_model
        fields = ['id', 'producto', 'precio', 'dimensiones', 'imagen', 'tipo_entrega', 'inventario', 'comentario', 'estado']

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = pedidos_model
        fields = [  'id', 'codigo_venta', 'id_producto', 'cantidad_vendida', 'tipo_entrega', 'estado']

class HeaderApartadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = cookietem_header_model
        fields = [ 'id', 'codigo_temp', 'fecha_expiracion', 'fecha_registro' ]

class BodyApartadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = cookietem_body_model
        fields = [ 'id', 'id_codigo', 'producto_id', 'cantidad_prod']