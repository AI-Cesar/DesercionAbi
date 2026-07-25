import pandas as pd
import random
import mysql.connector

def generar_base_de_datos_inicial():
    # Conexión inicial a MySQL en XAMPP (sin especificar BD)
    conexion_servidor = mysql.connector.connect(
        host="localhost",
        user="root",
        password="" # Por defecto en XAMPP viene vacía
    )
    cursor_servidor = conexion_servidor.cursor()
    
    # Crear la base de datos si no existe
    cursor_servidor.execute("CREATE DATABASE IF NOT EXISTS registros_escuela_upg")
    cursor_servidor.close()
    conexion_servidor.close()

    # Ahora nos conectamos a la BD específica
    conexion_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="registros_escuela_upg"
    )

    numero_total_de_estudiantes = 1000
    
    nombres_de_estudiantes = [
        "César", "Ana", "Luis", "Marta", "Pedro", "Sofía", "Jorge", "Lucía", "Carlos", "Elena",
        "Miguel", "Laura", "José", "Carmen", "David", "Paula", "Juan", "María", "Diego", "Julia",
        "Eliceo", "Cecilia", "Gustavo", "Ricardo", "Fernando", "Valeria", "Andrea", "Gabriel", "Ximena", "Daniel"
    ]
    
    apellidos_de_estudiantes = [
        "García", "Martínez", "López", "González", "Pérez", "Rodríguez", "Sánchez", "Ramírez", "Cruz", "Flores",
        "Gómez", "Morales", "Vázquez", "Reyes", "Jiménez", "Torres", "Díaz", "Gutiérrez", "Mendoza", "Ruiz"
    ]
    
    carreras_upg = [
        "Datos e Inteligencia Artificial (IDIA)",
        "Alimentos (IAL)",
        "Automotriz (IAU)",
        "Biotecnología (IBI)",
        "Energía y Desarrollo Sostenible (IEDS)",
        "Logística (ILO)",
        "Manufactura Avanzada (IMA)",
        "Calidad y Metrología (ICM)",
        "Mecatrónica (IME)"
    ]

    opciones_situacion = ["Normal"] * 70 + ["Regular"] * 20 + ["Especial"] * 10
    lista_completa_de_datos = []
    
    for indice_estudiante in range(numero_total_de_estudiantes):
        nombre_aleatorio = random.choice(nombres_de_estudiantes)
        apellido_paterno = random.choice(apellidos_de_estudiantes)
        apellido_materno = random.choice(apellidos_de_estudiantes)
        nombre_completo_estudiante = f"{nombre_aleatorio} {apellido_paterno} {apellido_materno}"
        
        matricula_estudiante_unica = 25030000 + indice_estudiante
        carrera_estudiante = random.choice(carreras_upg)
        situacion_academica = random.choice(opciones_situacion)
        
        if situacion_academica == "Normal":
            calificacion_promedio_unidad = round(random.uniform(7.8, 10.0), 1)
            porcentaje_asistencia_total = random.randint(85, 100)
            horas_de_estudio_semanales = random.randint(8, 20)
            horas_de_sueno_promedio = random.randint(6, 9)
            nivel_de_estres_percibido = random.randint(1, 3)
        elif situacion_academica == "Regular":
            calificacion_promedio_unidad = round(random.uniform(6.5, 8.2), 1)
            porcentaje_asistencia_total = random.randint(75, 90)
            horas_de_estudio_semanales = random.randint(4, 12)
            horas_de_sueno_promedio = random.randint(5, 7)
            nivel_de_estres_percibido = random.randint(2, 4)
        else:
            calificacion_promedio_unidad = round(random.uniform(5.0, 7.2), 1)
            porcentaje_asistencia_total = random.randint(60, 82)
            horas_de_estudio_semanales = random.randint(1, 8)
            horas_de_sueno_promedio = random.randint(4, 6)
            nivel_de_estres_percibido = random.randint(3, 5)
        
        diccionario_informacion_estudiante = {
            "matricula_estudiante": matricula_estudiante_unica,
            "nombre_completo_estudiante": nombre_completo_estudiante,
            "carrera": carrera_estudiante,
            "situacion_academica": situacion_academica,
            "calificacion_promedio_unidad": calificacion_promedio_unidad,
            "porcentaje_asistencia_total": porcentaje_asistencia_total,
            "horas_de_estudio_semanales": horas_de_estudio_semanales,
            "horas_de_sueno_promedio": horas_de_sueno_promedio,
            "nivel_de_estres_percibido": nivel_de_estres_percibido
        }
        lista_completa_de_datos.append(diccionario_informacion_estudiante)
    
    # Crear la tabla usando una conexión SQLAlchemy para compatibilidad limpia con Pandas to_sql
    from sqlalchemy import create_engine
    engine = create_engine("mysql+mysqlconnector://root:@localhost/registros_escuela_upg")
    
    tabla_pandas_estudiantes = pd.DataFrame(lista_completa_de_datos)
    tabla_pandas_estudiantes.to_sql("tabla_alumnos", engine, if_exists="replace", index=False)
    
    # Crear la tabla de notificaciones directamente
    cursor = conexion_db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabla_notificaciones (
            id_notificacion INT AUTO_INCREMENT PRIMARY KEY,
            matricula_estudiante INT NOT NULL,
            mensaje_notificacion TEXT NOT NULL,
            fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado_leido INT DEFAULT 0
        )
    """)
    conexion_db.commit()
    cursor.close()
    conexion_db.close()
    
    print("--------------------------------------------------")
    print("¡Base de datos 'registros_escuela_upg' generada!")


if __name__ == '__main__':
    generar_base_de_datos_inicial()