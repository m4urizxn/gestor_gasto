from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Gasto, DineroEnviado
import json
import urllib.request
import urllib.error


def obtener_tasa_euro_pen():
    """Obtiene la tasa de cambio EUR a PEN desde una API gratuita"""
    try:
        url = "https://api.exchangerate-api.com/v4/latest/EUR"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            return float(data['rates']['PEN'])
    except:
        return 4.05  # Tasa por defecto si falla la API


def gastos_view(request):
    tasa_cambio = obtener_tasa_euro_pen()
    
    # Gastos por persona
    gastos_mama = Gasto.objects.filter(persona='mama')
    gastos_mauricio = Gasto.objects.filter(persona='mauricio')
    gastos_papa = Gasto.objects.filter(persona='papa')
    
    # Totales
    total_mama = gastos_mama.aggregate(Sum('monto'))['monto__sum'] or 0
    total_mauricio = gastos_mauricio.aggregate(Sum('monto'))['monto__sum'] or 0
    total_papa_euros = gastos_papa.aggregate(Sum('monto'))['monto__sum'] or 0
    total_papa_soles = float(total_papa_euros) * tasa_cambio
    total_familia = total_mama + total_mauricio
    
    context = {
        'gastos_mama': gastos_mama,
        'gastos_mauricio': gastos_mauricio,
        'gastos_papa': gastos_papa,
        'total_mama': total_mama,
        'total_mauricio': total_mauricio,
        'total_papa_euros': total_papa_euros,
        'total_papa_soles': total_papa_soles,
        'total_familia': total_familia,
        'tasa_cambio': tasa_cambio,
    }
    return render(request, 'gastos.html', context)


def agregar_gasto_view(request):
    if request.method == 'POST':
        persona = request.POST.get('persona')
        descripcion = request.POST.get('descripcion')
        monto = request.POST.get('monto')
        nota = request.POST.get('nota', '').strip() or None
        
        Gasto.objects.create(
            persona=persona,
            descripcion=descripcion,
            monto=monto,
            nota=nota
        )
        return redirect('gastos')
    return render(request, 'agregar_gasto.html')


def gestionar_gasto_view(request):
    gastos_mama = list(Gasto.objects.filter(persona='mama').values('id', 'descripcion', 'monto'))
    gastos_mauricio = list(Gasto.objects.filter(persona='mauricio').values('id', 'descripcion', 'monto'))
    gastos_papa = list(Gasto.objects.filter(persona='papa').values('id', 'descripcion', 'monto'))
    
    # Convertir Decimal a float para JSON
    for g in gastos_mama + gastos_mauricio + gastos_papa:
        g['monto'] = float(g['monto'])
    
    context = {
        'gastos_mama_json': json.dumps(gastos_mama),
        'gastos_mauricio_json': json.dumps(gastos_mauricio),
        'gastos_papa_json': json.dumps(gastos_papa),
    }
    return render(request, 'gestionar_gasto.html', context)


def editar_gasto_view(request, gasto_id):
    gasto = get_object_or_404(Gasto, id=gasto_id)
    
    if request.method == 'POST':
        gasto.persona = request.POST.get('persona')
        gasto.descripcion = request.POST.get('descripcion')
        gasto.monto = request.POST.get('monto')
        gasto.nota = request.POST.get('nota', '').strip() or None
        gasto.save()
        return redirect('gastos')
    
    return render(request, 'editar_gasto.html', {'gasto': gasto})


def eliminar_gasto_view(request, gasto_id):
    gasto = get_object_or_404(Gasto, id=gasto_id)
    
    if request.method == 'POST':
        gasto.delete()
        return redirect('gastos')
    
    return render(request, 'eliminar_gasto.html', {'gasto': gasto})


def dinero_enviado_view(request):
    tasa_cambio = obtener_tasa_euro_pen()
    
    envios = DineroEnviado.objects.all().order_by('-fecha')
    total_euros = envios.aggregate(Sum('monto_euros'))['monto_euros__sum'] or 0
    total_soles = envios.aggregate(Sum('monto_soles'))['monto_soles__sum'] or 0
    
    # Totales enviados por persona
    enviado_mama_soles = DineroEnviado.objects.filter(destino='mama').aggregate(Sum('monto_soles'))['monto_soles__sum'] or 0
    enviado_mauricio_soles = DineroEnviado.objects.filter(destino='mauricio').aggregate(Sum('monto_soles'))['monto_soles__sum'] or 0
    
    # Gastos totales por persona
    gastos_mama = Gasto.objects.filter(persona='mama').aggregate(Sum('monto'))['monto__sum'] or 0
    gastos_mauricio = Gasto.objects.filter(persona='mauricio').aggregate(Sum('monto'))['monto__sum'] or 0
    
    # Calcular restante
    restante_mama_soles = float(gastos_mama) - float(enviado_mama_soles)
    restante_mauricio_soles = float(gastos_mauricio) - float(enviado_mauricio_soles)
    restante_mama_euros = restante_mama_soles / tasa_cambio if tasa_cambio > 0 else 0
    restante_mauricio_euros = restante_mauricio_soles / tasa_cambio if tasa_cambio > 0 else 0
    
    context = {
        'envios': envios,
        'total_euros': total_euros,
        'total_soles': total_soles,
        'tasa_cambio': tasa_cambio,
        'gastos_mama': gastos_mama,
        'gastos_mauricio': gastos_mauricio,
        'enviado_mama_soles': enviado_mama_soles,
        'enviado_mauricio_soles': enviado_mauricio_soles,
        'restante_mama_soles': restante_mama_soles,
        'restante_mama_euros': restante_mama_euros,
        'restante_mauricio_soles': restante_mauricio_soles,
        'restante_mauricio_euros': restante_mauricio_euros,
    }
    return render(request, 'dinero_enviado.html', context)


def agregar_envio_view(request):
    tasa_cambio = obtener_tasa_euro_pen()
    
    if request.method == 'POST':
        destino = request.POST.get('destino')
        monto_euros = float(request.POST.get('monto_euros'))
        monto_soles = monto_euros * tasa_cambio
        
        DineroEnviado.objects.create(
            destino=destino,
            monto_euros=monto_euros,
            monto_soles=monto_soles,
            tasa_cambio=tasa_cambio
        )
        return redirect('dinero_enviado')
    
    return render(request, 'agregar_envio.html', {'tasa_cambio': tasa_cambio})


def vaciar_historial_view(request):
    total_envios = DineroEnviado.objects.count()
    
    if request.method == 'POST':
        DineroEnviado.objects.all().delete()
        return redirect('dinero_enviado')
    
    return render(request, 'vaciar_historial.html', {'total_envios': total_envios})


def gestionar_estado_view(request, persona):
    gastos = Gasto.objects.filter(persona=persona)
    persona_display = dict(Gasto.PERSONAS).get(persona, persona)
    
    if request.method == 'POST':
        for gasto in gastos:
            nuevo_estado = request.POST.get(f'estado_{gasto.id}')
            if nuevo_estado:
                gasto.estado = nuevo_estado
                gasto.save()
        return redirect('gastos')
    
    return render(request, 'gestionar_estado.html', {
        'gastos': gastos,
        'persona': persona,
        'persona_display': persona_display,
    })
