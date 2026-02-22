import math
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from app.models import Evento, Gastos, BracketMatch, Equipo
from .forms import BoletaGastoForm, GastosForm, EventoForm, PartidoForm

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def evento(request):
    eventos = Evento.objects.select_related('estado').all()
    data = {
        'eventos': eventos,
        'evento_form': EventoForm(),
        }
    return render(request, 'app/evento.html', data)

def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save()
            # Si es torneo, generar el bracket automáticamente
            if evento.es_torneo and evento.equipos_participantes >= 2:
                generar_bracket(evento)
            messages.success(request, 'Evento creado exitosamente.')
        else:
            messages.error(request, 'Error al crear el evento. Revisa los campos.')
    return redirect('evento')


def generar_bracket(evento):
    """Genera las casillas del bracket para un torneo."""
    # Eliminar bracket anterior si existe
    BracketMatch.objects.filter(evento=evento).delete()

    n = evento.equipos_participantes
    # Redondear al siguiente potencia de 2
    rondas_total = math.ceil(math.log2(n)) if n > 1 else 1
    partidos_ronda1 = 2 ** (rondas_total - 1)

    for ronda in range(1, rondas_total + 1):
        partidos_en_ronda = 2 ** (rondas_total - ronda)
        for pos in range(partidos_en_ronda):
            BracketMatch.objects.create(
                evento=evento,
                ronda=ronda,
                posicion=pos,
            )


def obtener_bracket(request, evento_id):
    """API: Devuelve el bracket de un evento en JSON."""
    evento = get_object_or_404(Evento, pk=evento_id)
    matches = evento.bracket_matches.all().order_by('ronda', 'posicion')

    rondas = {}
    for m in matches:
        if m.ronda not in rondas:
            rondas[m.ronda] = []
        rondas[m.ronda].append({
            'id': m.id,
            'ronda': m.ronda,
            'posicion': m.posicion,
            'equipo1': m.equipo1_nombre,
            'equipo2': m.equipo2_nombre,
            'ganador': m.ganador_nombre,
        })

    return JsonResponse({
        'evento_id': evento.id,
        'evento_nombre': evento.nombre,
        'equipos_participantes': evento.equipos_participantes,
        'rondas': rondas,
    })


@require_POST
def actualizar_bracket_match(request, match_id):
    """API: Actualiza un partido del bracket (equipos y ganador)."""
    match = get_object_or_404(BracketMatch, pk=match_id)
    data = json.loads(request.body)

    if 'equipo1' in data:
        match.equipo1_nombre = data['equipo1']
    if 'equipo2' in data:
        match.equipo2_nombre = data['equipo2']
    if 'ganador' in data:
        match.ganador_nombre = data['ganador']
        # Si hay ganador, avanzarlo a la siguiente ronda
        if data['ganador']:
            siguiente_ronda = match.ronda + 1
            siguiente_pos = match.posicion // 2
            try:
                next_match = BracketMatch.objects.get(
                    evento=match.evento,
                    ronda=siguiente_ronda,
                    posicion=siguiente_pos,
                )
                # Determinar si va como equipo1 o equipo2
                if match.posicion % 2 == 0:
                    next_match.equipo1_nombre = data['ganador']
                else:
                    next_match.equipo2_nombre = data['ganador']
                next_match.save()
            except BracketMatch.DoesNotExist:
                pass  # Es la final, no hay siguiente ronda

    match.save()
    return JsonResponse({'status': 'ok'})


def get_equipos(request):
    """API: Devuelve lista de equipos en JSON."""
    equipos = Equipo.objects.all().order_by('nombre')
    return JsonResponse({
        'equipos': [{'id': e.id, 'nombre': e.nombre, 'ciudad': e.ciudad} for e in equipos]
    })


@require_POST
def crear_equipo_api(request):
    """API: Crea un nuevo equipo y lo devuelve."""
    data = json.loads(request.body)
    nombre = data.get('nombre', '').strip()
    ciudad = data.get('ciudad', '').strip()
    gimnasio = data.get('gimnasio', '').strip()
    if not nombre:
        return JsonResponse({'error': 'El nombre es requerido.'}, status=400)
    equipo = Equipo.objects.create(nombre=nombre, ciudad=ciudad, gimnasio=gimnasio)
    return JsonResponse({'id': equipo.id, 'nombre': equipo.nombre, 'ciudad': equipo.ciudad})


def administrativo(request):
    eventos = Evento.objects.prefetch_related('gastos_set__boletas').all()
    data = {
        'boleta_form': BoletaGastoForm(),
        'gastos_form': GastosForm(),
        'eventos': eventos,
        }
    return render(request, 'app/administrativo.html', data)

def crear_gasto(request):
    if request.method == 'POST':
        form = GastosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto creado exitosamente.')
        else:
            messages.error(request, 'Error al crear el gasto. Revisa los campos.')
    return redirect('administrativo')

def subir_boleta(request):
    if request.method == 'POST':
        form = BoletaGastoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Boleta adjuntada exitosamente.')
        else:
            messages.error(request, 'Error al subir la boleta. Revisa los campos.')
    return redirect('administrativo')

def registro(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

