from django.db import connection

def obtenerAdministrador(administrador_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM administrador WHERE administrador_id = %s", [administrador_id])
        administrador = cursor.fetchone()
    return administrador

def registrarAdministrador(usuario_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO administrador (usuario_id) VALUES (%s)", [usuario_id])
    except Exception as e:
        print(f"Ocurrió un error al agregar el administrador: {e}")