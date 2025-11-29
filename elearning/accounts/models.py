from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('student', 'Estudiante'),
        ('teacher', 'Instructor'),
        ('admin', 'Administrador'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='student')
