# E-Commerce Backend - BlackButton

Django rest-framework

Aprovechando las ventajas de framework, se generan una API RESTful rápida y
sencilla para que la página web pueda obtener de forma rápida la información de
los productos, así como usarla para el proceso CRUD y administrar la página.

## Stack Tecnológico

* Lenguaje: Python3.
* Framework: Django.
* Base de datos: MySQL.
* Librerías clave:
    * django-cors-header: Para permitir coxión con Vue 3
    * djangorestframework: Para construir la API web en Django
    * mysqlclient: Para conexión y gestión de base de datos.
    * django-environ: Para gestionar variables de entorno.
    * pillow: Para permitir el procesamiento de imagenes de forma sencilla y
      eficiente.

## Instalación y configuración

### Crear entorno virtual

```sh
python -m venv [nombre_del_entorno]
```

### Activar entorno virtual

```sh
source [nombre_del_entorno]/Scripts/activate
```

### Instalar las librerías

```sh
pip install -r requirements.txt
```

### Correr el proyecto

```sh
py server/manage.py runserver
```