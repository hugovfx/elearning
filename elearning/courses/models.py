from django.db import models
from django.conf import settings
from django.utils import timezone


class Curso(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    instructor = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='cursos/', blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'


class Leccion(models.Model):
    TIPOS = (
        ('video', '📹 Video'),
        ('documento', '📄 Documento'),
        ('texto', '📝 Texto/Artículo'),
    )
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='texto')
    orden = models.PositiveIntegerField(default=0)
    
    video_url = models.URLField(blank=True, null=True, help_text="URL de YouTube o Vimeo")
    documento = models.FileField(upload_to='lecciones/documentos/', blank=True, null=True)
    contenido_texto = models.TextField(blank=True, help_text="Contenido HTML permitido")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"
    
    class Meta:
        verbose_name = 'Lección'
        verbose_name_plural = 'Lecciones'
        ordering = ['orden', 'fecha_creacion']


class Enrollment(models.Model):
    """Inscripción de estudiantes a cursos"""
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.curso.titulo}"
    
    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        unique_together = ['estudiante', 'curso']


# ========== NUEVOS MODELOS: EVALUACIONES ==========

class Quiz(models.Model):
    """Examen o evaluación de un curso"""
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='quizzes')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    
    # Configuración
    puntaje_minimo = models.PositiveIntegerField(default=70, help_text="Puntaje mínimo para aprobar (%)")
    intentos_maximos = models.PositiveIntegerField(default=3, help_text="Número máximo de intentos permitidos")
    tiempo_limite = models.PositiveIntegerField(null=True, blank=True, help_text="Tiempo límite en minutos (opcional)")
    deadline = models.DateTimeField(null=True, blank=True, help_text="Fecha límite de entrega")
    
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"
    
    def total_preguntas(self):
        return self.preguntas.count()
    
    def esta_disponible(self):
        """Verifica si el quiz está disponible para realizar"""
        if not self.activo:
            return False
        if self.deadline and timezone.now() > self.deadline:
            return False
        return True
    
    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['orden', 'fecha_creacion']


class Pregunta(models.Model):
    """Pregunta de opción múltiple"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.TextField(help_text="Texto de la pregunta")
    puntos = models.PositiveIntegerField(default=1, help_text="Puntos que vale esta pregunta")
    orden = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.quiz.titulo} - Pregunta {self.orden}"
    
    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['orden']


class Opcion(models.Model):
    """Opción de respuesta para una pregunta"""
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.CharField(max_length=300)
    es_correcta = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.pregunta} - {self.texto[:30]}"
    
    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'
        ordering = ['orden']


class IntentoCuestionario(models.Model):
    """Registro de un intento de realizar un quiz"""
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='intentos')
    
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    
    puntaje_obtenido = models.FloatField(default=0)
    puntaje_maximo = models.FloatField(default=0)
    porcentaje = models.FloatField(default=0)
    aprobado = models.BooleanField(default=False)
    
    completado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.quiz.titulo} - Intento {self.fecha_inicio}"
    
    def calcular_resultado(self):
        """Calcula el resultado del intento"""
        respuestas = self.respuestas.all()
        total_puntos = sum([r.pregunta.puntos for r in respuestas])
        puntos_obtenidos = sum([r.pregunta.puntos for r in respuestas if r.es_correcta()])
        
        self.puntaje_obtenido = puntos_obtenidos
        self.puntaje_maximo = total_puntos
        self.porcentaje = (puntos_obtenidos / total_puntos * 100) if total_puntos > 0 else 0
        self.aprobado = self.porcentaje >= self.quiz.puntaje_minimo
        self.completado = True
        self.fecha_finalizacion = timezone.now()
        self.save()
    
    class Meta:
        verbose_name = 'Intento de Cuestionario'
        verbose_name_plural = 'Intentos de Cuestionarios'
        ordering = ['-fecha_inicio']


class RespuestaEstudiante(models.Model):
    """Respuesta de un estudiante a una pregunta específica"""
    intento = models.ForeignKey(IntentoCuestionario, on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.CASCADE)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    
    def es_correcta(self):
        """Verifica si la respuesta seleccionada es correcta"""
        return self.opcion_seleccionada.es_correcta
    
    def __str__(self):
        return f"{self.intento.estudiante.username} - {self.pregunta}"
    
    class Meta:
        verbose_name = 'Respuesta de Estudiante'
        verbose_name_plural = 'Respuestas de Estudiantes'
        unique_together = ['intento', 'pregunta']


# ========== SISTEMA DE NOTIFICACIONES ==========

class Notificacion(models.Model):
    """Notificación para estudiantes sobre deadlines y eventos importantes"""
    TIPOS = (
        ('deadline', '⏰ Deadline próximo'),
        ('nuevo_quiz', '📝 Nuevo quiz disponible'),
        ('resultado', '📊 Resultado de quiz'),
        ('curso', '📚 Actualización de curso'),
    )
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    
    # Referencias opcionales
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.titulo}"
    
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']  # Un estudiante solo puede responder una vez por pregunta en cada intento