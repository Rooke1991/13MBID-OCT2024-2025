# app.py

import streamlit as st

# 1) Configuración de la página (debe ir al principio)
st.set_page_config(
    page_title="Herramienta de Visualización de Datos – 13MBID",
    page_icon="📊",
    layout="wide",
)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 2) Lectura de datos (con separador correcto)
try:
    df = pd.read_csv("../../../data/final/datos_finales.csv", sep=";")
    st.success("✅ Datos cargados correctamente.")
    st.write("Columnas detectadas:", list(df.columns))
except FileNotFoundError:
    st.error("❌ No se encontró el archivo de datos. Verifica la ruta.")
    st.stop()

# 3) Cabecera de la app
st.title("Herramienta de Visualización de Datos – 13MBID")
st.write("Esta aplicación permite explorar y visualizar los datos del proyecto en curso.")
st.write("Desarrollado por: Roque Álvarez Benalcazar")
st.markdown("---")

# 4) Vista previa de los datos
st.subheader("Vista previa de los datos")
st.dataframe(df.head())

# 5) Gráficos
st.header("Gráficos")
st.subheader("Caracterización de los créditos otorgados:")

# 5.1) Histograma de créditos por objetivo
creditos_x_objetivo = px.histogram(
    df,
    x="objetivo_credito",
    title="Conteo de créditos por objetivo"
)
creditos_x_objetivo.update_layout(
    xaxis_title="Objetivo del crédito",
    yaxis_title="Cantidad de créditos"
)
st.plotly_chart(creditos_x_objetivo, use_container_width=True)


# 5.2) Histograma de importes solicitados
hist_importes = px.histogram(
    df,
    x='importe_solicitado',
    nbins=10,
    title='Importes solicitados en créditos'
)
hist_importes.update_layout(
    xaxis_title='Importe solicitado',
    yaxis_title='Cantidad'
)
st.plotly_chart(hist_importes, use_container_width=True)


# 5.3) Pie chart por estado_credito_N
estado_credito_counts = df['estado_credito_N'].value_counts()
pie_estado = go.Figure(data=[
    go.Pie(labels=estado_credito_counts.index, values=estado_credito_counts.values)
])
pie_estado.update_layout(title_text='Distribución de créditos por estado registrado')
st.plotly_chart(pie_estado, use_container_width=True)


# 5.4) Pie chart por falta_pago
falta_pago_counts = df['falta_pago'].value_counts()
pie_mora = go.Figure(data=[
    go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts.values)
])
pie_mora.update_layout(title_text='Distribución de créditos en función de registro de mora')
st.plotly_chart(pie_mora, use_container_width=True)


# 5.5) Barras apiladas: estado_credito_N vs objetivo_credito
barras_apiladas = px.histogram(
    df,
    x='objetivo_credito',
    color='estado_credito_N',
    barmode='stack',
    title='Distribución de créditos por estado y objetivo'
)
barras_apiladas.update_layout(
    xaxis_title='Objetivo del crédito',
    yaxis_title='Cantidad'
)
st.plotly_chart(barras_apiladas, use_container_width=True)


# 5.6) Línea de importe medio por antigüedad del cliente
orden_antiguedad = ['menor_2y', '2y_a_4y', 'mayor_4y']
df_medias = (
    df
    .groupby('antiguedad_cliente')['importe_solicitado']
    .mean()
    .reindex(orden_antiguedad)
    .reset_index()
)
linea_antig = px.line(
    df_medias,
    x='antiguedad_cliente',
    y='importe_solicitado',
    title='Evolución de importes solicitados por antigüedad del cliente'
)
linea_antig.update_layout(
    xaxis_title='Antigüedad del cliente',
    yaxis_title='Importe solicitado promedio'
)
st.plotly_chart(linea_antig, use_container_width=True)


# 5.7) Boxplot: Distribución de importes por objetivo del crédito
box_objetivo = px.box(
    df,
    x='objetivo_credito',
    y='importe_solicitado',
    title='Distribución de importes solicitados por objetivo del crédito'
)
st.plotly_chart(box_objetivo, use_container_width=True)


# 5.8) Scatter: Importe vs Duración del crédito por estado
scatter_imp_dur = px.scatter(
    df,
    x="duracion_credito",
    y="importe_solicitado",
    color="estado_credito_N",
    title="Importe vs Duración del crédito por estado"
)
st.plotly_chart(scatter_imp_dur, use_container_width=True)
