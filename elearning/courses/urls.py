from django.urls import path
from .views import (
    home, 
    crear_curso, 
    detalle_curso,
    agregar_leccion,
    editar_leccion,
    eliminar_leccion,
    inscribirse_curso,
    mis_cursos
)
from .views_quiz import (
    crear_quiz,
    editar_quiz,
    eliminar_quiz,
    detalle_quiz,
    agregar_pregunta,
    editar_pregunta,
    eliminar_pregunta,
    agregar_opcion,
    realizar_quiz,
    responder_quiz,
    resultado_quiz,
)
from .views_notificaciones import (
    mis_notificaciones,
    marcar_leida,
    eliminar_notificacion,
    generar_notificaciones_manual,
)

from .views_calificaciones import (
    calificaciones_curso,
    generar_certificado,
    detalle_estudiante_curso,
)

urlpatterns = [
    # Rutas de cursos
    path('', home, name='home'),
    path('crear/', crear_curso, name='crear_curso'),
    path('<int:course_id>/', detalle_curso, name='detalle_curso'),
    path('<int:course_id>/inscribirse/', inscribirse_curso, name='inscribirse_curso'),
    path('mis-cursos/', mis_cursos, name='mis_cursos'),
    
    # Rutas de lecciones
    path('<int:course_id>/agregar-leccion/', agregar_leccion, name='agregar_leccion'),
    path('leccion/<int:leccion_id>/editar/', editar_leccion, name='editar_leccion'),
    path('leccion/<int:leccion_id>/eliminar/', eliminar_leccion, name='eliminar_leccion'),
    
    # Rutas de quizzes
    path('<int:course_id>/crear-quiz/', crear_quiz, name='crear_quiz'),
    path('quiz/<int:quiz_id>/', detalle_quiz, name='detalle_quiz'),
    path('quiz/<int:quiz_id>/editar/', editar_quiz, name='editar_quiz'),
    path('quiz/<int:quiz_id>/eliminar/', eliminar_quiz, name='eliminar_quiz'),
    path('quiz/<int:quiz_id>/realizar/', realizar_quiz, name='realizar_quiz'),
    
    # Rutas de preguntas
    path('quiz/<int:quiz_id>/agregar-pregunta/', agregar_pregunta, name='agregar_pregunta'),
    path('pregunta/<int:pregunta_id>/editar/', editar_pregunta, name='editar_pregunta'),
    path('pregunta/<int:pregunta_id>/eliminar/', eliminar_pregunta, name='eliminar_pregunta'),
    path('pregunta/<int:pregunta_id>/agregar-opcion/', agregar_opcion, name='agregar_opcion'),
    
    # Rutas de intentos
    path('intento/<int:intento_id>/responder/', responder_quiz, name='responder_quiz'),
    path('intento/<int:intento_id>/resultado/', resultado_quiz, name='resultado_quiz'),
    
    # Rutas de notificaciones
    path('notificaciones/', mis_notificaciones, name='mis_notificaciones'),
    path('notificacion/<int:notificacion_id>/marcar-leida/', marcar_leida, name='marcar_leida'),
    path('notificacion/<int:notificacion_id>/eliminar/', eliminar_notificacion, name='eliminar_notificacion'),
    path('generar-notificaciones/', generar_notificaciones_manual, name='generar_notificaciones_manual'),

    # Rutas de calificaciones
    path('<int:course_id>/calificaciones/', calificaciones_curso, name='calificaciones_curso'),
    path('<int:course_id>/certificado/<int:student_id>/', generar_certificado, name='generar_certificado'),
    path('<int:course_id>/estudiante/<int:student_id>/', detalle_estudiante_curso, name='detalle_estudiante_curso'),
]