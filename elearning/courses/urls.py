from django.urls import path
from .views import home, crear_curso, detalle_curso

urlpatterns = [
    path('', home, name='home'),
    path('crear/', crear_curso, name='crear_curso'),
    path('<int:course_id>/', detalle_curso, name='detalle_curso'),
]

