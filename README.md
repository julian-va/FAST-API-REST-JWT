# FAST-API-REST-JWT

Api de Autenticación con jwt y el framework Fast-api

# creacion entorno virtual

Creal entorno virtaul con la libre de prefencia, en este caso se realiza con
virtualenv

1.  clonar repositorio e ingresar a la carpeta
2.  pip3 install virtualenv
3.  dentro de la carpeta crear entorno virtual: virtualenv venv
4.  activar entorno virtual(linux): source venv/bin/activate
5.  descargar dependencias: pip3 o pip install -r requirements.txt

# correr proyecto

1. crear archivo .env como el ejemplo env.example con la constante SECRET=string o lo que quieras
2. abrir consola en la raiz de la carpeta y escribir: uvicor main:app --reload
3. documentacion api, url asignado/docs# ej: http://127.0.0.1:8000/docs#
