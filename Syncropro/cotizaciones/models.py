from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Cotizacion(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("aprobada", "Aprobada"),
        ("rechazada", "Rechazada"),
    ]
    numero = models.CharField(max_length=50, unique=True)
    cliente_nombre = models.CharField(max_length=200)
    razon_social = models.CharField(max_length=200)
    nit = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=300, blank=True)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField()
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="pendiente")
    valor_tablero = models.PositiveIntegerField(default=0)
    descuento_tablero = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    descuento_materiales = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    fecha = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Cotización #{self.numero} - {self.cliente_nombre}"

    @property
    def subtotal_tablero(self):
        return int(self.valor_tablero * (100 - self.descuento_tablero) / 100)

    @property
    def subtotal_materiales(self):
        total = sum(m.subtotal for m in self.materiales.all())
        return int(total * (100 - self.descuento_materiales) / 100)

    @property
    def subtotal(self):
        return self.subtotal_tablero + self.subtotal_materiales

    @property
    def iva(self):
        return int(self.subtotal * 19 / 100)

    @property
    def total(self):
        return self.subtotal + self.iva


class Material(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="materiales")
    nombre = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    valor_unitario = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99999999)])
    descuento = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.nombre} - {self.cantidad} unidades"

    @property
    def subtotal(self):
        total = self.cantidad * self.valor_unitario
        return int(total * (100 - self.descuento) / 100)