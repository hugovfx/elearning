from django import forms
from .models import Curso, Leccion, Quiz, Pregunta, Opcion


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo', 'descripcion', 'instructor', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'instructor': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }


class LeccionForm(forms.ModelForm):
    class Meta:
        model = Leccion
        fields = ['titulo', 'descripcion', 'tipo', 'orden', 'video_url', 'documento', 'contenido_texto']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/watch?v=...'}),
            'documento': forms.FileInput(attrs={'class': 'form-control'}),
            'contenido_texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        video_url = cleaned_data.get('video_url')
        documento = cleaned_data.get('documento')
        contenido_texto = cleaned_data.get('contenido_texto')
        
        if tipo == 'video' and not video_url:
            raise forms.ValidationError('Debes proporcionar una URL de video')
        elif tipo == 'documento' and not documento:
            raise forms.ValidationError('Debes subir un documento')
        elif tipo == 'texto' and not contenido_texto:
            raise forms.ValidationError('Debes escribir el contenido de texto')
        
        return cleaned_data


# ========== FORMULARIOS PARA QUIZZES ==========

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['titulo', 'descripcion', 'puntaje_minimo', 'intentos_maximos', 'tiempo_limite', 'deadline', 'orden', 'activo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Examen Final'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del quiz'}),
            'puntaje_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'intentos_maximos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'tiempo_limite': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Minutos (opcional)'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'puntaje_minimo': 'Puntaje mínimo para aprobar (%)',
            'intentos_maximos': 'Intentos máximos permitidos',
            'tiempo_limite': 'Tiempo límite (minutos)',
            'deadline': 'Fecha límite',
        }


class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto', 'puntos', 'orden']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '¿Cuál es la pregunta?'}),
            'puntos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class OpcionForm(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ['texto', 'es_correcta', 'orden']
        widgets = {
            'texto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opción de respuesta'}),
            'es_correcta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        labels = {
            'es_correcta': '¿Es correcta?',
        }