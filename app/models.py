from django.db import models

# Create your models here.

class Evento(models.Model):
    TIPO_CHOICES = [
        ('evento', 'Solo Evento'),
        ('torneo', 'Evento + Torneo'),
    ]
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    lugar = models.CharField(max_length=100)
    equipos_participantes = models.IntegerField(default=0, blank=True)
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='evento')
    descripcion = models.TextField(blank=True, default='')
    def __str__(self):
        return self.nombre
    
    @property
    def es_torneo(self):
        return self.tipo == 'torneo'
    
class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    gimnasio = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    posicion = models.CharField(max_length=50)
    numero = models.IntegerField()
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Partido(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    equipo_local = models.ForeignKey(Equipo, related_name='equipo_local', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='equipo_visitante', on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    resultado = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} - {self.fecha_hora}"

class Gastos (models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    def __str__(self):
        return f"{self.descripcion} - {self.monto}"

class BoletaGasto(models.Model):
    gasto = models.ForeignKey(Gastos, on_delete=models.CASCADE, related_name='boletas')
    archivo = models.FileField(upload_to='boletas/%Y/%m/')
    descripcion = models.CharField(max_length=200, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Boleta: {self.descripcion or self.archivo.name} - {self.gasto}"

    @property
    def es_imagen(self):
        extensiones_imagen = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        return any(self.archivo.name.lower().endswith(ext) for ext in extensiones_imagen)

class Estado (models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class BracketMatch(models.Model):
    """Representa un partido dentro del bracket/cuadro de un torneo."""
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='bracket_matches')
    ronda = models.IntegerField()  # 1 = primera ronda, 2 = segunda, etc.
    posicion = models.IntegerField()  # posición dentro de la ronda (0, 1, 2, ...)
    equipo1_nombre = models.CharField(max_length=100, blank=True, default='')
    equipo2_nombre = models.CharField(max_length=100, blank=True, default='')
    ganador_nombre = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['ronda', 'posicion']
        unique_together = ['evento', 'ronda', 'posicion']

    def __str__(self):
        return f"Ronda {self.ronda} - Pos {self.posicion}: {self.equipo1_nombre} vs {self.equipo2_nombre}"