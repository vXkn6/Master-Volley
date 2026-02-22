from django import forms
from .models import BoletaGasto
from .models import Gastos
from .models import Evento
from .models import Partido

class BoletaGastoForm(forms.ModelForm):
    class Meta:
        model = BoletaGasto
        fields = ['gasto', 'archivo', 'descripcion']

class GastosForm(forms.ModelForm):
    class Meta:
        model = Gastos
        fields = ['evento', 'descripcion', 'monto', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
        
class PartidoForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ['evento', 'equipo_local', 'equipo_visitante', 'fecha_hora', 'resultado']

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'fecha', 'lugar', 'tipo', 'equipos_participantes', 'estado', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'tipo': forms.Select(attrs={'id': 'id_tipo', 'onchange': 'toggleEquipos()'}),
        }
        
