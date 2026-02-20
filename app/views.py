from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from app.models import Evento, Gastos
from .forms import BoletaGastoForm, GastosForm, EventoForm, PartidoForm

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def evento(request):
    eventos = Evento.objects.all()
    data = {
        'eventos': eventos
        }
    return render(request, 'app/evento.html', data)

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

