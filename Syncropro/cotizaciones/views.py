from django.shortcuts import render, redirect, get_object_or_404
from .models import Cotizacion, Material
from .forms import CotizacionForm, MaterialInlineFormSet

def lista_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all().order_by("-id")
    return render(request, "cotizaciones/lista_cotizaciones.html", {"cotizaciones": cotizaciones})

def nueva_cotizacion(request):
    if request.method == "POST":
        form = CotizacionForm(request.POST)
        formset = MaterialInlineFormSet(request.POST, instance=Cotizacion())
        if form.is_valid() and formset.is_valid():
            cotizacion = form.save()
            formset.instance = cotizacion
            formset.save()
            return redirect("cotizaciones:lista")
    else:
        form = CotizacionForm()
        formset = MaterialInlineFormSet(instance=Cotizacion())
    return render(request, "cotizaciones/nueva_cotizacion.html", {"form": form, "formset": formset})

def detalle_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    return render(request, "cotizaciones/detalle_cotizacion.html", {
        "cotizacion": cotizacion,
        "materiales": cotizacion.materiales.all(),
        "subtotal_tablero": cotizacion.subtotal_tablero,
        "subtotal_materiales": cotizacion.subtotal_materiales,
        "subtotal": cotizacion.subtotal,
        "iva": cotizacion.iva,
        "total": cotizacion.total,
    })

def editar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.method == "POST":
        form = CotizacionForm(request.POST, instance=cotizacion)
        formset = MaterialInlineFormSet(request.POST, instance=cotizacion)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("cotizaciones:detalle", pk=cotizacion.pk)
    else:
        form = CotizacionForm(instance=cotizacion)
        formset = MaterialInlineFormSet(instance=cotizacion)
    return render(request, "cotizaciones/editar_cotizacion.html", {
        "form": form, "formset": formset, "cotizacion": cotizacion
    })

def eliminar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.method == "POST":
        cotizacion.delete()
        return redirect("cotizaciones:lista")
    return render(request, "cotizaciones/eliminar_cotizacion.html", {"cotizacion": cotizacion})