# EA2 – Análisis de tendencias turísticas en Europa 2023

Proyecto académico de visualización y análisis exploratorio de un conjunto de datos **simulados** de viajes por Europa durante 2023.

## Integrantes

- **Indira Hamdam Jarava**
- **Cristian Vicioso Escamilla**

El trabajo se desarrolla en pareja, de acuerdo con la autorización comunicada por el docente en clase.

## Objetivo

Explorar variables temporales, categóricas, numéricas y geográficas para identificar patrones de viaje, destinos visitados, gasto diario, satisfacción, duración de estancia y distribución espacial.

## Herramientas

Se investigaron Tableau, Power BI y Python. Para el desarrollo se seleccionó Python con las bibliotecas:

- **Pandas:** lectura, preparación y agrupación de los datos.
- **Matplotlib:** gráfico de viajes por mes y recursos gráficos estáticos.
- **Seaborn:** diagrama de caja para comparar gasto diario por alojamiento.
- **Plotly Express:** gráficos interactivos de satisfacción, duración y mapa geográfico.

## Estructura del repositorio

```text
EA2_Turismo_Europa/
├── README.md
├── requirements.txt
├── .gitignore
├── datos/
│   └── DOC03_Datos_U2_IDSD_VIS_TOM_DEC_542_CE.csv
├── codigo/
│   └── EA2_Analisis_Turismo_Europa.py
├── informe/
│   ├── Hamdam_Indira_Vicioso_Cristian_EA2.docx
│   └── Hamdam_Indira_Vicioso_Cristian_EA2.pdf
├── guia/
│   ├── Guia_y_Guion_Video_EA2.docx
│   └── Guia_y_Guion_Video_EA2.pdf
├── visualizaciones/
│   └── resultados_ea2_turismo/
│       ├── gráficos PNG
│       ├── visualizaciones HTML interactivas
│       └── tablas de resumen CSV
└── video/
    └── README.md
```

## Requisitos

- Python 3.10 o superior recomendado.
- Visual Studio Code (opcional, como editor).
- Conexión a Internet no es necesaria para ejecutar el análisis porque el CSV está incluido en `datos/`.

## Instalación y ejecución

Desde la carpeta raíz del repositorio, abre una terminal y ejecuta:

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

Ejecuta el análisis:

```bash
python codigo/EA2_Analisis_Turismo_Europa.py
```

Los archivos se guardan en `visualizaciones/resultados_ea2_turismo/`. Abre los archivos `.html` en un navegador para explorar los gráficos interactivos.

## Visualizaciones desarrolladas

1. **Patrones estacionales:** número de viajes por mes (barras).
2. **Destinos populares:** diez ciudades con más registros de viajes (barras horizontales).
3. **Alojamiento y gasto:** distribución del gasto diario por tipo de alojamiento (diagrama de caja).
4. **Satisfacción por país:** distribución de valoraciones por país (diagrama de caja interactivo y vista estática).
5. **Duración por ciudad:** duración promedio de estancia (barras interactivas y vista estática).
6. **Distribución geográfica:** localización de los viajes con país y duración (mapa interactivo y vista estática de coordenadas).

## Consideraciones sobre los datos

El conjunto de datos fue suministrado como material del caso de estudio de la asignatura y se identifica como simulado. Los resultados describen exclusivamente ese conjunto y **no deben interpretarse como estadísticas oficiales del turismo europeo**. El archivo no especifica la moneda del gasto diario; por ello, el análisis compara valores sin asignar una divisa.

## Entregables

- Informe académico en Word y PDF: carpeta `informe/`.
- Código fuente reproducible: carpeta `codigo/`.
- Datos utilizados: carpeta `datos/`.
- Gráficos y tablas generados: carpeta `visualizaciones/`.
- Guía de configuración y guion del video: carpeta `guia/`.
- Cuando esté grabado, agregar el video MP4 a `video/`.

## Créditos

Actividad académica de la asignatura **Visualización de Toma de Decisiones**, IU Digital de Antioquia.
