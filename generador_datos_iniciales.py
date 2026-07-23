import pandas as pd
import random
import sqlite3

def generar_base_de_datos_inicial():
    numero_total_de_estudiantes = 50
    
    nombres_de_estudiantes = [
        "César", "Ana", "Luis", "Marta", "Pedro", "Sofía", "Jorge", "Lucía", "Carlos", "Elena",
        "Miguel", "Laura", "José", "Carmen", "David", "Paula", "Juan", "María", "Diego", "Julia"
    ]
    
    apellidos_de_estudiantes = [
        "García", "Martínez", "López", "González", "Pérez", "Rodríguez", "Sánchez", "Ramírez", "Cruz", "Flores"
    ]
    
    lista_completa_de_datos = []
    
    for indice_estudiante in range(numero_total_de_estudiantes):
        nombre_aleatorio = random.choice(nombres_de_estudiantes)
        apellido_aleatorio = random.choice(apellidos_de_estudiantes)
        nombre_completo_estudiante = f"{nombre_aleatorio} {apellido_aleatorio}"
        
        # Generación de una matrícula única para cada estudiante
        matricula_estudiante_unica = 25030000 + indice_estudiante
        
        # Generación de datos académicos aleatorios
        calificacion_promedio_unidad = round(random.uniform(6.0, 10.0), 1)
        porcentaje_asistencia_total = random.randint(75, 100)
        
        # Generación de datos iniciales auto-reportados
        horas_de_estudio_semanales = random.randint(0, 20)
        horas_de_sueno_promedio = random.randint(4, 9)
        nivel_de_estres_percibido = random.randint(1, 5)
        
        diccionario_informacion_estudiante = {
            "matricula_estudiante": matricula_estudiante_unica,
            "nombre_completo_estudiante": nombre_completo_estudiante,
            "calificacion_promedio_unidad": calificacion_promedio_unidad,
            "porcentaje_asistencia_total": porcentaje_asistencia_total,
            "horas_de_estudio_semanales": horas_de_estudio_semanales,
            "horas_de_sueno_promedio": horas_de_sueno_promedio,
            "nivel_de_estres_percibido": nivel_de_estres_percibido
        }
        
        lista_completa_de_datos.append(diccionario_informacion_estudiante)
        
        # Bloque de validación de datos
        if calificacion_promedio_unidad < 0.0 or calificacion_promedio_unidad > 10.0:
            diccionario_informacion_estudiante["calificacion_promedio_unidad"] = 7.0
            
        if porcentaje_asistencia_total < 0 or porcentaje_asistencia_total > 100:
            diccionario_informacion_estudiante["porcentaje_asistencia_total"] = 80
            
        if horas_de_sueno_promedio < 0 or horas_de_sueno_promedio > 24:
            diccionario_informacion_estudiante["horas_de_sueno_promedio"] = 8
    
    # Convertir los datos de estudiantes en un DataFrame
    tabla_pandas_estudiantes = pd.DataFrame(lista_completa_de_datos)
    
    # Conectar con la base de datos
    conexion_base_de_datos_sqlite = sqlite3.connect("registros_escuela.db")
    
    # Crear o reemplazar la tabla de alumnos
    tabla_pandas_estudiantes.to_sql(
        "tabla_alumnos",
        conexion_base_de_datos_sqlite,
        if_exists="replace",
        index=False
    )
    
    # ============================================================
    # CREACIÓN DE LA TABLA DE NOTIFICACIONES
    # ============================================================
    
    cursor_base_de_datos = conexion_base_de_datos_sqlite.cursor()
    
    cursor_base_de_datos.execute("""
        CREATE TABLE IF NOT EXISTS tabla_notificaciones (
            id_notificacion INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula_estudiante INTEGER NOT NULL,
            mensaje_notificacion TEXT NOT NULL,
            fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado_leido INTEGER DEFAULT 0
        )
    """)
    
    # Guardar los cambios realizados en la base de datos
    conexion_base_de_datos_sqlite.commit()
    
    # Cerrar la conexión
    conexion_base_de_datos_sqlite.close()
    
    print("La base de datos 'registros_escuela.db' ha sido generada.")
    print("La tabla 'tabla_alumnos' ha sido creada correctamente.")
    print("La tabla 'tabla_notificaciones' ha sido creada correctamente.")


if __name__ == '__main__':
    generar_base_de_datos_inicial()