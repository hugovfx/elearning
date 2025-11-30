from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Curso, Quiz, Pregunta, Opcion, IntentoCuestionario, RespuestaEstudiante, Enrollment
from .forms import QuizForm, PreguntaForm, OpcionForm


@login_required
def crear_quiz(request, course_id):
    """Crear un nuevo quiz para un curso"""
    curso = get_object_or_404(Curso, id=course_id)
    
    # Solo instructores y admins
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para crear quizzes')
        return redirect('detalle_curso', course_id=curso.id)
    
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.curso = curso
            quiz.save()
            messages.success(request, f'Quiz "{quiz.titulo}" creado. Ahora agrega preguntas.')
            return redirect('agregar_pregunta', quiz_id=quiz.id)
    else:
        form = QuizForm()
    
    return render(request, 'courses/crear_quiz.html', {
        'form': form,
        'curso': curso
    })


@login_required
def editar_quiz(request, quiz_id):
    """Editar un quiz existente"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    curso = quiz.curso
    
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para editar quizzes')
        return redirect('detalle_curso', course_id=curso.id)
    
    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, f'Quiz "{quiz.titulo}" actualizado')
            return redirect('detalle_quiz', quiz_id=quiz.id)
    else:
        form = QuizForm(instance=quiz)
    
    return render(request, 'courses/editar_quiz.html', {
        'form': form,
        'quiz': quiz,
        'curso': curso
    })


@login_required
def eliminar_quiz(request, quiz_id):
    """Eliminar un quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    curso = quiz.curso
    
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para eliminar quizzes')
        return redirect('detalle_curso', course_id=curso.id)
    
    if request.method == "POST":
        titulo = quiz.titulo
        quiz.delete()
        messages.success(request, f'Quiz "{titulo}" eliminado')
        return redirect('detalle_curso', course_id=curso.id)
    
    return render(request, 'courses/eliminar_quiz.html', {
        'quiz': quiz,
        'curso': curso
    })


@login_required
def detalle_quiz(request, quiz_id):
    """Ver detalles de un quiz y gestionar preguntas"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    curso = quiz.curso
    preguntas = quiz.preguntas.all().prefetch_related('opciones')
    
    # Verificar si el usuario está inscrito
    is_enrolled = Enrollment.objects.filter(estudiante=request.user, curso=curso).exists()
    puede_editar = request.user.role in ['teacher', 'admin']
    
    # Obtener intentos del estudiante
    intentos = []
    puede_intentar = False
    if request.user.role == 'student' and is_enrolled:
        intentos = IntentoCuestionario.objects.filter(
            estudiante=request.user,
            quiz=quiz
        ).order_by('-fecha_inicio')
        
        # Verificar si puede hacer un nuevo intento
        intentos_realizados = intentos.filter(completado=True).count()
        puede_intentar = (
            quiz.esta_disponible() and
            intentos_realizados < quiz.intentos_maximos
        )
    
    return render(request, 'courses/detalle_quiz.html', {
        'quiz': quiz,
        'curso': curso,
        'preguntas': preguntas,
        'is_enrolled': is_enrolled,
        'puede_editar': puede_editar,
        'intentos': intentos,
        'puede_intentar': puede_intentar,
    })


@login_required
def agregar_pregunta(request, quiz_id):
    """Agregar una nueva pregunta a un quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para agregar preguntas')
        return redirect('detalle_quiz', quiz_id=quiz.id)
    
    if request.method == "POST":
        form = PreguntaForm(request.POST)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.quiz = quiz
            pregunta.save()
            messages.success(request, 'Pregunta agregada. Ahora agrega las opciones de respuesta.')
            return redirect('agregar_opcion', pregunta_id=pregunta.id)
    else:
        form = PreguntaForm()
    
    return render(request, 'courses/agregar_pregunta.html', {
        'form': form,
        'quiz': quiz
    })


@login_required
def editar_pregunta(request, pregunta_id):
    """Editar una pregunta"""
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    quiz = pregunta.quiz
    
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para editar preguntas')
        return redirect('detalle_quiz', quiz_id=quiz.id)
    
    if request.method == "POST":
        form = PreguntaForm(request.POST, instance=pregunta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pregunta actualizada')
            return redirect('detalle_quiz', quiz_id=quiz.id)
    else:
        form = PreguntaForm(instance=pregunta)
    
    return render(request, 'courses/editar_pregunta.html', {
        'form': form,
        'pregunta': pregunta,
        'quiz': quiz
    })


@login_required
def eliminar_pregunta(request, pregunta_id):
    """Eliminar una pregunta"""
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    quiz = pregunta.quiz
    
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para eliminar preguntas')
        return redirect('detalle_quiz', quiz_id=quiz.id)
    
    if request.method == "POST":
        pregunta.delete()
        messages.success(request, 'Pregunta eliminada')
        return redirect('detalle_quiz', quiz_id=quiz.id)
    
    return render(request, 'courses/eliminar_pregunta.html', {
        'pregunta': pregunta,
        'quiz': quiz
    })


@login_required
def agregar_opcion(request, pregunta_id):
    """Agregar opciones de respuesta a una pregunta"""
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    quiz = pregunta.quiz
    opciones_existentes = pregunta.opciones.all()
    
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para agregar opciones')
        return redirect('detalle_quiz', quiz_id=quiz.id)
    
    if request.method == "POST":
        form = OpcionForm(request.POST)
        if form.is_valid():
            opcion = form.save(commit=False)
            opcion.pregunta = pregunta
            opcion.save()
            messages.success(request, 'Opción agregada')
            
            # Verificar si hay al menos una opción correcta
            if opciones_existentes.count() >= 3:
                return redirect('detalle_quiz', quiz_id=quiz.id)
            return redirect('agregar_opcion', pregunta_id=pregunta.id)
    else:
        form = OpcionForm()
    
    return render(request, 'courses/agregar_opcion.html', {
        'form': form,
        'pregunta': pregunta,
        'quiz': quiz,
        'opciones_existentes': opciones_existentes
    })


@login_required
def realizar_quiz(request, quiz_id):
    """Realizar un intento del quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    curso = quiz.curso
    
    # Verificar inscripción
    if not Enrollment.objects.filter(estudiante=request.user, curso=curso).exists():
        messages.error(request, 'Debes estar inscrito en el curso para realizar el quiz')
        return redirect('detalle_curso', course_id=curso.id)
    
    # Verificar disponibilidad
    if not quiz.esta_disponible():
        messages.error(request, 'Este quiz ya no está disponible')
        return redirect('detalle_quiz', quiz_id=quiz.id)
    
    # Verificar intentos
    intentos_previos = IntentoCuestionario.objects.filter(
        estudiante=request.user,
        quiz=quiz,
        completado=True
    ).count()
    
    if intentos_previos >= quiz.intentos_maximos:
        messages.warning(request, 'Has agotado todos tus intentos para este quiz')
        return redirect('detalle_quiz', quiz_id=quiz.id)
    
    # Crear nuevo intento
    intento = IntentoCuestionario.objects.create(
        estudiante=request.user,
        quiz=quiz
    )
    
    return redirect('responder_quiz', intento_id=intento.id)


@login_required
def responder_quiz(request, intento_id):
    """Interfaz para responder el quiz"""
    intento = get_object_or_404(IntentoCuestionario, id=intento_id)
    quiz = intento.quiz
    
    # Verificar que sea el dueño del intento
    if intento.estudiante != request.user:
        messages.error(request, 'No tienes permiso para ver este intento')
        return redirect('home')
    
    if intento.completado:
        messages.info(request, 'Ya completaste este intento')
        return redirect('resultado_quiz', intento_id=intento.id)
    
    preguntas = quiz.preguntas.all().prefetch_related('opciones')
    
    if request.method == "POST":
        # Guardar respuestas
        for pregunta in preguntas:
            opcion_id = request.POST.get(f'pregunta_{pregunta.id}')
            if opcion_id:
                opcion = get_object_or_404(Opcion, id=opcion_id)
                RespuestaEstudiante.objects.update_or_create(
                    intento=intento,
                    pregunta=pregunta,
                    defaults={'opcion_seleccionada': opcion}
                )
        
        # Calcular resultado
        intento.calcular_resultado()
        messages.success(request, 'Quiz completado. Aquí están tus resultados.')
        return redirect('resultado_quiz', intento_id=intento.id)
    
    return render(request, 'courses/responder_quiz.html', {
        'intento': intento,
        'quiz': quiz,
        'preguntas': preguntas
    })


@login_required
def resultado_quiz(request, intento_id):
    """Ver el resultado de un intento"""
    intento = get_object_or_404(IntentoCuestionario, id=intento_id)
    
    # Verificar permisos
    if intento.estudiante != request.user and request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para ver este resultado')
        return redirect('home')
    
    respuestas = intento.respuestas.all().select_related('pregunta', 'opcion_seleccionada')
    
    return render(request, 'courses/resultado_quiz.html', {
        'intento': intento,
        'respuestas': respuestas
    })