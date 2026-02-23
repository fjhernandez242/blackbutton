from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class catalogo_model(models.Model):

    class tipo_de_entrega(models.IntegerChoices):
        INMEDIATA = 1, _('Inmediata')
        PEDIDO = 2, _('Pedido')

    class estado_venta(models.TextChoices):
        DISPONIBLE = 'D', _('Disponible')
        RESERVADO = 'R', _('Reservado')

    producto = models.CharField(max_length=255, verbose_name='Producto', null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio', null=True, blank=True)
    dimensiones = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='Dimensiones', null=True, blank=True)
    imagen = models.ImageField(upload_to='catalogo/' ,null=True, blank=True)
    tipo_entrega = models.IntegerField(default=tipo_de_entrega.INMEDIATA, choices=tipo_de_entrega.choices, verbose_name='Tipo de entrega', null=True, blank=True)
    inventario = models.IntegerField(verbose_name='Inventario', default=1, blank=True)
    comentario = models.TextField(null=True, blank=True)
    estado = models.TextField(default=estado_venta.DISPONIBLE, choices=estado_venta.choices, verbose_name='Estado del producto', null=True, blank=True)
    fecha_registro = models.DateTimeField(verbose_name='Fecha de regsitro', null=True, blank=True)

    class Meta:
        verbose_name="Catalogo"
        verbose_name_plural="Catalogos"

    def __str__(self):
        return self.producto

class pedidos_model(models.Model):

    class tipo_de_entrega(models.IntegerChoices):
        INMEDIATA = 1, _('Inmediata')
        PEDIDO = 2, _('Pedido')

    class estado_pedido(models.IntegerChoices):
        PROCESO = 1, _('En proceso')
        FINALIZADA = 2, _('Finalizada')
        CANCELADA = 3, _('Cancelada')

    codigo_venta = models.CharField(max_length=50,verbose_name='Código de venta', null=True, blank=True)
    id_producto = models.IntegerField(verbose_name='Id del producto', null=True, blank=True)
    cantidad_vendida = models.IntegerField(verbose_name='Cantidad vendida', null=True, blank=True)
    tipo_entrega = models.IntegerField(default=tipo_de_entrega.INMEDIATA, choices=tipo_de_entrega.choices, verbose_name='Tipo de entrega', null=True, blank=True)
    estado = models.IntegerField(default=estado_pedido.PROCESO, choices=estado_pedido.choices, verbose_name='Estado de la venta', null=True, blank=True)
    fecha_venta = models.DateTimeField(verbose_name='Fecha de venta', null=True, blank=True)

    class Meta:
        verbose_name="Pedido"
        verbose_name_plural="Pedidos"

    def __str__(self):
        return self.codigo_venta

class cookietem_header_model(models.Model):

    codigo_temp = models.CharField(max_length=255, verbose_name="Código temporal", null=True, blank=True)
    fecha_expiracion = models.DateTimeField(verbose_name="Fecha de expiración", null=True, blank=True)
    fecha_registro = models.DateTimeField(verbose_name="Fecha de expiración", null=True, blank=True)

    class Meta:
        verbose_name="Encabezado"
        verbose_name_plural="Encabezados"

    def __str__(self):
        return self.codigo_temp

class cookietem_body_model(models.Model):

    id_codigo = models.CharField(max_length=255, verbose_name="Relación codigo con tabla header", null=True, blank=True)
    producto_id = models.IntegerField(verbose_name="Id del producto", null=True, blank=True)
    cantidad_prod = models.IntegerField(verbose_name="Cantidad de productos apartados", null=True, blank=True)

    class Meta:
        verbose_name="Cuerpo"
        verbose_name_plural="Cuerpos"

    def __str__(self):
        return self.id_codigo