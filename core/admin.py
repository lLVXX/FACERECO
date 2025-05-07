from django.contrib import admin
from .models import Sede, Carrera, Profesor, Asignatura, ProfesorAsignatura, Estudiante

admin.site.register(Sede)
admin.site.register(Carrera)
admin.site.register(Profesor)
admin.site.register(Asignatura)
admin.site.register(ProfesorAsignatura)
admin.site.register(Estudiante)
