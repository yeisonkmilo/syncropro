from django.db import models
from django.core.validators import MinValueValidator
from cotizaciones.models import Cotizacion

class OrdenProduccion(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("en_proceso", "En proceso"),
        ("finalizada", "Finalizada"),
    ]

    numero = models.CharField(max_length=50, unique=True)
    cliente_nombre = models.CharField(max_length=200)
    razon_social = models.CharField(max_length=200)
    nit = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=300, blank=True)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField()
    tipo_tablero = models.CharField(max_length=200)
    dimensiones = models.CharField(max_length=200)
    color = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="pendiente")
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.SET_NULL, null=True, blank=True)
    archivo = models.FileField(upload_to='ordenes_archivos/%Y/%m/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Orden #{self.numero} - {self.cliente_nombre}"


class MaterialProduccion(models.Model):
    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, related_name="materiales")
    nombre = models.CharField(max_length=200)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"