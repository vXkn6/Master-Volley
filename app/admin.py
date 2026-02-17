from django.contrib import admin
from .models import Evento, Equipo, Jugador, Partido, Gastos, BoletaGasto


class BoletaGastoInline(admin.TabularInline):
    model = BoletaGasto
    extra = 1


@admin.register(Gastos)
class GastosAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'monto', 'evento', 'fecha')
    inlines = [BoletaGastoInline]


admin.site.register(Evento)
admin.site.register(Equipo)
admin.site.register(Jugador)
admin.site.register(Partido)
admin.site.register(BoletaGasto)
