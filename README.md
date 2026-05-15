# 🚦 Siniestros Viales Fatales · CABA 2019–2024


[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/davidpalacio1/TP-3-Siniestros/blob/main/TP3_Siniestros_Viales_REAL.ipynb)

Análisis completo de víctimas **fatales** en siniestros viales de la Ciudad de Buenos Aires (2019–2024), basado en **datos oficiales** del Observatorio de Movilidad y Seguridad Vial (OMSV) del GCBA.

> **610 víctimas fatales · 6 años de datos · Fuente: Buenos Aires Data (GCBA) · Licencia CC Attribution**

---

## 📓 Análisis completo (notebook)

| Sección | Contenido |
|---|---|
| 1 | Introducción y preguntas guía |
| 2 | Carga y comprensión del dataset oficial |
| 3 | Limpieza y preparación (justificación de decisiones) |
| 4 | EDA — evolución, modo, sexo, edad |
| 5 | Análisis en profundidad — cruces y perfiles comparados |
| 6 | Insights clave (6 hallazgos con interpretación) |
| 7 | Conclusiones y recomendaciones de política pública |

---

## 🔍 Hallazgos principales

**1. Motos y peatones concentran el 81% de las muertes**
256 motociclistas (42%) y 238 peatones (39%) — ambos sin protección física ante impactos.

**2. 2024 es el máximo post-pandemia con 113 víctimas**
El ASPO 2020 redujo un 22% las muertes — prueba de que la siniestralidad escala con el tránsito.

**3. Los motociclistas mueren jóvenes: mediana 31 años, 88% hombres**
El 54% tiene menos de 35 años — perfil del trabajador de delivery sin marco regulatorio.

**4. Los peatones fallecen a edades mayores: mediana 57 años**
El 38% tiene 60+ años — adultos mayores en calles diseñadas para otros cuerpos.

**5. El sesgo de género varía por modo: del 88% (moto) al 58% (peatón)**
La menor brecha en peatones confirma que su vulnerabilidad no depende del comportamiento sino de la infraestructura.

**6. Los ciclistas crecen como grupo de riesgo desde 2022**
La expansión de ciclovías no contuvo la siniestralidad ciclista.

---

## 📁 Estructura del repositorio

```
TP-3-Siniestros/
├── siniestros_viales_victimas.csv          # Dataset oficial (Buenos Aires Data · GCBA)
├── Analisis_Siniestros_Viales.ipynb       # Notebook de análisis completo
└── README.md
```

---

## 📦 Fuente de datos

[Buenos Aires Data — Siniestros viales](https://data.buenosaires.gob.ar/dataset/victimas-siniestros-viales)  
Observatorio de Movilidad y Seguridad Vial (OMSV) · GCBA · Licencia Creative Commons Attribution

---

## 🚀 Cómo correr localmente

```bash
git clone https://github.com/davidpalacio1/TP-3-Siniestros.git
cd TP-3-Siniestros
pip install -r requirements.txt
streamlit run app.py
```

---

## 👤 Autor

**David Palacio Velásquez** · Ciencias de Datos y Matemáticas — UBA  
[LinkedIn](https://www.linkedin.com/in/davidpalacio-velasquez-3864b6298) · [GitHub](https://github.com/davidpalacio1)
