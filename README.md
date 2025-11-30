# 📚 E-Learning Platform

Plataforma de aprendizaje en línea desarrollada con Django que permite a instructores crear cursos, lecciones y evaluaciones, mientras que los estudiantes pueden inscribirse, estudiar y realizar quizzes.

## ✨ Características Principales

### Para Estudiantes
- 👤 Registro e inicio de sesión
- 📚 Explorar y inscribirse a cursos disponibles
- 📖 Acceder a lecciones (videos, documentos, texto)
- 📝 Realizar quizzes con intentos múltiples
- 📊 Ver resultados detallados de evaluaciones
- 🔔 Sistema de notificaciones para deadlines
- 📜 Obtener certificados al aprobar cursos

### Para Instructores
- ➕ Crear y gestionar cursos
- 📹 Agregar lecciones de diferentes tipos (video, documento, texto)
- 🎯 Crear quizzes con preguntas de opción múltiple
- ⏰ Configurar deadlines y límites de tiempo
- 📊 Ver calificaciones de todos los estudiantes
- 📜 Generar certificados PDF para estudiantes aprobados
- 👁️ Ver detalle completo del progreso de cada estudiante

### Funcionalidades del Sistema
- 🔐 Sistema de autenticación con roles (Estudiante, Instructor, Admin)
- 📝 Quizzes con calificación automática
- 🎨 Interfaz responsive con Bootstrap 5
- 📱 Notificaciones en tiempo real
- 🏆 Sistema de certificados PDF
- 📈 Seguimiento de progreso y calificaciones

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 5.2.8
- **Frontend:** Bootstrap 5.3.3, HTML5, CSS3
- **Base de datos:** SQLite (desarrollo)
- **Generación de PDFs:** ReportLab
- **Gestión de imágenes:** Pillow

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio (o descargar el ZIP)
```bash
git clone <url-del-repositorio>
cd elearning
```

### 2. Crear un entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Realizar las migraciones de la base de datos
```bash
python manage.py migrate
```

### 5. Crear un superusuario (administrador)
```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu usuario administrador.

### 6. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

### 7. Acceder a la aplicación

Abre tu navegador y ve a:
- **Aplicación principal:** http://127.0.0.1:8000/
- **Panel de administración:** http://127.0.0.1:8000/admin/

## 👥 Roles de Usuario

### Estudiante (student)
- Rol por defecto al registrarse
- Puede inscribirse a cursos
- Puede realizar quizzes
- Puede convertirse en instructor

### Instructor (teacher)
- Puede crear y gestionar cursos
- Puede crear lecciones y quizzes
- Puede ver calificaciones de estudiantes
- Puede generar certificados

### Administrador (admin)
- Tiene todos los permisos
- Acceso al panel de administración de Django
- Puede gestionar todos los cursos y usuarios

## 📁 Estructura del Proyecto
```
elearning/
├── accounts/                 # App de autenticación y usuarios
│   ├── models.py            # Modelo de usuario personalizado
│   ├── views.py             # Vistas de login, registro, etc.
│   └── forms.py             # Formularios de autenticación
├── courses/                  # App principal de cursos
│   ├── models.py            # Modelos de Curso, Lección, Quiz, etc.
│   ├── views.py             # Vistas de cursos y lecciones
│   ├── views_quiz.py        # Vistas de quizzes
│   ├── views_calificaciones.py  # Vistas de calificaciones
│   ├── views_notificaciones.py  # Vistas de notificaciones
│   ├── forms.py             # Formularios
│   ├── admin.py             # Configuración del admin
│   └── templates/           # Plantillas HTML
├── templates/               # Plantillas base
│   ├── base.html           # Template base
│   ├── login.html          # Página de login
│   └── register.html       # Página de registro
├── media/                   # Archivos subidos (imágenes, documentos)
├── elearning/              # Configuración del proyecto
│   ├── settings.py         # Configuración de Django
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # Configuración WSGI
├── manage.py               # Script de gestión de Django
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Este archivo
```

## 🎯 Uso Básico

### Como Estudiante

1. **Registrarse:** Crea una cuenta desde `/register/`
2. **Explorar cursos:** Ve la lista de cursos disponibles en la página principal
3. **Inscribirse:** Haz clic en "Inscribirme a este curso"
4. **Estudiar:** Accede a las lecciones del curso
5. **Realizar quizzes:** Completa las evaluaciones disponibles
6. **Ver resultados:** Revisa tus calificaciones y respuestas

### Como Instructor

1. **Convertirse en instructor:** Usa el botón "Convertirse en instructor" (si eres estudiante)
2. **Crear curso:** Haz clic en "➕ Crear curso"
3. **Agregar lecciones:** Añade contenido de video, documentos o texto
4. **Crear quizzes:** Crea evaluaciones con preguntas y opciones
5. **Ver calificaciones:** Revisa el progreso de tus estudiantes
6. **Generar certificados:** Descarga certificados para estudiantes aprobados

## 📝 Criterios de Aprobación

Para que un estudiante apruebe un curso:
- ✅ Debe completar **todos** los quizzes del curso
- ✅ Debe obtener un promedio general **≥ 70%**
- ✅ Solo se consideran los mejores intentos de cada quiz

## 🔧 Configuración Adicional

### Cambiar la zona horaria

Edita `elearning/settings.py`:
```python
TIME_ZONE = 'America/Chihuahua'  # Cambia según tu zona
```

### Configurar archivos estáticos para producción
```bash
python manage.py collectstatic
```

### Cambiar el SECRET_KEY

⚠️ **Importante:** Antes de desplegar a producción, cambia el `SECRET_KEY` en `settings.py`

## 🐛 Solución de Problemas

### Error: "No module named 'PIL'"
```bash
pip install Pillow
```

### Error: "No module named 'reportlab'"
```bash
pip install reportlab
```

### Las imágenes no se muestran
- Verifica que `DEBUG = True` en desarrollo
- Asegúrate de que las URLs de media estén configuradas en `urls.py`

### Error de migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📄 Licencia

Este proyecto es un prototipo educativo desarrollado para demostración.

## 👨‍💻 Autor

Proyecto desarrollado como sistema de gestión de aprendizaje en línea.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

Para preguntas o sugerencias sobre el proyecto, por favor abre un issue en el repositorio.

---

⭐ Si te gustó este proyecto, dale una estrella en GitHub!
