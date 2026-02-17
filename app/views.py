from django.shortcuts import render

from app.models import Evento, Gastos

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def evento(request):
    eventos = Evento.objects.all()
    data = {
        'eventos': eventos
    
        }
    
    return render(request, 'app/evento.html',data)

def administrativo(request):
    eventos = Evento.objects.prefetch_related('gastos_set__boletas').all()
    return render(request, 'app/administrativo.html', {'eventos': eventos})

