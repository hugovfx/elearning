from django.db import models

class Curso(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    instructor = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='cursos/', blank=True, null=True)

    def __str__(self):
        return self.titulo
