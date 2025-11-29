from django.urls import path, include
from courses.views import home
from accounts.views import register_view, login_view, logout_view
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls')), # Rutas de la app courses
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('accounts/', include('accounts.urls')), # Rutas adicionales de accounts
]

# El manejo de medios SIEMPRE hasta el final
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
