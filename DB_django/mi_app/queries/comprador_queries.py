from django.db import connection

def obtenerComprador(comprador_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM comprador WHERE comprador_id = %s", [comprador_id])
        comprador = cursor.fetchone()
    return comprador

def registrarComprador(usuario_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO comprador (usuario_id) VALUES (%s)", [usuario_id])
    except Exception as e:
        print(f"Ocurrió un error al agregar el comprador: {e}")