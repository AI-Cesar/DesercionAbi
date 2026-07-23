def calcular_nivel_de_riesgo_estudiantil(
    calificacion_promedio_unidad, 
    porcentaje_asistencia_total, 
    horas_de_estudio_semanales, 
    horas_de_sueno_promedio, 
    nivel_de_estres_percibido
):
    """
    Calcula el riesgo de deserción aplicando las reglas estrictas de reprobación 
    (asistencia menor a 80% o calificación menor a 7.0) y el modelo de ponderación.
    """
    
    # 1. Evaluación Académica 
    penalizacion_por_bajas_calificaciones = (10.0 - calificacion_promedio_unidad) * 10.0
    penalizacion_por_faltas_de_asistencia = 100.0 - porcentaje_asistencia_total
    
    # 2. Evaluación de Hábitos
    penalizacion_por_falta_de_sueno = (8.0 - horas_de_sueno_promedio) * 12.5
    penalizacion_por_alto_estres = (nivel_de_estres_percibido / 5.0) * 100.0
    penalizacion_por_falta_de_estudio = 100.0 - (horas_de_estudio_semanales * 5.0)
    
    # 3. Ponderación por bloques
    riesgo_ponderado_seccion_academica = (penalizacion_por_bajas_calificaciones * 0.5) + (penalizacion_por_faltas_de_asistencia * 0.5)
    riesgo_ponderado_seccion_habitos = (penalizacion_por_falta_de_sueno * 0.3) + (penalizacion_por_alto_estres * 0.4) + (penalizacion_por_falta_de_estudio * 0.3)
    
    # 4. Fórmula final (60% Académico, 40% Hábitos)
    puntuacion_final_de_riesgo_calculado = (riesgo_ponderado_seccion_academica * 0.6) + (riesgo_ponderado_seccion_habitos * 0.4)
    
    # 5. Asignación de la etiqueta visual original
    etiqueta_clasificacion_de_riesgo = "Indefinido"
    
    if puntuacion_final_de_riesgo_calculado <= 30.0:
        etiqueta_clasificacion_de_riesgo = "Bajo"
    elif puntuacion_final_de_riesgo_calculado <= 60.0:
        etiqueta_clasificacion_de_riesgo = "Medio"
    else:
        etiqueta_clasificacion_de_riesgo = "Alto"

    # Reglas estrictas: Si reprueba por calificación o faltas, se impone riesgo Alto inmediatamente
    if calificacion_promedio_unidad < 7.0 or porcentaje_asistencia_total < 80:
        etiqueta_clasificacion_de_riesgo = "Alto"
        
        # Ajustamos la puntuación a un mínimo de 80 para reflejar la gravedad de reprobar
        if puntuacion_final_de_riesgo_calculado < 80.0:
            puntuacion_final_de_riesgo_calculado = 80.0
        
    # 6. Validaciones de límites al final de la lógica para asegurar coherencia en los datos
    if penalizacion_por_falta_de_sueno < 0.0:
        penalizacion_por_falta_de_sueno = 0.0
        
    if penalizacion_por_falta_de_estudio < 0.0:
        penalizacion_por_falta_de_estudio = 0.0
        
    if puntuacion_final_de_riesgo_calculado < 0.0:
        puntuacion_final_de_riesgo_calculado = 0.0
        
    if puntuacion_final_de_riesgo_calculado > 100.0:
        puntuacion_final_de_riesgo_calculado = 100.0
        
    return etiqueta_clasificacion_de_riesgo, round(puntuacion_final_de_riesgo_calculado, 2)