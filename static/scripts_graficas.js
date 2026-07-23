document.addEventListener("DOMContentLoaded", function () {
    
    // 1. GRÁFICA DE DONA: Riesgo
    const canvas_dona = document.getElementById("grafica_dona_riesgo");
    if (canvas_dona) {
        new Chart(canvas_dona.getContext("2d"), {
            type: "doughnut",
            data: {
                labels: ["Riesgo Bajo", "Riesgo Medio", "Riesgo Alto"],
                datasets: [{
                    data: [
                        parseInt(canvas_dona.getAttribute("data-bajo")) || 0,
                        parseInt(canvas_dona.getAttribute("data-medio")) || 0,
                        parseInt(canvas_dona.getAttribute("data-alto")) || 0
                    ],
                    backgroundColor: ["#198754", "#ffc107", "#dc3545"],
                    borderWidth: 2
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "bottom" } } }
        });
    }

    // 2. BARRAS DE CALIFICACIONES (Desglosada por Rangos)
    const canvas_calif = document.getElementById("grafica_barras_calificacion");
    if (canvas_calif) {
        new Chart(canvas_calif.getContext("2d"), {
            type: "bar",
            data: {
                labels: ["Excelente (9.0 - 10)", "Aprobatoria (7.0 - 8.9)", "Reprobatoria (< 7.0)"],
                datasets: [{
                    label: "Número de Alumnos",
                    data: [
                        parseInt(canvas_calif.getAttribute("data-excelente")) || 0,
                        parseInt(canvas_calif.getAttribute("data-buena")) || 0,
                        parseInt(canvas_calif.getAttribute("data-reprobado")) || 0
                    ],
                    backgroundColor: ["#198754", "#0d6efd", "#dc3545"],
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    }

    // 3. BARRAS DE ASISTENCIA (Desglosada por Rangos)
    const canvas_asist = document.getElementById("grafica_barras_asistencia");
    if (canvas_asist) {
        new Chart(canvas_asist.getContext("2d"), {
            type: "bar",
            data: {
                labels: ["Excelente (90% - 100%)", "Regular (80% - 89%)", "Crítica (< 80%)"],
                datasets: [{
                    label: "Número de Alumnos",
                    data: [
                        parseInt(canvas_asist.getAttribute("data-excelente")) || 0,
                        parseInt(canvas_asist.getAttribute("data-regular")) || 0,
                        parseInt(canvas_asist.getAttribute("data-critica")) || 0
                    ],
                    backgroundColor: ["#198754", "#0dcaf0", "#dc3545"],
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    }

    // 4. BARRAS DE HÁBITOS
    const canvas_habitos = document.getElementById("grafica_barras_habitos");
    if (canvas_habitos) {
        new Chart(canvas_habitos.getContext("2d"), {
            type: "bar",
            data: {
                labels: ["Horas Sueño / Noche", "Horas Estudio / Semana", "Nivel Estrés (1-5)"],
                datasets: [{
                    label: "Promedio General",
                    data: [
                        parseFloat(canvas_habitos.getAttribute("data-sueno")) || 0,
                        parseFloat(canvas_habitos.getAttribute("data-estudio")) || 0,
                        parseFloat(canvas_habitos.getAttribute("data-estres")) || 0
                    ],
                    backgroundColor: ["#0d6efd", "#20c997", "#fd7e14"],
                    borderRadius: 5
                }]
            },
            options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
        });
    }
});