# teknos

Pasos para ejecutar:
- Instalar python 3.10
- Ejectuar comando en el cmd: "pip install virtualenv"
- Descargar el repositorio
- Navegar hasta la carpeta del repositorio y ejecutar en el cmd: "python -m venv teknos"
- Ejecutar en el cmd: "teknos\Scripts\activate" 
  (Deberia aparecer al costado del path (teknos))
- Ejecutar en el cmd: "pip install -r requirements.txt"
- Ejecutar en el cmd: "uvicorn mailApi.main:app --reload"
  Dentro de lo ejecutado la segunda linea va a tener esta forma:
  [32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
  Este va a ser nuestro url para acceder desde el navegador: http://127.0.0.1:8000
 - Copiar el url y agregarle /docs al final: http://127.0.0.1:8000/docs
 - Esto nos lleva a una interfaz donde estan los distintos tipos de request con sus parametros requeridos y ejemplos de sus bodys
 - Si queremos probar un request clickeamos en el mismo, vamos a donde dice tryout y modificamos los params y el body de ejemplo que provee y le damos a execute

Aclaraciones:
- Tuve que cambiar el campo "from" de los json a "froms" porque from es una keyword en python y traia problemas usarlo como variable.
- Queda a cargo del usuario mantener la coherencia con los attachments, la api permite crear un mail con hasAttachments = true pero despues debe ser agregado.
- El reset data carga todos los mails que habia en los distintos modelos en la base de datos (Cambie los Ids de algunos mails porque se repetia en los distintos archivos pero el contenido era distinto).
