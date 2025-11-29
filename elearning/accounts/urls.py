from django.urls import path
from .views import volverse_teacher

urlpatterns = [
    path('ser-instructor/', volverse_teacher, name="volverse_teacher"),
]
