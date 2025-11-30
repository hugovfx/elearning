from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, Leccion, Enrollment
from .forms import CursoForm, LeccionForm


def home(request):
    cursos = Curso.objects.all()
    return render(request, 'courses/home.html', {"cursos": cursos})


@login_required
def crear_curso(request):
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para crear cursos')
        return redirect('home')

    if request.method == "POST":
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save()
            messages.success(request, f'Curso "{curso.titulo}" creado exitosamente')
            return redirect('detalle_curso', course_id=curso.id)
    else:
        form = CursoForm()

    return render(request, 'courses/crear_curso.html', {"form": form})


def detalle_curso(request, course_id):
    curso = get_object_or_404(Curso, id=course_id)
    lecciones = curso.lecciones.all()
    
    # Verificar si el usuario está inscrito
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(estudiante=request.user, curso=curso).exists()
    
    # Verificar si es el instructor o admin
    puede_editar = False
    if request.user.is_authenticated and request.user.role in ['teacher', 'admin']:
        puede_editar = True

    return render(request, "courses/detalle_curso.html", {
        "course": curso,
        "lessons": lecciones,
        "is_enrolled": is_enrolled,
        "puede_editar": puede_editar,
    })


@login_required
def agregar_leccion(request, course_id):
    curso = get_object_or_404(Curso, id=course_id)
    
    # Solo instructores y admins pueden agregar lecciones
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para agregar lecciones')
        return redirect('detalle_curso', course_id=curso.id)
    
    if request.method == "POST":
        form = LeccionForm(request.POST, request.FILES)
        if form.is_valid():
            leccion = form.save(commit=False)
            leccion.curso = curso
            leccion.save()
            messages.success(request, f'Lección "{leccion.titulo}" agregada exitosamente')
            return redirect('detalle_curso', course_id=curso.id)
    else:
        form = LeccionForm()
    
    return render(request, 'courses/agregar_leccion.html', {
        'form': form,
        'curso': curso
    })


@login_required
def editar_leccion(request, leccion_id):
    leccion = get_object_or_404(Leccion, id=leccion_id)
    curso = leccion.curso
    
    # Solo instructores y admins pueden editar
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para editar lecciones')
        return redirect('detalle_curso', course_id=curso.id)
    
    if request.method == "POST":
        form = LeccionForm(request.POST, request.FILES, instance=leccion)
        if form.is_valid():
            form.save()
            messages.success(request, f'Lección "{leccion.titulo}" actualizada')
            return redirect('detalle_curso', course_id=curso.id)
    else:
        form = LeccionForm(instance=leccion)
    
    return render(request, 'courses/editar_leccion.html', {
        'form': form,
        'leccion': leccion,
        'curso': curso
    })


@login_required
def eliminar_leccion(request, leccion_id):
    leccion = get_object_or_404(Leccion, id=leccion_id)
    curso = leccion.curso
    
    # Solo instructores y admins pueden eliminar
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, 'No tienes permiso para eliminar lecciones')
        return redirect('detalle_curso', course_id=curso.id)
    
    if request.method == "POST":
        titulo = leccion.titulo
        leccion.delete()
        messages.success(request, f'Lección "{titulo}" eliminada')
        return redirect('detalle_curso', course_id=curso.id)
    
    return render(request, 'courses/eliminar_leccion.html', {
        'leccion': leccion,
        'curso': curso
    })


@login_required
def inscribirse_curso(request, course_id):
    curso = get_object_or_404(Curso, id=course_id)
    
    # Solo estudiantes pueden inscribirse
    if request.user.role != 'student':
        messages.warning(request, 'Solo los estudiantes pueden inscribirse a cursos')
        return redirect('detalle_curso', course_id=curso.id)
    
    # Verificar si ya está inscrito
    if Enrollment.objects.filter(estudiante=request.user, curso=curso).exists():
        messages.info(request, 'Ya estás inscrito en este curso')
        return redirect('detalle_curso', course_id=curso.id)
    
    # Crear inscripción
    Enrollment.objects.create(estudiante=request.user, curso=curso)
    messages.success(request, f'Te has inscrito exitosamente en "{curso.titulo}"')
    return redirect('detalle_curso', course_id=curso.id)


@login_required
def mis_cursos(request):
    """Vista de cursos en los que el estudiante está inscrito"""
    if request.user.role != 'student':
        messages.warning(request, 'Esta sección es solo para estudiantes')
        return redirect('home')
    
    inscripciones = Enrollment.objects.filter(estudiante=request.user).select_related('curso')
    
    return render(request, 'courses/mis_cursos.html', {
        'inscripciones': inscripciones
    })