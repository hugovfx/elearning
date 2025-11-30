from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Notificacion, Quiz, Enrollment


@login_required
def mis_notificaciones(request):
    """Vista de todas las notificaciones del usuario"""
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    
    # Marcar como leídas si el usuario lo solicita
    if request.GET.get('marcar_leidas'):
        notificaciones.filter(leida=False).update(leida=True)
        messages.success(request, 'Todas las notificaciones marcadas como leídas')
        return redirect('mis_notificaciones')
    
    return render(request, 'courses/notificaciones.html', {
        'notificaciones': notificaciones
    })


@login_required
def marcar_leida(request, notificacion_id):
    """Marcar una notificación como leída"""
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.leida = True
    notificacion.save()
    
    # Redirigir al contenido relacionado si existe
    if notificacion.quiz:
        return redirect('detalle_quiz', quiz_id=notificacion.quiz.id)
    elif notificacion.curso:
        return redirect('detalle_curso', course_id=notificacion.curso.id)
    
    return redirect('mis_notificaciones')


@login_required
def eliminar_notificacion(request, notificacion_id):
    """Eliminar una notificación"""
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.delete()
    messages.success(request, 'Notificación eliminada')
    return redirect('mis_notificaciones')


def generar_notificaciones_deadlines():
    """
    Función auxiliar para generar notificaciones de deadlines próximos.
    Se puede llamar periódicamente con un cron job o Celery.
    """
    ahora = timezone.now()
    en_24_horas = ahora + timedelta(hours=24)
    en_3_dias = ahora + timedelta(days=3)
    
    # Buscar quizzes con deadline en las próximas 24 horas
    quizzes_urgentes = Quiz.objects.filter(
        deadline__gte=ahora,
        deadline__lte=en_24_horas,
        activo=True
    )
    
    for quiz in quizzes_urgentes:
        # Obtener estudiantes inscritos en el curso
        estudiantes = Enrollment.objects.filter(curso=quiz.curso).values_list('estudiante', flat=True)
        
        for estudiante_id in estudiantes:
            # Verificar si ya existe una notificación similar reciente
            existe = Notificacion.objects.filter(
                usuario_id=estudiante_id,
                quiz=quiz,
                tipo='deadline',
                fecha_creacion__gte=ahora - timedelta(hours=12)
            ).exists()
            
            if not existe:
                Notificacion.objects.create(
                    usuario_id=estudiante_id,
                    tipo='deadline',
                    titulo=f'⏰ Deadline urgente: {quiz.titulo}',
                    mensaje=f'El quiz "{quiz.titulo}" vence en menos de 24 horas. ¡Apúrate!',
                    quiz=quiz,
                    curso=quiz.curso
                )
    
    # Buscar quizzes con deadline en 3 días
    quizzes_proximos = Quiz.objects.filter(
        deadline__gte=en_24_horas,
        deadline__lte=en_3_dias,
        activo=True
    )
    
    for quiz in quizzes_proximos:
        estudiantes = Enrollment.objects.filter(curso=quiz.curso).values_list('estudiante', flat=True)
        
        for estudiante_id in estudiantes:
            existe = Notificacion.objects.filter(
                usuario_id=estudiante_id,
                quiz=quiz,
                tipo='deadline',
                fecha_creacion__gte=ahora - timedelta(days=2)
            ).exists()
            
            if not existe:
                Notificacion.objects.create(
                    usuario_id=estudiante_id,
                    tipo='deadline',
                    titulo=f'📅 Próximo deadline: {quiz.titulo}',
                    mensaje=f'El quiz "{quiz.titulo}" vence en 3 días.',
                    quiz=quiz,
                    curso=quiz.curso
                )


@login_required
def generar_notificaciones_manual(request):
    """Vista para generar notificaciones manualmente (solo para testing)"""
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para esta acción')
        return redirect('home')
    
    generar_notificaciones_deadlines()
    messages.success(request, 'Notificaciones de deadlines generadas')
    return redirect('mis_notificaciones')