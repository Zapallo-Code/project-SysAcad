from app.models import (
    Alumno, Area, Autoridad, Cargo, CategoriaCargo, Departamento,
    Especialidad, Facultad, Grado, Grupo, Materia, Orientacion,
    Plan, TipoDedicacion, TipoDocumento, TipoEspecialidad, Universidad
)
from datetime import date

from app.services import (
    AlumnoService, AreaService,AutoridadService, CargoService, CategoriaCargoService,
    DepartamentoService, EspecialidadService, FacultadService, GradoService, GrupoService,
    MateriaService, OrientacionService, PlanService, TipoDedicacionService, TipoDocumentoService,
    TipoEspecialidadService, UniversidadService
)

def nuevotipodocumento(dni=46291002, libreta_civica="nacional", libreta_enrolamiento="naci", pasaporte="nacnal"):
    tipo_documento = TipoDocumento()
    tipo_documento.dni = dni
    tipo_documento.libreta_civica = libreta_civica
    tipo_documento.libreta_enrolamiento = libreta_enrolamiento
    tipo_documento.pasaporte = pasaporte
    TipoDocumentoService.crear(tipo_documento)
    return tipo_documento

def nuevotipodedicacion(nombre="Dedicacion Completa", observacion="Observacion de prueba"):
    td = TipoDedicacion()
    td.nombre = nombre
    td.observacion = observacion
    TipoDedicacionService.crear(td)
    return td

def nuevacategoriacargo(nombre="Docente"):
    categoria = CategoriaCargo()
    categoria.nombre = nombre
    CategoriaCargoService.crear(categoria)
    return categoria

def nuevocargo(nombre="Profesor", puntos=10, categoria_cargo=None, tipo_dedicacion=None):
    cargo = Cargo()
    cargo.nombre = nombre
    cargo.puntos = puntos
    cargo.categoria_cargo = categoria_cargo or nuevacategoriacargo()
    cargo.tipo_dedicacion = tipo_dedicacion or nuevotipodedicacion()
    CargoService.crear(cargo)
    return cargo

def nuevafacultad(nombre="Facultad de Ciencias", abreviatura="FCC", directorio="/facultad/ciencias",
                  sigla="FC", codigopostal="12345", ciudad="Ciudad", domicilio="Calle 123",
                  telefono="123456789", contacto="Juan Perez", email="1234@gmail.com", universidad=None, autoridades=None):
    facultad = Facultad()
    facultad.nombre = nombre
    facultad.abreviatura = abreviatura
    facultad.directorio = directorio
    facultad.sigla = sigla
    facultad.codigopostal = codigopostal
    facultad.ciudad = ciudad
    facultad.domicilio = domicilio
    facultad.telefono = telefono
    facultad.contacto = contacto
    facultad.email = email
    facultad.universidad = universidad or nuevauniversidad()

    if autoridades is None:
        autoridades = []
    facultad.autoridades = autoridades

    FacultadService.crear(facultad)
    return facultad

def nuevodepartamento(nombre="Matematicas"):
    departamento = Departamento()
    departamento.nombre = nombre
    DepartamentoService.crear(departamento)
    return departamento

def nuevaarea(nombre="Matematica"):
    area = Area()
    area.nombre = nombre
    AreaService.crear(area)
    return area

def nuevotipoespecialidad(nombre="Cardiologia", nivel="Avanzado"):
    tipo = TipoEspecialidad()
    tipo.nombre = nombre
    tipo.nivel = nivel
    TipoEspecialidadService.crear(tipo)
    return tipo

def nuevaespecialidad(nombre="Matematicas", letra="A", observacion="Observacion de prueba", tipoespecialidad=None, facultad=None):
    esp = Especialidad()
    esp.nombre = nombre
    esp.letra = letra
    esp.observacion = observacion
    esp.tipoespecialidad = tipoespecialidad or nuevotipoespecialidad()
    esp.facultad = facultad or nuevafacultad()
    EspecialidadService.crear(esp)
    return esp

def nuevoplan(nombre="Plan A", fecha_inicio=date(2024, 6, 4), fecha_fin=date(2024, 6, 5), observacion="Observacion de prueba"):
    plan = Plan()
    plan.nombre = nombre
    plan.fecha_inicio = fecha_inicio
    plan.fecha_fin = fecha_fin
    plan.observacion = observacion
    PlanService.crear(plan)
    return plan

def nuevamateria(nombre="Matematica", codigo="MAT101", observacion="Observacion de prueba",autoridades=None):
    materia = Materia()
    materia.nombre = nombre
    materia.codigo = codigo
    materia.observacion = observacion

    if autoridades is None:
        autoridades = []  
    materia.autoridades = autoridades
    
    MateriaService.crear(materia)
    return materia

def nuevaorientacion(nombre="Orientacion 1", especialidad=None, plan=None, materia=None):
    orientacion = Orientacion()
    orientacion.nombre = nombre
    orientacion.especialidad = especialidad or nuevaespecialidad()
    orientacion.plan = plan or nuevoplan()
    orientacion.materia = materia or nuevamateria()
    OrientacionService.crear(orientacion)
    return orientacion

def nuevauniversidad(nombre="Universidad Nacional", sigla="UN"):
    universidad = Universidad()
    universidad.nombre = nombre
    universidad.sigla = sigla
    UniversidadService.crear(universidad)
    return universidad

def nuevogrado(nombre="Primero", descripcion="Descripcion del primer grado"):
    grado = Grado()
    grado.nombre = nombre
    grado.descripcion = descripcion
    GradoService.crear(grado)
    return grado

def nuevogrupo(nombre="Grupo A"):
    grupo = Grupo()
    grupo.nombre = nombre
    GrupoService.crear(grupo)
    return grupo

def nuevoalumno(nombre="Juan", apellido="Pérez", nrodocumento="46291002", tipo_documento=None,
                fecha_nacimiento=date(1990, 1, 1), sexo="M", nro_legajo=123456, fecha_ingreso=date(2020, 1, 1),especialidad=None):
    alumno = Alumno()
    alumno.nombre = nombre
    alumno.apellido = apellido
    alumno.nrodocumento = nrodocumento
    alumno.tipo_documento = tipo_documento or nuevotipodocumento()
    alumno.fecha_nacimiento = fecha_nacimiento
    alumno.sexo = sexo
    alumno.nro_legajo = nro_legajo
    alumno.fecha_ingreso = fecha_ingreso
    alumno.especialidad = especialidad or nuevaespecialidad()
    AlumnoService.crear(alumno)
    return alumno

def nuevaautoridad(nombre="Pelo", cargo=None, telefono="123456789", email="123@gmail.com", 
                   materias=None, facultades=None):
    autoridad = Autoridad()
    autoridad.nombre = nombre
    autoridad.cargo = cargo or nuevocargo()
    autoridad.telefono = telefono
    autoridad.email = email

    if materias is None:
        materias = []
    autoridad.materias = materias

    if facultades is None:
        facultades = []
    autoridad.facultades = facultades
    
    AutoridadService.crear(autoridad)
    return autoridad
