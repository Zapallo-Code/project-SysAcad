# SysAcad - Sistema Académico Universitario

Sistema de gestión académica universitaria desarrollado con Django REST Framework y PostgreSQL. Este proyecto proporciona una API REST completa para administrar la estructura organizacional de una universidad, incluyendo facultades, carreras, materias, estudiantes y personal académico.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#️-tecnologías)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Modelos de Datos](#-modelos-de-datos)
- [Instalación y Ejecución](#-instalación-y-ejecución)
  - [Requisitos Previos](#requisitos-previos)
  - [Ejecución Local](#ejecución-local)
  - [Ejecución con Docker](#ejecución-con-docker)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Funcionalidades Especiales](#-funcionalidades-especiales)
- [Configuración](#️-configuración)

---

## ✨ Características

- **API RESTful completa** para gestión académica universitaria
- **Arquitectura en capas** (Models, Repositories, Services, Views)
- **Generación de certificados** en múltiples formatos (PDF, ODT, DOCX)
- **Base de datos PostgreSQL** con relaciones complejas
- **Testing completo** con fixtures y casos de prueba
- **Dockerización** para fácil despliegue
- **Validaciones personalizadas** con Django validators
- **Paginación automática** de resultados
- **Soporte de internacionalización** (Español - Argentina)

---

## 🏗 Arquitectura

El proyecto sigue una **arquitectura en capas** que separa responsabilidades:

```
┌─────────────────┐
│     Views       │  ← Capa de Presentación (API REST)
│   (ViewSets)    │
└────────┬────────┘
         │
┌────────▼────────┐
│   Serializers   │  ← Validación y Serialización
└────────┬────────┘
         │
┌────────▼────────┐
│    Services     │  ← Lógica de Negocio
└────────┬────────┘
         │
┌────────▼────────┐
│  Repositories   │  ← Acceso a Datos
└────────┬────────┘
         │
┌────────▼────────┐
│     Models      │  ← Capa de Datos (ORM)
└─────────────────┘
```

### Capas del Sistema

1. **Models (`app/models/`)**: Define la estructura de datos con Django ORM
2. **Repositories (`app/repositories/`)**: Maneja las operaciones CRUD sobre los modelos
3. **Services (`app/services/`)**: Implementa la lógica de negocio
4. **Serializers (`app/serializers/`)**: Valida y transforma datos para la API
5. **Views (`app/views/`)**: Expone endpoints REST usando ViewSets de DRF

---

## 🛠️ Tecnologías

### Backend Framework
- **Django 5.2.7** - Framework web de alto nivel
- **Django REST Framework 3.15.2** - Construcción de APIs REST

### Base de Datos
- **PostgreSQL** - Base de datos relacional
- **psycopg2 2.9.10** - Adaptador PostgreSQL para Python

### Librerías Adicionales
- **python-dotenv** - Gestión de variables de entorno
- **hashids** - Generación de IDs ofuscados
- **weasyprint** - Generación de PDFs
- **python-odt-template** - Generación de documentos ODT
- **docxtpl** - Generación de documentos DOCX

### Infraestructura
- **Docker & Docker Compose** - Contenedorización
- **Python 3.12** - Lenguaje de programación

---

## 📁 Estructura del Proyecto

```
project-SysAcad/
├── app/                          # Aplicación principal
│   ├── models/                   # Modelos de datos (18 entidades)
│   │   ├── university.py         # Universidad
│   │   ├── faculty.py            # Facultad
│   │   ├── specialty.py          # Especialidad/Carrera
│   │   ├── student.py            # Estudiante
│   │   ├── subject.py            # Materia
│   │   ├── plan.py               # Plan de estudio
│   │   ├── authority.py          # Autoridades
│   │   ├── position.py           # Cargos
│   │   └── ...                   # Otros modelos
│   ├── repositories/             # Capa de acceso a datos
│   ├── services/                 # Lógica de negocio
│   │   ├── certificate.py        # Generación de certificados
│   │   └── ...                   # Servicios por entidad
│   ├── serializers/              # Serialización de datos
│   ├── views/                    # ViewSets de la API
│   ├── validators/               # Validadores personalizados
│   ├── static/                   # Archivos estáticos
│   ├── template/                 # Templates para documentos
│   │   └── certificado/          # Templates de certificados
│   ├── config/                   # Configuración de la app
│   ├── urls.py                   # Rutas de la API
│   └── admin.py                  # Configuración admin
├── main/                         # Configuración Django
│   ├── settings.py               # Configuración principal
│   ├── urls.py                   # URLs del proyecto
│   └── wsgi.py                   # WSGI application
├── tests/                        # Suite de pruebas
│   ├── fixtures.py               # Datos de prueba
│   └── test_*.py                 # Tests por entidad
├── docs/                         # Documentación
│   └── class_diagram.puml        # Diagrama de clases
├── docker-compose.yml            # Orquestación de contenedores
├── Dockerfile                    # Imagen Docker
├── requirements.txt              # Dependencias Python
├── manage.py                     # CLI de Django
└── README.md                     # Este archivo
```

---

## 📊 Modelos de Datos

El sistema cuenta con **18 modelos principales** que representan la estructura universitaria:

### Entidades Principales

#### 🏛️ Estructura Organizacional
- **University**: Universidad (nombre, acrónimo)
- **Faculty**: Facultad (datos de contacto, ubicación)
- **Department**: Departamento académico
- **Area**: Área de conocimiento

#### 🎓 Estructura Académica
- **Specialty**: Especialidad/Carrera (asociada a faculty)
- **SpecialtyType**: Tipo de speciality
- **Plan**: Plan de estudios (vigencia)
- **Subject**: Materia (código único, nombre)
- **Orientation**: Orientación académica
- **Degree**: Título/Grado otorgado
- **Group**: Grupo de materias

#### 👨‍🎓 Estudiantes
- **Student**: Estudiante
  - Datos personales (nombre, apellido, DNI)
  - Fecha de nacimiento y género
  - Número de legajo único
  - Fecha de inscripción
  - Relación con especialidad y tipo de documento
  - Propiedades calculadas: `full_name`, `age`

#### 👔 Personal y Autoridades
- **Authority**: Autoridades académicas
- **Position**: Cargos/Posiciones
- **PositionCategory**: Categoría de position
- **DedicationType**: Tipo de dedicación

#### 📄 Tipos de Documentos
- **DocumentType**: Tipos de documentos de identidad

### Relaciones Clave

```
University (1) ──→ (N) Faculty
Faculty (1) ──→ (N) Specialty
Specialty (1) ──→ (N) Student
Student (N) ──→ (1) DocumentType
```

---

## 🚀 Instalación y Ejecución

### Requisitos Previos

- **Python 3.12+** (para ejecución local)
- **PostgreSQL 13+** (para ejecución local)
- **Docker y Docker Compose** (para ejecución con Docker)
- **Git**

### Ejecución Local

#### 1. Clonar el repositorio

```bash
git clone https://github.com/Zapallo-Code/project-SysAcad.git
cd project-SysAcad
```

#### 2. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
# o
.venv\Scripts\activate  # En Windows
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Django
SECRET_KEY=tu-secret-key-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
POSTGRES_DB=sysacad
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

#### 5. Configurar PostgreSQL

Crear la base de datos:

```bash
# Conectarse a PostgreSQL
psql -U postgres

# Crear la base de datos
CREATE DATABASE sysacad;
\q
```

#### 6. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

#### 8. Ejecutar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

---

### Ejecución con Docker

Docker simplifica el despliegue al encapsular todas las dependencias.

#### 1. Clonar el repositorio

```bash
git clone https://github.com/Zapallo-Code/project-SysAcad.git
cd project-SysAcad
```

#### 2. Configurar variables de entorno

Crear archivo `.env`:

```env
# Django
SECRET_KEY=tu-secret-key-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,backend

# PostgreSQL
POSTGRES_DB=sysacad
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu-password-seguro
DATABASE_HOST=db
DATABASE_PORT=5432
```

**⚠️ Importante**: Para Docker, `DATABASE_HOST` debe ser `db` (nombre del servicio).

#### 3. Construir y levantar contenedores

```bash
docker-compose up --build
```

O en modo detached (segundo plano):

```bash
docker-compose up -d --build
```

#### 4. Ejecutar migraciones en el contenedor

```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

#### 5. Crear superusuario (opcional)

```bash
docker-compose exec backend python manage.py createsuperuser
```

#### 6. Acceder a la aplicación

- **API**: `http://localhost:8000`
- **Admin**: `http://localhost:8000/admin`
- **PostgreSQL**: `localhost:5432`

#### Comandos útiles de Docker

```bash
# Ver logs
docker-compose logs -f backend

# Detener contenedores
docker-compose down

# Detener y eliminar volúmenes (⚠️ borra la BD)
docker-compose down -v

# Reconstruir sin cache
docker-compose build --no-cache

# Ejecutar comandos en el contenedor
docker-compose exec backend python manage.py <comando>

# Ejecutar tests
docker-compose exec backend python manage.py test
```

---

## 🌐 API Endpoints

La API REST está disponible en `/api/v1/` con los siguientes recursos:

### Endpoints Disponibles

| Recurso | Endpoint | Métodos |
|---------|----------|---------|
| Universidades | `/api/v1/university/` | GET, POST, PUT, DELETE |
| Facultades | `/api/v1/faculty/` | GET, POST, PUT, DELETE |
| Especialidades | `/api/v1/speciality/` | GET, POST, PUT, DELETE |
| Estudiantes | `/api/v1/student/` | GET, POST, PUT, DELETE |
| Materias | `/api/v1/subject/` | GET, POST, PUT, DELETE |
| Planes | `/api/v1/plan/` | GET, POST, PUT, DELETE |
| Autoridades | `/api/v1/authority/` | GET, POST, PUT, DELETE |
| Cargos | `/api/v1/position/` | GET, POST, PUT, DELETE |
| Categorías Cargo | `/api/v1/position_category/` | GET, POST, PUT, DELETE |
| Departamentos | `/api/v1/departament/` | GET, POST, PUT, DELETE |
| Áreas | `/api/v1/area/` | GET, POST, PUT, DELETE |
| Grupos | `/api/v1/group/` | GET, POST, PUT, DELETE |
| Orientaciones | `/api/v1/orientation/` | GET, POST, PUT, DELETE |
| Títulos | `/api/v1/degree/` | GET, POST, PUT, DELETE |
| Tipos Dedicación | `/api/v1/dedication_type/` | GET, POST, PUT, DELETE |
| Tipos Documento | `/api/v1/document_type/` | GET, POST, PUT, DELETE |
| Tipos Especialidad | `/api/v1/speciality_type/` | GET, POST, PUT, DELETE |

### Ejemplos de Uso

#### Listar todos los estudiantes

```bash
curl -X GET http://localhost:8000/api/v1/student/
```

#### Obtener un estudiante específico

```bash
curl -X GET http://localhost:8000/api/v1/student/1/
```

#### Crear un nuevo estudiante

```bash
curl -X POST http://localhost:8000/api/v1/student/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan",
    "last_name": "Pérez",
    "document_number": "12345678",
    "document_type": 1,
    "birth_date": "2000-01-01",
    "gender": "M",
    "student_number": 123456,
    "enrollment_date": "2020-03-01",
    "specialty": 1
  }'
```

#### Actualizar un estudiante

```bash
curl -X PUT http://localhost:8000/api/v1/student/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan Modificado",
    ...
  }'
```

#### Eliminar un estudiante

```bash
curl -X DELETE http://localhost:8000/api/v1/student/1/
```

### Paginación

La API implementa paginación automática (100 elementos por página):

```bash
curl -X GET "http://localhost:8000/api/v1/student/?page=2"
```

---

## 🧪 Testing

El proyecto incluye una suite completa de tests unitarios usando Django TestCase.

### Ejecutar todos los tests

```bash
# Local
python manage.py test

# Docker
docker-compose exec backend python manage.py test
```

### Ejecutar tests específicos

```bash
# Test de un módulo específico
python manage.py test tests.test_student

# Test de una clase específica
python manage.py test tests.test_student.StudentTestCase

# Test de un método específico
python manage.py test tests.test_student.StudentTestCase.test_crear
```

### Estructura de Tests

Los tests están organizados en `tests/`:

- `fixtures.py`: Funciones auxiliares para crear datos de prueba
- `test_student.py`: Tests para el modelo Student
- `test_university.py`: Tests para el modelo University
- `test_faculty.py`: Tests para el modelo Faculty
- ... (un archivo por cada modelo)

### Ejemplo de Test

```python
class StudentTestCase(TestCase):
    def test_crear(self):
        student = new_student()
        self.assertIsNotNone(student)
        self.assertEqual(student.last_name, "Pérez")
    
    def test_find_by_id(self):
        student = new_student()
        r = StudentService.find_by_id(student.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.first_name, "Juan")
```

### Cobertura de Tests

Los tests cubren:
- ✅ Creación de entidades
- ✅ Lectura por ID
- ✅ Listado completo
- ✅ Actualización de datos
- ✅ Eliminación lógica
- ✅ Validaciones de campos
- ✅ Relaciones entre entidades

---

## 🎯 Funcionalidades Especiales

### Generación de Certificados

El sistema puede generar certificados académicos en múltiples formatos:

#### Formatos Soportados
- **PDF** (usando WeasyPrint)
- **ODT** (LibreOffice)
- **DOCX** (Microsoft Word)

#### Implementación

```python
# En app/services/student.py
def generar_certificado_student_regular(id: int, tipo: str) -> BytesIO:
    # tipo puede ser: 'pdf', 'odt', 'docx'
    student = StudentRepository.find_by_id(id)
    context = self.__get_student_data(student)
    documento = get_document_type(tipo)
    return documento.generar(
        folder='certificado',
        template='certificado_pdf',
        context=context
    )
```

#### Templates

Los templates están en `app/template/certificado/`:
- `certificado_pdf.html` (para PDF)
- `certificado_pdf.odt` (para ODT)
- `certificado_pdf.docx` (para DOCX)

### Propiedades Calculadas

Varios modelos incluyen propiedades calculadas dinámicamente:

```python
# Student
@property
def full_name(self):
    return f"{self.first_name} {self.last_name}"

@property
def age(self):
    today = date.today()
    return today.year - self.birth_date.year - (
        (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
    )

# Plan
@property
def is_active(self):
    today = date.today()
    return self.start_date <= today <= self.end_date
```

---

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Django | - |
| `DEBUG` | Modo debug | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |
| `POSTGRES_DB` | Nombre de la BD | `sysacad` |
| `POSTGRES_USER` | Usuario PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Contraseña PostgreSQL | `postgres` |
| `DATABASE_HOST` | Host de la BD | `localhost` / `db` |
| `DATABASE_PORT` | Puerto de la BD | `5432` |

### Configuración REST Framework

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
```

### Internacionalización

```python
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True
```

---

## 📝 Notas Adicionales

### Admin de Django

Accede al panel de administración en `/admin/` después de crear un superusuario.

### Migraciones

Después de modificar modelos:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Shell Interactivo

Para experimentar con los modelos:

```bash
python manage.py shell

# Ejemplo
>>> from app.models import Student
>>> Student.objects.all()
```

---

## 👥 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico universitario.

---

## 📧 Contacto

Proyecto SysAcad - Sistema Académico Universitario

Repository: [https://github.com/Zapallo-Code/project-SysAcad](https://github.com/Zapallo-Code/project-SysAcad)

---

## 🙏 Equipo

- Valentin Rubio

- Luciano Castro

- Santiago Calzonari

- Santiago Oses

- Pablo Geyer
