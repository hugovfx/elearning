from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def register_view(request):
    """Vista de registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido {user.username}')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = RegisterForm()
    
    return render(request, "register.html", {"form": form})


def login_view(request):
    """Vista de inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    
    return render(request, "login.html", {"form": form})


def logout_view(request):
    """Vista de cierre de sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('home')


@login_required
def volverse_teacher(request):
    """Permitir a un estudiante convertirse en instructor"""
    user = request.user
    
    if user.role == 'teacher':
        messages.info(request, 'Ya eres instructor')
        return redirect('home')
    
    if user.role == 'admin':
        messages.warning(request, 'Los administradores ya tienen todos los permisos')
        return redirect('home')
    
    user.role = 'teacher'
    user.save()
    messages.success(request, '¡Felicidades! Ahora eres instructor y puedes crear cursos')
    
    return redirect('home')