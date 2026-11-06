
# Integrantes: Indira Hamdam Jarava y Cristian Vicioso Escamilla
# Evidencia desarrollada en pareja, según indicación del docente en clase.

# -*- coding: utf-8 -*-
"""
EA2 - Caso de estudio: análisis de tendencias turísticas en Europa 2023
Herramienta seleccionada: Python (Pandas, Matplotlib, Seaborn y Plotly).

INSTRUCCIONES:
1. Guarda este archivo .py y el CSV suministrado por la IU Digital en la misma carpeta.
2. Instala las librerías indicadas en el informe/guía:
   py -m pip install pandas matplotlib seaborn plotly
3. Ejecuta:
   py EA2_Analisis_Turismo_Europa.py
4. Consulta la carpeta "resultados_ea2_turismo" que se creará automáticamente.
"""

from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ------------------------------------------------------------
# 1. Rutas y configuración general
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
CSV_NAME = "DOC03_Datos_U2_IDSD_VIS_TOM_DEC_542_CE.csv"
CSV_PATH = BASE_DIR / CSV_NAME
OUTPUT_DIR = BASE_DIR / "resultados_ea2_turismo"
OUTPUT_DIR.mkdir(exist_ok=True)

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.dpi"] = 130
plt.rcParams["savefig.dpi"] = 180


# ------------------------------------------------------------
# 2. Cargar y validar el conjunto de datos
# ------------------------------------------------------------
def cargar_datos():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            "No se encontró el archivo CSV. Guarda el archivo "
            f"'{CSV_NAME}' en la misma carpeta de este programa.\n"
            f"Carpeta esperada: {BASE_DIR}"
        )

    datos = pd.read_csv(CSV_PATH)

    columnas_requeridas = [
        "fecha", "pais", "ciudad", "latitud", "longitud",
        "tipo_alojamiento", "duracion_estancia", "gasto_diario",
        "valoracion", "transporte", "motivo_viaje"
    ]
    faltantes = [col for col in columnas_requeridas if col not in datos.columns]
    if faltantes:
        raise ValueError(f"El CSV no contiene estas columnas requeridas: {faltantes}")

    # Convertir los campos a sus tipos de datos esperados.
    datos["fecha"] = pd.to_datetime(datos["fecha"], errors="coerce")
    columnas_numericas = [
        "latitud", "longitud", "duracion_estancia", "gasto_diario", "valoracion"
    ]
    for columna in columnas_numericas:
        datos[columna] = pd.to_numeric(datos[columna], errors="coerce")

    if datos["fecha"].isna().any():
        raise ValueError("Hay fechas que no se pudieron interpretar. Revisa la columna 'fecha'.")
    if datos[columnas_numericas].isna().any().any():
        raise ValueError("Hay valores no numéricos en columnas que deberían ser numéricas.")

    datos["mes_numero"] = datos["fecha"].dt.month
    datos["mes"] = datos["mes_numero"].map(lambda numero: MESES[numero - 1])
    datos["mes"] = pd.Categorical(datos["mes"], categories=MESES, ordered=True)

    return datos


# ------------------------------------------------------------
# 3. Visualización 1: viajes por mes (Matplotlib)
# ------------------------------------------------------------
def grafico_viajes_por_mes(datos):
    resumen = datos.groupby("mes", observed=False).size().reindex(MESES, fill_value=0)
    fig, ax = plt.subplots(figsize=(11, 5.8))
    barras = ax.bar(resumen.index, resumen.values)
    ax.set_title("Patrones estacionales: número de viajes por mes", fontsize=15, pad=15)
    ax.set_xlabel("Mes de viaje")
    ax.set_ylabel("Número de viajes")
    ax.tick_params(axis="x", rotation=35)
    ax.bar_label(barras, padding=3, fontsize=8)
    ax.margins(y=0.12)
    fig.tight_layout()
    ruta = OUTPUT_DIR / "01_viajes_por_mes.png"
    fig.savefig(ruta, bbox_inches="tight")
    plt.close(fig)
    resumen.rename_axis("mes").rename("numero_viajes").to_csv(
        OUTPUT_DIR / "resumen_viajes_por_mes.csv", encoding="utf-8-sig"
    )
    return resumen


# ------------------------------------------------------------
# 4. Visualización 2: diez ciudades más visitadas (Matplotlib)
# ------------------------------------------------------------
def grafico_top_ciudades(datos):
    top_ciudades = datos["ciudad"].value_counts().head(10).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6.2))
    barras = ax.barh(top_ciudades.index, top_ciudades.values)
    ax.set_title("Las 10 ciudades más visitadas", fontsize=15, pad=15)
    ax.set_xlabel("Número de viajes registrados")
    ax.set_ylabel("Ciudad")
    ax.bar_label(barras, padding=4, fontsize=9)
    ax.margins(x=0.12)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "02_top_10_ciudades.png", bbox_inches="tight")
    plt.close(fig)
    top_ciudades.sort_values(ascending=False).rename_axis("ciudad").rename(
        "numero_viajes"
    ).to_csv(OUTPUT_DIR / "resumen_top_10_ciudades.csv", encoding="utf-8-sig")
    return top_ciudades.sort_values(ascending=False)


# ------------------------------------------------------------
# 5. Visualización 3: gasto diario por alojamiento (Seaborn)
# ------------------------------------------------------------
def grafico_gasto_alojamiento(datos):
    orden = datos.groupby("tipo_alojamiento")["gasto_diario"].median().sort_values(
        ascending=False
    ).index.tolist()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=datos,
        x="tipo_alojamiento",
        y="gasto_diario",
        order=orden,
        ax=ax,
        showfliers=True
    )
    ax.set_title("Distribución del gasto diario según tipo de alojamiento", fontsize=14, pad=15)
    ax.set_xlabel("Tipo de alojamiento")
    ax.set_ylabel("Gasto diario (unidades monetarias del conjunto simulado)")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "03_gasto_por_alojamiento.png", bbox_inches="tight")
    plt.close(fig)

    resumen = datos.groupby("tipo_alojamiento")["gasto_diario"].agg(
        cantidad="count", promedio="mean", mediana="median",
        q1=lambda serie: serie.quantile(0.25),
        q3=lambda serie: serie.quantile(0.75),
        minimo="min", maximo="max"
    ).round(2).sort_values("mediana", ascending=False)
    resumen.to_csv(OUTPUT_DIR / "resumen_gasto_alojamiento.csv", encoding="utf-8-sig")
    return resumen


# ------------------------------------------------------------
# 6. Visualización 4: satisfacción por país (Plotly interactivo)
# ------------------------------------------------------------
def grafico_satisfaccion_pais(datos):
    fig = px.box(
        datos,
        x="pais",
        y="valoracion",
        color="pais",
        points="outliers",
        title="Distribución de las valoraciones de satisfacción por país",
        labels={"pais": "País", "valoracion": "Valoración (1 a 5)"},
        hover_data=["ciudad", "fecha", "tipo_alojamiento"]
    )
    fig.update_yaxes(range=[0.5, 5.5], dtick=1)
    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        title_x=0.5,
        xaxis_title="País",
        yaxis_title="Valoración (1 = baja, 5 = alta)"
    )
    fig.write_html(
        OUTPUT_DIR / "04_satisfaccion_por_pais_interactivo.html",
        include_plotlyjs=True,
        full_html=True
    )

    # Vista estática para insertar en el informe escrito.
    fig2, ax = plt.subplots(figsize=(10, 5.8))
    sns.boxplot(data=datos, x="pais", y="valoracion", ax=ax, showfliers=False)
    ax.set_title("Valoraciones de satisfacción por país", fontsize=14, pad=15)
    ax.set_xlabel("País")
    ax.set_ylabel("Valoración (1 a 5)")
    ax.set_ylim(0.5, 5.5)
    fig2.tight_layout()
    fig2.savefig(OUTPUT_DIR / "04_satisfaccion_por_pais_vista_estatica.png", bbox_inches="tight")
    plt.close(fig2)

    resumen = datos.groupby("pais")["valoracion"].agg(
        cantidad="count", promedio="mean", mediana="median", desviacion="std"
    ).round(2).sort_values("promedio", ascending=False)
    resumen.to_csv(OUTPUT_DIR / "resumen_satisfaccion_por_pais.csv", encoding="utf-8-sig")
    return resumen


# ------------------------------------------------------------
# 7. Visualización 5: duración promedio por ciudad (Plotly interactivo)
# ------------------------------------------------------------
def grafico_duracion_ciudad(datos):
    resumen = datos.groupby(["pais", "ciudad"], as_index=False).agg(
        duracion_promedio=("duracion_estancia", "mean"),
        cantidad_viajes=("duracion_estancia", "size")
    )
    resumen["duracion_promedio"] = resumen["duracion_promedio"].round(2)
    resumen = resumen.sort_values("duracion_promedio", ascending=True)

    fig = px.bar(
        resumen,
        x="duracion_promedio",
        y="ciudad",
        color="pais",
        orientation="h",
        title="Duración promedio de la estancia por ciudad",
        labels={
            "duracion_promedio": "Duración promedio (días)",
            "ciudad": "Ciudad",
            "pais": "País",
            "cantidad_viajes": "Número de viajes"
        },
        hover_data={"cantidad_viajes": True, "duracion_promedio": ":.2f"}
    )
    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        yaxis_title="Ciudad",
        xaxis_title="Duración promedio (días)",
        height=850
    )
    fig.write_html(
        OUTPUT_DIR / "05_duracion_promedio_por_ciudad_interactivo.html",
        include_plotlyjs=True,
        full_html=True
    )

    # Vista estática para insertar en el informe escrito.
    fig2, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(
        data=resumen,
        x="duracion_promedio",
        y="ciudad",
        hue="pais",
        dodge=False,
        ax=ax
    )
    ax.set_title("Duración promedio de la estancia por ciudad", fontsize=14, pad=15)
    ax.set_xlabel("Duración promedio (días)")
    ax.set_ylabel("Ciudad")
    ax.legend(title="País", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig2.tight_layout()
    fig2.savefig(OUTPUT_DIR / "05_duracion_promedio_por_ciudad_vista_estatica.png", bbox_inches="tight")
    plt.close(fig2)

    resumen.sort_values("duracion_promedio", ascending=False).to_csv(
        OUTPUT_DIR / "resumen_duracion_por_ciudad.csv", index=False, encoding="utf-8-sig"
    )
    return resumen.sort_values("duracion_promedio", ascending=False)


# ------------------------------------------------------------
# 8. Visualización 6: distribución geográfica (Plotly interactivo)
# ------------------------------------------------------------
def grafico_mapa_viajes(datos):
    fig = px.scatter_geo(
        datos,
        lat="latitud",
        lon="longitud",
        color="pais",
        size="duracion_estancia",
        size_max=17,
        opacity=0.38,
        hover_name="ciudad",
        hover_data={
            "fecha": True,
            "pais": True,
            "tipo_alojamiento": True,
            "duracion_estancia": True,
            "gasto_diario": ":.2f",
            "valoracion": True,
            "latitud": False,
            "longitud": False
        },
        scope="europe",
        projection="natural earth",
        title="Distribución geográfica de los viajes en Europa"
    )
    fig.update_geos(
        showcountries=True,
        countrycolor="white",
        showland=True,
        landcolor="rgb(242, 244, 247)",
        showocean=True,
        oceancolor="rgb(226, 239, 249)",
        showlakes=True,
        lataxis_range=[35, 58],
        lonaxis_range=[-7, 16]
    )
    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        legend_title_text="País",
        margin={"r": 10, "t": 60, "l": 10, "b": 10},
        height=700
    )
    fig.write_html(
        OUTPUT_DIR / "06_mapa_interactivo_viajes_europa.html",
        include_plotlyjs=True,
        full_html=True
    )

    # Vista estática de coordenadas para el informe. La versión HTML es el mapa interactivo.
    fig2, ax = plt.subplots(figsize=(10, 6.5))
    for pais, grupo in datos.groupby("pais"):
        ax.scatter(
            grupo["longitud"], grupo["latitud"],
            s=grupo["duracion_estancia"] * 2.4,
            alpha=0.23,
            label=pais,
            edgecolors="none"
        )
    ax.set_title("Vista de coordenadas geográficas de los viajes", fontsize=14, pad=15)
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.legend(title="País", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.grid(True, alpha=0.25)
    ax.set_xlim(-7, 16)
    ax.set_ylim(35, 58)
    fig2.tight_layout()
    fig2.savefig(OUTPUT_DIR / "06_distribucion_geografica_vista_estatica.png", bbox_inches="tight")
    plt.close(fig2)

    return datos[["pais", "ciudad", "latitud", "longitud"]].drop_duplicates().shape[0]


# ------------------------------------------------------------
# 9. Resumen de resultados para la revisión y el informe
# ------------------------------------------------------------
def imprimir_resumen(datos, mensual, top_ciudades, gasto, satisfaccion, duracion, ubicaciones):
    print("\n" + "=" * 70)
    print("EA2 - ANÁLISIS DE TENDENCIAS TURÍSTICAS EN EUROPA 2023")
    print("=" * 70)
    print(f"Registros: {len(datos):,}".replace(",", "."))
    print(f"Columnas originales: 11")
    print(f"Países: {datos['pais'].nunique()} | Ciudades: {datos['ciudad'].nunique()}")
    print(f"Fechas: {datos['fecha'].min().date()} a {datos['fecha'].max().date()}")
    print(f"Valores vacíos: {int(datos.isna().sum().sum())}")
    print(f"Filas duplicadas completas: {int(datos.duplicated().sum())}")
    print(f"Ubicaciones geográficas ciudad-país: {ubicaciones}")

    print("\nMES CON MÁS VIAJES:")
    print(f"{mensual.idxmax()}: {mensual.max()} viajes")
    print("MES CON MENOS VIAJES:")
    print(f"{mensual.idxmin()}: {mensual.min()} viajes")

    print("\nTOP 5 CIUDADES:")
    print(top_ciudades.head(5).to_string())

    print("\nGASTO DIARIO PROMEDIO POR ALOJAMIENTO:")
    print(gasto[["promedio", "mediana"]].to_string())

    print("\nPROMEDIO DE VALORACIÓN POR PAÍS:")
    print(satisfaccion[["promedio", "mediana"]].to_string())

    print("\nCIUDADES CON MAYOR DURACIÓN PROMEDIO:")
    print(duracion[["ciudad", "pais", "duracion_promedio"]].head(5).to_string(index=False))
    print("\nCIUDADES CON MENOR DURACIÓN PROMEDIO:")
    print(duracion[["ciudad", "pais", "duracion_promedio"]].tail(5).sort_values("duracion_promedio").to_string(index=False))

    print("\nArchivos guardados en:")
    print(OUTPUT_DIR)
    print("\nAbre los archivos HTML en un navegador para explorar las visualizaciones interactivas.")
    print("Ejecución finalizada correctamente.")


def main():
    try:
        print("Cargando y validando el archivo CSV...")
        datos = cargar_datos()
        print(f"Se cargaron {len(datos):,} registros.".replace(",", "."))

        print("Creando visualización 1 de 6: viajes por mes...")
        mensual = grafico_viajes_por_mes(datos)

        print("Creando visualización 2 de 6: top 10 ciudades...")
        top_ciudades = grafico_top_ciudades(datos)

        print("Creando visualización 3 de 6: gasto por alojamiento...")
        gasto = grafico_gasto_alojamiento(datos)

        print("Creando visualización 4 de 6: satisfacción por país...")
        satisfaccion = grafico_satisfaccion_pais(datos)

        print("Creando visualización 5 de 6: duración promedio por ciudad...")
        duracion = grafico_duracion_ciudad(datos)

        print("Creando visualización 6 de 6: mapa interactivo...")
        ubicaciones = grafico_mapa_viajes(datos)

        imprimir_resumen(datos, mensual, top_ciudades, gasto, satisfaccion, duracion, ubicaciones)

    except Exception as error:
        print("\nERROR DURANTE LA EJECUCIÓN:")
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
