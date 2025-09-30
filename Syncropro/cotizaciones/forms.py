from django import forms
from django.forms import inlineformset_factory
from .models import Cotizacion, Material

class MaterialFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        valid_forms = [
            form for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        ]
        if not valid_forms:
            raise forms.ValidationError("Debe agregar al menos un material.")

MaterialInlineFormSet = inlineformset_factory(
    Cotizacion,
    Material,
    formset=MaterialFormSet,
    fields=["nombre", "cantidad", "valor_unitario", "descuento"],
    extra=0,
    can_delete=True,
    widgets={
        "nombre": forms.TextInput(attrs={"class": "form-control"}),
        "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
        "valor_unitario": forms.NumberInput(attrs={"class": "form-control", "step": "1"}),
        "descuento": forms.NumberInput(attrs={"class": "form-control", "step": "1", "min": "0", "max": "100"}),
    },
)

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = [
            "numero", "cliente_nombre", "razon_social", "nit", "direccion",
            "telefono", "correo_electronico", "descripcion", "valor_tablero",
            "descuento_tablero", "descuento_materiales"
        ]
        widgets = {
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "cliente_nombre": forms.TextInput(attrs={"class": "form-control"}),
            "razon_social": forms.TextInput(attrs={"class": "form-control"}),
            "nit": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "correo_electronico": forms.EmailInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "valor_tablero": forms.NumberInput(attrs={"class": "form-control", "step": "1"}),
            "descuento_tablero": forms.NumberInput(attrs={"class": "form-control", "step": "1", "min": "0", "max": "100"}),
            "descuento_materiales": forms.NumberInput(attrs={"class": "form-control", "step": "1", "min": "0", "max": "100"}),
        }