
PROYECTO EN ORACLE SQL Y DJANGO 

PASOS PARA LA CORRER EL PROGRAMA:

1) Instalar la última versión de Python 3.12  
 - https://www.python.org/downloads/

2) Instalar Oracle SQL Developer y Oracle Database 21c Express Edition 
- https://www.oracle.com/database/sqldeveloper/technologies/download/
- https://www.oracle.com/database/technologies/xe-downloads.html

3) en el CMD ejecutar:
- python -m pip install cx-Oracle --upgrade
- python -m pip install DJango
- python -m pip install oracledb

4) en Oracle SQL:
- Realizar una nueva conexión donde ejecutaremos nuestras sentencias:
    - Video tutorial https://www.youtube.com/watch?v=yLVMdrDrsec

- Ejecutar las sentencias en la consola de la conexión en oracle SQL ubicadas en esta carpeta ./sql/ 
 - Seguir el siguiente orden de ejecución
    - schemas.sql
    - fillSchemas.sql

5) En la carpeta ./WebDBProject/mainDB/settings.py: 
- En la línea 81 el diccionario DATABASES cambiar los datos con sus datos que ingreso en la nueva conexión de oracleDB

6) Correr las migraciones. 
- Dentro de la carpeta ./WebDBProject Abrir una terminal ejecutar:
    - python manage.py migrate

7) Correr el servidor y entrar a la pagina web
- Dentro de la carpeta ./WebDBProject Abrir una terminal ejecutar:
    - python manage.py runserver
- Ahora acceda al link que le aparece en la terminal


