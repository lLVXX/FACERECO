from django.db import models

class Sede(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    descripcion = models.TextField()
    def __str__(self):
        return self.nombre

class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    horario = models.CharField(max_length=100)  # NUEVO CAMPO
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class ProfesorAsignatura(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profesor', 'asignatura')

    def __str__(self):
        return f"{self.profesor.nombre} - {self.asignatura.nombre}"

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    asignaturas = models.ManyToManyField(Asignatura)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
