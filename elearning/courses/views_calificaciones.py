from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Avg, Count, Q
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
from .models import Curso, Quiz, IntentoCuestionario, Enrollment
from accounts.models import User


@login_required
def calificaciones_curso(request, course_id):
    """Vista para que el instructor vea las calificaciones de todos los estudiantes"""
    curso = get_object_or_404(Curso, id=course_id)
    
    # Verificar que sea instructor o admin
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para ver estas calificaciones')
        return redirect('detalle_curso', course_id=curso.id)
    
    # Obtener todos los estudiantes inscritos
    inscripciones = Enrollment.objects.filter(curso=curso).select_related('estudiante')
    
    # Obtener todos los quizzes del curso
    quizzes = curso.quizzes.all().order_by('orden')
    
    # Preparar datos de calificaciones
    datos_estudiantes = []
    total_aprobados = 0
    total_reprobados = 0
    
    for inscripcion in inscripciones:
        estudiante = inscripcion.estudiante
        
        # Obtener calificaciones de cada quiz
        calificaciones_quizzes = []
        suma_porcentajes = 0
        quizzes_completados = 0
        
        for quiz in quizzes:
            # Obtener el mejor intento del estudiante en este quiz
            mejor_intento = IntentoCuestionario.objects.filter(
                estudiante=estudiante,
                quiz=quiz,
                completado=True
            ).order_by('-porcentaje').first()
            
            if mejor_intento:
                calificaciones_quizzes.append({
                    'quiz': quiz,
                    'porcentaje': mejor_intento.porcentaje,
                    'aprobado': mejor_intento.aprobado,
                    'intento': mejor_intento
                })
                suma_porcentajes += mejor_intento.porcentaje
                quizzes_completados += 1
            else:
                calificaciones_quizzes.append({
                    'quiz': quiz,
                    'porcentaje': None,
                    'aprobado': False,
                    'intento': None
                })
        
        # Calcular promedio
        promedio = suma_porcentajes / quizzes_completados if quizzes_completados > 0 else 0
        aprobado_curso = promedio >= 70 and quizzes_completados == quizzes.count()
        
        if aprobado_curso:
            total_aprobados += 1
        else:
            total_reprobados += 1
        
        datos_estudiantes.append({
            'estudiante': estudiante,
            'inscripcion': inscripcion,
            'calificaciones': calificaciones_quizzes,
            'promedio': promedio,
            'quizzes_completados': quizzes_completados,
            'total_quizzes': quizzes.count(),
            'aprobado': aprobado_curso
        })
    
    return render(request, 'courses/calificaciones_curso.html', {
        'curso': curso,
        'quizzes': quizzes,
        'datos_estudiantes': datos_estudiantes,
        'total_estudiantes': inscripciones.count(),
        'total_aprobados': total_aprobados,
        'total_reprobados': total_reprobados,
    })


@login_required
def generar_certificado(request, course_id, student_id):
    """Generar certificado PDF para un estudiante"""
    curso = get_object_or_404(Curso, id=course_id)
    estudiante = get_object_or_404(User, id=student_id)
    
    # Verificar permisos
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para generar certificados')
        return redirect('home')
    
    # Verificar que el estudiante esté inscrito
    inscripcion = get_object_or_404(Enrollment, curso=curso, estudiante=estudiante)
    
    # Calcular promedio
    quizzes = curso.quizzes.all()
    suma_porcentajes = 0
    quizzes_completados = 0
    
    for quiz in quizzes:
        mejor_intento = IntentoCuestionario.objects.filter(
            estudiante=estudiante,
            quiz=quiz,
            completado=True
        ).order_by('-porcentaje').first()
        
        if mejor_intento:
            suma_porcentajes += mejor_intento.porcentaje
            quizzes_completados += 1
    
    promedio = suma_porcentajes / quizzes_completados if quizzes_completados > 0 else 0
    aprobado = promedio >= 70 and quizzes_completados == quizzes.count()
    
    if not aprobado:
        messages.error(request, f'{estudiante.username} no ha aprobado el curso')
        return redirect('calificaciones_curso', course_id=curso.id)
    
    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{estudiante.username}_{curso.titulo}.pdf"'
    
    # Crear el PDF con ReportLab
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    
    # Configurar el certificado
    p.setFont("Helvetica-Bold", 36)
    p.drawCentredString(width/2, height - 2*inch, "CERTIFICADO")
    
    p.setFont("Helvetica", 16)
    p.drawCentredString(width/2, height - 2.8*inch, "Se otorga a:")
    
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width/2, height - 3.5*inch, estudiante.get_full_name() or estudiante.username)
    
    p.setFont("Helvetica", 16)
    p.drawCentredString(width/2, height - 4.2*inch, "Por haber completado exitosamente el curso:")
    
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width/2, height - 4.9*inch, curso.titulo)
    
    p.setFont("Helvetica", 14)
    p.drawCentredString(width/2, height - 5.6*inch, f"Con un promedio de: {promedio:.1f}%")
    
    p.setFont("Helvetica-Oblique", 12)
    p.drawCentredString(width/2, height - 6.3*inch, f"Instructor: {curso.instructor}")
    p.drawCentredString(width/2, height - 6.7*inch, f"Fecha: {datetime.now().strftime('%d de %B de %Y')}")
    
    # Línea decorativa
    p.line(2*inch, height - 7.5*inch, width - 2*inch, height - 7.5*inch)
    
    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, 1*inch, "E-learning Platform - Certificado de Finalización")
    
    p.showPage()
    p.save()
    
    return response


@login_required
def detalle_estudiante_curso(request, course_id, student_id):
    """Ver el detalle completo de un estudiante en un curso"""
    curso = get_object_or_404(Curso, id=course_id)
    estudiante = get_object_or_404(User, id=student_id)
    
    # Verificar permisos
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para ver este detalle')
        return redirect('home')
    
    # Verificar inscripción
    inscripcion = get_object_or_404(Enrollment, curso=curso, estudiante=estudiante)
    
    # Obtener todos los intentos del estudiante
    quizzes = curso.quizzes.all().order_by('orden')
    datos_quizzes = []
    
    for quiz in quizzes:
        intentos = IntentoCuestionario.objects.filter(
            estudiante=estudiante,
            quiz=quiz,
            completado=True
        ).order_by('-fecha_inicio')
        
        mejor_intento = intentos.order_by('-porcentaje').first() if intentos.exists() else None
        
        datos_quizzes.append({
            'quiz': quiz,
            'intentos': intentos,
            'mejor_intento': mejor_intento,
            'total_intentos': intentos.count()
        })
    
    # Calcular estadísticas
    intentos_totales = IntentoCuestionario.objects.filter(
        estudiante=estudiante,
        quiz__curso=curso,
        completado=True
    )
    
    promedio_general = intentos_totales.aggregate(Avg('porcentaje'))['porcentaje__avg'] or 0
    
    return render(request, 'courses/detalle_estudiante_curso.html', {
        'curso': curso,
        'estudiante': estudiante,
        'inscripcion': inscripcion,
        'datos_quizzes': datos_quizzes,
        'promedio_general': promedio_general,
    })