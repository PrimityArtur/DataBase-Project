from django.db import connection

def obtenerSchematic(tipo_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM SCHEMATIC WHERE TIPO_ID = %s", [tipo_id])
        schematic = cursor.fetchone()
    return schematic

def registrarSchematic(tipo_id, dimensiones):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO SCHEMATIC (TIPO_ID, DIMENSIONES)
                VALUES (%s, %s)
            """, [tipo_id, dimensiones])
            connection.commit()
    except Exception as e:
        print("Ocurrio un error al inertar el schematic", e)

def modificarSchematic(tipo_id, dimensiones):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE SCHEMATIC
            SET DIMENSIONES = %s
            WHERE TIPO_ID = %s
        """, [dimensiones, tipo_id])
        connection.commit()

def eliminarSchematic(tipo_id):
    print("Eliminando schematic")
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM SCHEMATIC WHERE TIPO_ID = %s", [tipo_id])
        connection.commit()