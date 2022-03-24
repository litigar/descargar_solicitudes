## Descargar pdfs de solicitudes de Radicaciones
> Aplicacion cliente que consume servicio de la api de litigar, para descargar los pdfs asociados a las solicitudes de radicaciones.
# Versionamiento
- Fecha primera versión: 24/03/2022
* Python >3.6.2 +
# Instalación
## 1. Instale python desde la siguiente ruta:
> https://www.python.org/downloads/
## 2. Descargue y Descomprima el proyecto
- Descargue en la carpeta el proyecto desde github, ya sea desde un archivo zip (descomprímirlo) o por github
> https://github.com/litigar/descargar_solicitudes.git
- Descomprima el archivo zip 
## 3. Instale el entorno virtual:
- Abra una terminal e ingrese a la carpeta donde descomprimió el archivo zip
> python -m pip install virtualenv
- Cree un entorno virtual
> python -m venv venv_descarga
- Activar El Entorno Virtual
> venv_descarga\Scripts\activate
## 4. Instale los componentes
Con el entorno virtual activo ejecute el siguiente comando
> pip install -r requirements.txt
# Configuración inicial
- Abra el archivo .env
- Ingrese el usuario y password de litigar inmediatamente al frente de caracter igual (=)
> - user_name=
> - password=
# Funcionalidad
## 1. Selección de solicitudes para descargar pdfs
- En el archivo solicitudes.txt se deben ingresar los numero de solicitudes.
- En cada fila del archivo se debe ingresar un numero de solicitud.
- El numero de solicitud no se deben separar con caracteres adicionales como la coma, punto y coma o pipes.
## 2. Descargue de pdfs de las solicitudes
- Los archivos pdfs quedan ubicados en la carpeta pdfs.
- El nombre del archivo descargado tiene la siguiente estructura:
> Solicitud_id_Historia_id_estadoSolicitud.pdf
## 3. Logs:
- Los logs de la ejecución de la aplicación quedan ubicados en la carpeta logs.
# Ejecución de la aplicación
Estando en la terminal en la ruta principal del proyecto, ejecute los siguientes pasos:
## 1. realizar la descarga de pdfs de las solicitudes
> python descargar_solicitudes.py

