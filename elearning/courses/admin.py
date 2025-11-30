from django.contrib import admin
from .models import Curso, Leccion, Enrollment, Quiz, Pregunta, Opcion, IntentoCuestionario, RespuestaEstudiante, Notificacion


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'instructor', 'fecha_creacion']
    search_fields = ['titulo', 'instructor']
    list_filter = ['fecha_creacion']


@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'tipo', 'orden', 'fecha_creacion']
    list_filter = ['tipo', 'curso']
    search_fields = ['titulo', 'curso__titulo']
    ordering = ['curso', 'orden']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'curso', 'fecha_inscripcion', 'completado']
    list_filter = ['completado', 'fecha_inscripcion']
    search_fields = ['estudiante__username', 'curso__titulo']


# ========== ADMIN PARA QUIZZES ==========

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 4
    fields = ['texto', 'es_correcta', 'orden']


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'quiz', 'puntos', 'orden']
    list_filter = ['quiz']
    search_fields = ['texto', 'quiz__titulo']
    inlines = [OpcionInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'puntaje_minimo', 'intentos_maximos', 'deadline', 'activo']
    list_filter = ['activo', 'curso', 'fecha_creacion']
    search_fields = ['titulo', 'curso__titulo']
    ordering = ['curso', 'orden']


@admin.register(IntentoCuestionario)
class IntentoCuestionarioAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'quiz', 'porcentaje', 'aprobado', 'fecha_inicio', 'completado']
    list_filter = ['aprobado', 'completado', 'fecha_inicio']
    search_fields = ['estudiante__username', 'quiz__titulo']
    ordering = ['-fecha_inicio']


@admin.register(RespuestaEstudiante)
class RespuestaEstudianteAdmin(admin.ModelAdmin):
    list_display = ['intento', 'pregunta', 'opcion_seleccionada', 'es_correcta']
    list_filter = ['fecha_respuesta']
    search_fields = ['intento__estudiante__username', 'pregunta__texto']


# ========== ADMIN PARA NOTIFICACIONES ==========

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'titulo', 'leida', 'fecha_creacion']
    list_filter = ['tipo', 'leida', 'fecha_creacion']
    search_fields = ['usuario__username', 'titulo', 'mensaje']
    ordering = ['-fecha_creacion']
    
    def marcar_como_leidas(self, request, queryset):
        queryset.update(leida=True)
    marcar_como_leidas.short_description = "Marcar seleccionadas como leídas"
    
    actions = [marcar_como_leidas]