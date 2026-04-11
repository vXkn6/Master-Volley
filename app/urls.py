from django.urls import path
from .views import (
    home, evento, administrativo, crear_gasto, subir_boleta, registro,
    crear_evento, obtener_bracket, actualizar_bracket_match,
    get_equipos, crear_equipo_api,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name="home"),
    path('evento/', evento, name="evento"),
    path('evento/crear/', crear_evento, name="crear_evento"),
    path('api/bracket/<int:evento_id>/', obtener_bracket, name="obtener_bracket"),
    path('api/bracket/match/<int:match_id>/', actualizar_bracket_match, name="actualizar_bracket_match"),
    path('api/equipos/', get_equipos, name="get_equipos"),
    path('api/equipos/crear/', crear_equipo_api, name="crear_equipo_api"),
    path('administrativo/', administrativo, name="administrativo"),
    path('administrativo/crear-gasto/', crear_gasto, name="crear_gasto"),
    path('administrativo/subir-boleta/', subir_boleta, name="subir_boleta"),
    path('registro/', registro, name="registro"),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
