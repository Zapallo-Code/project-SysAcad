import datetime
from io import BytesIO
from app.models import Alumno
from app.repositories import AlumnoRepository
from app.services.documentos_office_service import PDFDocument, ODTDocument, DOCXDocument, Document, obtener_tipo_documento

class AlumnoService:

    @staticmethod
    def crear(alumno):
        AlumnoRepository.crear(alumno)

    @staticmethod
    def buscar_por_id(id: int) -> Alumno:        
        return AlumnoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Alumno]:
        return AlumnoRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id: int, alumno: Alumno) -> Alumno:
        alumno_existente = AlumnoRepository.buscar_por_id(id)
        if not alumno_existente:
            return None
        alumno_existente.nombre = alumno.nombre
        alumno_existente.apellido = alumno.apellido
        alumno_existente.nrodocumento = alumno.nrodocumento
        alumno_existente.tipo_documento = alumno.tipo_documento
        alumno_existente.fecha_nacimiento = alumno.fecha_nacimiento
        alumno_existente.sexo = alumno.sexo
        alumno_existente.nro_legajo = alumno.nro_legajo
        alumno_existente.fecha_ingreso = alumno.fecha_ingreso
        alumno_existente.especialidad = alumno.especialidad
        return AlumnoRepository.actualizar(alumno_existente)
        
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return AlumnoRepository.borrar_por_id(id)
    
    @staticmethod
    def generar_certificado_alumno_regular(id: int,tipo: str)-> BytesIO:
        alumno = AlumnoRepository.buscar_por_id(id)
        if not alumno:
            return None
        
        context = AlumnoService.__obteneralumno(alumno)
        documento = obtener_tipo_documento(tipo)
        if not documento:
            return None
        
        return documento.generar(
            carpeta='certificado',
            plantilla='certificado_pdf',
            context=context
        )
    
    @staticmethod
    def __obtener_fechaactual():
        fecha_actual = datetime.datetime.now()
        fecha_str = fecha_actual.strftime('%d de %B de %Y')
        return fecha_str

    @staticmethod
    def __obteneralumno(alumno: Alumno) -> dict:
        especialidad = alumno.especialidad
        facultad = especialidad.facultad
        universidad = facultad.universidad
        return{
            "alumno": alumno,
            "especialidad": especialidad,
            "facultad": facultad,
            "universidad": universidad,
            "fecha":AlumnoService.__obtener_fechaactual()
        }
