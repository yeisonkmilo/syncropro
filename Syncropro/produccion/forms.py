from django import forms
from django.forms import inlineformset_factory
from .models import OrdenProduccion, MaterialProduccion

class OrdenProduccionForm(forms.ModelForm):
    class Meta:
        model = OrdenProduccion
        fields = [
            "numero", "cliente_nombre", "razon_social", "nit", "direccion",
            "telefono", "correo_electronico", "tipo_tablero", "dimensiones",
            "color", "observaciones", "estado", "cotizacion", "archivo"
        ]
        widgets = {
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "cliente_nombre": forms.TextInput(attrs={"class": "form-control"}),
            "razon_social": forms.TextInput(attrs={"class": "form-control"}),
            "nit": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "correo_electronico": forms.EmailInput(attrs={"class": "form-control"}),
            "tipo_tablero": forms.TextInput(attrs={"class": "form-control"}),
            "dimensiones": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "cotizacion": forms.Select(attrs={"class": "form-select"}),
            "archivo": forms.FileInput(attrs={"class": "form-control"}),
        }

MaterialProduccionInlineFormSet = inlineformset_factory(
    OrdenProduccion,
    MaterialProduccion,
    fields=["nombre", "cantidad"],
    extra=1,
    can_delete=True,
    widgets={
        "nombre": forms.TextInput(attrs={"class": "form-control"}),
        "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
    },
)