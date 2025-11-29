from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Curso
from .forms import CursoForm


def home(request):
    cursos = Curso.objects.all()
    return render(request, 'courses/home.html', {"cursos": cursos})


@login_required
def crear_curso(request):
    if request.user.role not in ['teacher', 'admin']:
        return redirect('home')  # no tiene permiso

    if request.method == "POST":
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save()
            return redirect('detalle_curso', course_id=curso.id)
    else:
        form = CursoForm()

    return render(request, 'courses/crear_curso.html', {"form": form})


def detalle_curso(request, course_id):
    curso = get_object_or_404(Curso, id=course_id)

    # Por ahora no hay sistema de lecciones ni inscripciones
    lessons = []
    is_enrolled = False

    return render(request, "courses/detalle_curso.html", {
        "course": curso,    
        "lessons": lessons,
        "is_enrolled": is_enrolled,
    })
