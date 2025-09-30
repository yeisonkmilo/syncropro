from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import OrdenProduccion, MaterialProduccion
from .forms import OrdenProduccionForm, MaterialProduccionInlineFormSet
from cotizaciones.models import Cotizacion

def lista_ordenes(request):
    ordenes = OrdenProduccion.objects.all().order_by("-fecha_creacion")
    return render(request, "produccion/lista_ordenes.html", {"ordenes": ordenes})

def nueva_orden(request):
    if request.method == "POST":
        form = OrdenProduccionForm(request.POST, request.FILES)
        formset = MaterialProduccionInlineFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            orden = form.save()
            formset.instance = orden
            formset.save()
            return redirect("produccion:lista")
    else:
        form = OrdenProduccionForm()
        formset = MaterialProduccionInlineFormSet()

    cotizaciones = Cotizacion.objects.all().order_by("-id")
    return render(request, "produccion/nueva_orden.html", {
        "form": form,
        "formset": formset,
        "cotizaciones": cotizaciones
    })

def detalle_orden(request, pk):
    orden = get_object_or_404(OrdenProduccion, pk=pk)
    return render(request, "produccion/detalle_orden.html", {
        "orden": orden,
        "materiales": orden.materiales.all()
    })

def editar_orden(request, pk):
    orden = get_object_or_404(OrdenProduccion, pk=pk)
    if request.method == "POST":
        form = OrdenProduccionForm(request.POST, request.FILES, instance=orden)
        formset = MaterialProduccionInlineFormSet(request.POST, instance=orden)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("produccion:detalle", pk=orden.pk)
    else:
        form = OrdenProduccionForm(instance=orden)
        formset = MaterialProduccionInlineFormSet(instance=orden)

    return render(request, "produccion/editar_orden.html", {
        "form": form,
        "formset": formset,
        "orden": orden
    })

def eliminar_orden(request, pk):
    orden = get_object_or_404(OrdenProduccion, pk=pk)
    if request.method == "POST":
        orden.delete()
        return redirect("produccion:lista")
    return render(request, "produccion/eliminar_orden.html", {"orden": orden})

def cargar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    return JsonResponse({
        'cliente_nombre': cotizacion.cliente_nombre,
        'razon_social': cotizacion.razon_social,
        'telefono': cotizacion.telefono,
        'correo_electronico': cotizacion.correo_electronico,
        'nit': getattr(cotizacion, 'nit', ''),
        'direccion': getattr(cotizacion, 'direccion', ''),
        'descripcion': cotizacion.descripcion,
        'materiales': list(cotizacion.materiales.values('nombre', 'cantidad'))
    })