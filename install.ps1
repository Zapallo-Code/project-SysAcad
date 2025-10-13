# Se Necesitan tener los permisos de seguridad configurados con Set-ExecutionPolicy RemoteSigned
# para ello abrir la consola de PowerShell como administrador y ejecutar:
# Set-ExecutionPolicy RemoteSigned

# Activar el entorno virtual
# Cambiar la ruta del entorno virtual si es necesario
& ".\venv\Scripts\Activate.ps1"

pip3 install -r requirements.txt

