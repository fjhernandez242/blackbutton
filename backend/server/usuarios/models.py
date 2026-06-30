from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class codigo_recuperacion_model(models.Model):

    class estadoUso(models.TextChoices):
        USADO = 'U', _('Usado')
        DESUSO = 'D', _('Desuso')
        EXPIRADO = 'E', _('Expirado')

    codigo = models.IntegerField(verbose_name='Codigo', null=True, blank=True)
    estado = models.TextField(default=estadoUso.DESUSO, choices=estadoUso.choices, verbose_name='Estado de uso', null=True, blank=True)
    periodo = models.DateField(verbose_name='Periodo para registro', null=True, blank=True)
    fecha_registro = models.DateTimeField(verbose_name='Fecha de regsitro', null=True, blank=True)

    class Meta:
        verbose_name="Recuperación"

    def __str__(self):
        return self.codigo
