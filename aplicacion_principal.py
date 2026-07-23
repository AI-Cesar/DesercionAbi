from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
from logica_calculo_riesgo import calcular_nivel_de_riesgo_estudiantil

aplicacion_web_flask = Flask(__name__)
# Necesario para poder usar 'session' en Flask
aplicacion_web_flask.secret_key = 'clave_secreta_super_segura_para_el_prototipo'

def obtener_conexion_base_de_datos():
    conexion_base_de_datos_sqlite = sqlite3.connect("registros_escuela.db")
    conexion_base_de_datos_sqlite.row_factory = sqlite3.Row
    return conexion_base_de_datos_sqlite

@aplicacion_web_flask.route('/')
def pagina_de_inicio_redireccion():
    if 'matricula_estudiante_sesion' in session:
        return redirect(url_for('modulo_vista_estudiante'))
    return redirect(url_for('vista_inicio_sesion'))

@aplicacion_web_flask.route('/login', methods=['GET', 'POST'])
def vista_inicio_sesion():
    mensaje_error_autenticacion = None
    
    if request.method == 'POST':
        matricula_ingresada_usuario = request.form.get('matricula_estudiante', '').strip()
        
        conexion_base_de_datos_sqlite = obtener_conexion_base_de_datos()
        cursor_base_de_datos = conexion_base_de_datos_sqlite.cursor()
        cursor_base_de_datos.execute("SELECT * FROM tabla_alumnos WHERE matricula_estudiante = ?", (matricula_ingresada_usuario,))
        registro_estudiante_encontrado = cursor_base_de_datos.fetchone()
        conexion_base_de_datos_sqlite.close()
        
        if registro_estudiante_encontrado:
            # Guardamos el alumno en la sesión activa
            session['matricula_estudiante_sesion'] = registro_estudiante_encontrado['matricula_estudiante']
            session['nombre_completo_estudiante_sesion'] = registro_estudiante_encontrado['nombre_completo_estudiante']
            return redirect(url_for('modulo_vista_estudiante'))
        else:
            mensaje_error_autenticacion = "La matrícula ingresada no se encuentra registrada en la base de datos."

    return render_template('login.html', mensaje_error=mensaje_error_autenticacion)

# 1. Nueva ruta para recibir la alerta enviada por el docente
@aplicacion_web_flask.route('/enviar_notificacion', methods=['POST'])
def enviar_notificacion_a_estudiante():
    matricula_estudiante_destino = request.form.get('matricula_estudiante')
    mensaje_notificacion_contenido = request.form.get('mensaje_notificacion')

    if matricula_estudiante_destino and mensaje_notificacion_contenido:
        conexion_base_de_datos_sqlite = obtener_conexion_base_de_datos()
        cursor_base_de_datos = conexion_base_de_datos_sqlite.cursor()
        cursor_base_de_datos.execute("""
            INSERT INTO tabla_notificaciones (matricula_estudiante, mensaje_notificacion)
            VALUES (?, ?)
        """, (matricula_estudiante_destino, mensaje_notificacion_contenido))
        conexion_base_de_datos_sqlite.commit()
        conexion_base_de_datos_sqlite.close()
        return jsonify({"estatus": "éxito", "mensaje": "Notificación guardada."})
    
    return jsonify({"estatus": "error", "mensaje": "Faltan datos."}), 400

@aplicacion_web_flask.route('/logout')
def cerrar_sesion_estudiante():
    session.clear()
    return redirect(url_for('vista_inicio_sesion'))
# 2. Modificación en la ruta del estudiante para consultar notificaciones
@aplicacion_web_flask.route('/estudiante', methods=['GET', 'POST'])
def modulo_vista_estudiante():
    if 'matricula_estudiante_sesion' not in session:
        return redirect(url_for('vista_inicio_sesion'))
        
    matricula_estudiante_actual = session['matricula_estudiante_sesion']
    
    conexion_base_de_datos_sqlite = obtener_conexion_base_de_datos()
    cursor_base_de_datos = conexion_base_de_datos_sqlite.cursor()
    
    # Manejo del formulario de hábitos (POST)
    if request.method == 'POST':
        horas_de_estudio_semanales = int(request.form.get('horas_de_estudio_semanales', 10))
        horas_de_sueno_promedio = int(request.form.get('horas_de_sueno_promedio', 8))
        nivel_de_estres_percibido = int(request.form.get('nivel_de_estres_percibido', 3))
        
        cursor_base_de_datos.execute("""
            UPDATE tabla_alumnos 
            SET horas_de_estudio_semanales = ?, horas_de_sueno_promedio = ?, nivel_de_estres_percibido = ?
            WHERE matricula_estudiante = ?
        """, (horas_de_estudio_semanales, horas_de_sueno_promedio, nivel_de_estres_percibido, matricula_estudiante_actual))
        conexion_base_de_datos_sqlite.commit()

    # Obtenemos los datos del alumno
    cursor_base_de_datos.execute("SELECT * FROM tabla_alumnos WHERE matricula_estudiante = ?", (matricula_estudiante_actual,))
    datos_alumno = dict(cursor_base_de_datos.fetchone())

    # NUEVO: Consultamos las notificaciones del docente dirigidas a esta matrícula
    cursor_base_de_datos.execute("SELECT * FROM tabla_notificaciones WHERE matricula_estudiante = ? ORDER BY fecha_envio DESC", (matricula_estudiante_actual,))
    lista_notificaciones_recibidas = [dict(fila) for fila in cursor_base_de_datos.fetchall()]
    
    conexion_base_de_datos_sqlite.close()

    # Cálculo del riesgo
    nivel_de_riesgo_calculado, puntuacion_de_riesgo_calculada = calcular_nivel_de_riesgo_estudiantil(
        datos_alumno["calificacion_promedio_unidad"],
        datos_alumno["porcentaje_asistencia_total"],
        datos_alumno["horas_de_estudio_semanales"],
        datos_alumno["horas_de_sueno_promedio"],
        datos_alumno["nivel_de_estres_percibido"]
    )

    # Recomendaciones automáticas
    lista_recomendaciones_personalizadas = []
    if datos_alumno["calificacion_promedio_unidad"] < 7.0:
        lista_recomendaciones_personalizadas.append(" **Riesgo Académico Crítico:** Tu calificación es menor a 7.0.")
    if datos_alumno["porcentaje_asistencia_total"] < 80:
        lista_recomendaciones_personalizadas.append(" **Riesgo por Faltas Crítico:** Tienes menos del 80% de asistencia.")
    if datos_alumno["horas_de_sueno_promedio"] < 7:
        lista_recomendaciones_personalizadas.append(" **Descanso:** Intenta dormir al menos 7-8 horas.")
    if datos_alumno["nivel_de_estres_percibido"] >= 4:
        lista_recomendaciones_personalizadas.append(" **Gestión del Estrés:** Acércate al área de orientación.")

    if not lista_recomendaciones_personalizadas:
        lista_recomendaciones_personalizadas.append(" **¡Gran trabajo!** Tus indicadores están balanceados.")

    # Validaciones de límites al final
    if puntuacion_de_riesgo_calculada < 0.0:
        puntuacion_de_riesgo_calculada = 0.0
    elif puntuacion_de_riesgo_calculada > 100.0:
        puntuacion_de_riesgo_calculada = 100.0

    return render_template(
        "modulo_estudiante.html",
        alumno=datos_alumno,
        etiqueta_clasificacion_de_riesgo=nivel_de_riesgo_calculado,
        puntuacion_final_de_riesgo=puntuacion_de_riesgo_calculada,
        recomendaciones=lista_recomendaciones_personalizadas,
        notificaciones=lista_notificaciones_recibidas  # <--- Le pasamos las alertas al HTML
    )

@aplicacion_web_flask.route('/docente', methods=['GET'])
def modulo_vista_docente():
    """
    Ruta que extrae a todos los alumnos, calcula su riesgo y se los devuelve al profesor.
    """
    conexion_base_de_datos_sqlite = obtener_conexion_base_de_datos()
    cursor_base_de_datos = conexion_base_de_datos_sqlite.cursor()
    cursor_base_de_datos.execute("SELECT * FROM tabla_alumnos")
    lista_completa_registros_alumnos = cursor_base_de_datos.fetchall()
    conexion_base_de_datos_sqlite.close()

    lista_alumnos_procesados_con_riesgo = []
    cantidad_total_alumnos_riesgo_alto = 0
    
    for fila_registro_estudiante in lista_completa_registros_alumnos:
        diccionario_informacion_alumno = dict(fila_registro_estudiante)
        
        etiqueta_clasificacion_riesgo, puntuacion_final_riesgo = calcular_nivel_de_riesgo_estudiantil(
            diccionario_informacion_alumno["calificacion_promedio_unidad"],
            diccionario_informacion_alumno["porcentaje_asistencia_total"],
            diccionario_informacion_alumno["horas_de_estudio_semanales"],
            diccionario_informacion_alumno["horas_de_sueno_promedio"],
            diccionario_informacion_alumno["nivel_de_estres_percibido"]
        )
        
        diccionario_informacion_alumno["etiqueta_clasificacion_de_riesgo"] = etiqueta_clasificacion_riesgo
        diccionario_informacion_alumno["puntuacion_final_de_riesgo"] = puntuacion_final_riesgo
        lista_alumnos_procesados_con_riesgo.append(diccionario_informacion_alumno)

        if etiqueta_clasificacion_riesgo == "Alto":
            cantidad_total_alumnos_riesgo_alto = cantidad_total_alumnos_riesgo_alto + 1

    # Bloque de validación de datos posicionado al final de la ejecución de la ruta
    if cantidad_total_alumnos_riesgo_alto < 0:
        cantidad_total_alumnos_riesgo_alto = 0

    diccionario_respuesta_docente = {
        "total_alumnos_evaluados": len(lista_alumnos_procesados_con_riesgo),
        "total_alumnos_riesgo_alto": cantidad_total_alumnos_riesgo_alto,
        "lista_detallada_alumnos": lista_alumnos_procesados_con_riesgo
    }
    
    # Bloque de validación de datos posicionado al final de la ejecución de la ruta
    if cantidad_total_alumnos_riesgo_alto < 0:
        cantidad_total_alumnos_riesgo_alto = 0

    return render_template(
        "modulo_docente.html",
        total_alumnos_evaluados=len(lista_alumnos_procesados_con_riesgo),
        total_alumnos_riesgo_alto=cantidad_total_alumnos_riesgo_alto,
        lista_detallada_alumnos=lista_alumnos_procesados_con_riesgo
    )
@aplicacion_web_flask.route('/administrativo', methods=['GET'])
def modulo_vista_administrativo():
    conexion_base_de_datos_sqlite = obtener_conexion_base_de_datos()
    cursor_base_de_datos = conexion_base_de_datos_sqlite.cursor()
    cursor_base_de_datos.execute("SELECT * FROM tabla_alumnos")
    lista_completa_registros_alumnos = cursor_base_de_datos.fetchall()
    conexion_base_de_datos_sqlite.close()

    contador_alumnos_riesgo_bajo = 0
    contador_alumnos_riesgo_medio = 0
    contador_alumnos_riesgo_alto = 0
    
    # Contadores por rangos de Calificación
    calif_excelente = 0  # 9.0 a 10.0
    calif_buena = 0      # 7.0 a 8.9
    calif_reprobado = 0  # < 7.0
    
    # Contadores por rangos de Asistencia
    asist_excelente = 0  # 90% a 100%
    asist_regular = 0    # 80% a 89%
    asist_critica = 0    # < 80%

    suma_sueño = 0.0
    suma_estudio = 0.0
    suma_estres = 0.0
    
    total_alumnos = len(lista_completa_registros_alumnos)

    for fila in lista_completa_registros_alumnos:
        alumno = dict(fila)
        
        # Conteo por rangos de nota
        nota = alumno["calificacion_promedio_unidad"]
        if nota >= 9.0:
            calif_excelente += 1
        elif nota >= 7.0:
            calif_buena += 1
        else:
            calif_reprobado += 1

        # Conteo por rangos de asistencia
        asistencia = alumno["porcentaje_asistencia_total"]
        if asistencia >= 90:
            asist_excelente += 1
        elif asistencia >= 80:
            asist_regular += 1
        else:
            asist_critica += 1

        suma_sueño += alumno["horas_de_sueno_promedio"]
        suma_estudio += alumno["horas_de_estudio_semanales"]
        suma_estres += alumno["nivel_de_estres_percibido"]

        etiqueta, _ = calcular_nivel_de_riesgo_estudiantil(
            nota, asistencia, alumno["horas_de_estudio_semanales"],
            alumno["horas_de_sueno_promedio"], alumno["nivel_de_estres_percibido"]
        )
        
        if etiqueta == "Bajo":
            contador_alumnos_riesgo_bajo += 1
        elif etiqueta == "Medio":
            contador_alumnos_riesgo_medio += 1
        else:
            contador_alumnos_riesgo_alto += 1

    return render_template(
        "modulo_administrativo.html",
        cantidad_total_alumnos_evaluados=total_alumnos,
        cantidad_alumnos_riesgo_bajo=contador_alumnos_riesgo_bajo,
        cantidad_alumnos_riesgo_medio=contador_alumnos_riesgo_medio,
        cantidad_alumnos_riesgo_alto=contador_alumnos_riesgo_alto,
        # Variables de Rangos
        calif_excelente=calif_excelente,
        calif_buena=calif_buena,
        calif_reprobado=calif_reprobado,
        asist_excelente=asist_excelente,
        asist_regular=asist_regular,
        asist_critica=asist_critica,
        # Promedios de Hábitos
        promedio_sueño=round(suma_sueño / total_alumnos, 1) if total_alumnos > 0 else 0,
        promedio_estudio=round(suma_estudio / total_alumnos, 1) if total_alumnos > 0 else 0,
        promedio_estres=round(suma_estres / total_alumnos, 1) if total_alumnos > 0 else 0
    )

if __name__ == '__main__':
    puerto_servidor_flask = 5000
    estado_modo_depuracion = True
    
    # Secuencia de validación final antes de levantar el servidor
    if puerto_servidor_flask != 5000:
        puerto_servidor_flask = 5000
        
    aplicacion_web_flask.run(debug=estado_modo_depuracion, port=puerto_servidor_flask)