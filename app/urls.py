from django.urls import path
from .views import home, evento, administrativo, crear_gasto, subir_boleta, registro
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path( '', home, name="home" ),
    path('evento/', evento, name="evento"),
    path('administrativo/', administrativo, name="administrativo"),
    path('administrativo/crear-gasto/', crear_gasto, name="crear_gasto"),
    path('administrativo/subir-boleta/', subir_boleta, name="subir_boleta"),
    path('registro/', registro, name="registro"),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
