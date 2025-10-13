# Proyecto: Flask Sysacad

## Equipo de desarrollo
- Agustin Campos  
- Loana Vargas  
- Delfina Carribero
- Leandro Canton
- Gabriel Flores  


## Descripción del proyecto

- **`app/`** → Contiene el código principal de la aplicación.  
  - **`config/`** → Configuración de la aplicación   
  - **`mapping/`** → convertir los models en JSON y viceversa.
  - **`models/`** → entidades/tablas de la base de datos   
  - **`repositories/`** → Interactua con la base de datos 
  - **`resources/`** →  Aquí se definen las rutas.  
  - **`services/`** → Lógica de la aplicacion, se aplican reglas y llaman a los repositorios
  -   
  - **`__init__.py`** → Inicialización de `app` 

- **`test/`** → Pruebas para ver si funciona correctamente.    
  
- **`requirements.txt`** → Lista de librerias.  
- **`.env`** → Variables de entorno.    
- **`boot.ps1`** → Scripts de inicio (no nos funciona, intentamos pero se nos desinstala visual).  
- **`install.ps1`** → Scripts para instalar librerias y preparar el entorno.  

## Pasos para iniciar la app:
1-crear entorno virtual (se entra mediante 'venv\Scripts\Activate.ps1')
2-instalar las librerias al entorno virtual (esta en requirements txt o ejecutando install.ps1)
3-crear las tablas en la base de datos mediante flask-migrate, PRIMERO: flask db init (se crea carpeta migrations),SEGUNDO: flask db migrate -m "crear tabla usuario"
TERCERO: flask db upgrade 
4- inicar la app usando el comando: python app.py (o por boot.ps1 pero quisimos hacerlo y nos desinstalaba visual)
5- insertar datos en las tablas mediante CREATE
6-probar mediante request en postman los CRUD

## Rutas para request:

CREATE: 'http://localhost:5000/api/v1/modelo'
READ (ID): 'http://localhost:5000/api/v1/modelo/ID'
READ (TODOS): 'http://localhost:5000/api/v1/modelo'
UPDATE: 'http://localhost:5000/api/v1/modelo/ID'
DELETE: 'http://localhost:5000/api/v1/modelo/ID'