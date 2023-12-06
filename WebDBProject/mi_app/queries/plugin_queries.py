from django.db import connection

def obtenerPlugin(tipo_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PLUGIN WHERE TIPO_ID = %s", [tipo_id])
        plugin = cursor.fetchone()
    return plugin

def registrarPlugin(tipo_id, version):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO PLUGIN (TIPO_ID, VERSION)
                VALUES (%s, %s)
            """, [tipo_id, version])
            connection.commit()
    except Exception as e:
        print("Ocurrio un error al inertar el plugin", e)

def modificarPlugin(tipo_id, version):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE PLUGIN
            SET VERSION = %s
            WHERE TIPO_ID = %s
        """, [version, tipo_id])
        connection.commit()

def eliminarPlugin(tipo_id):
    print("Eliminando plugin")
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM PLUGIN WHERE TIPO_ID = %s", [tipo_id])
        connection.commit()