# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 18:34:03 2024

@author: giovi
"""

import streamlit as st
import pandas as pd
import os

ruta_carpeta = r"data"
ruta_logo =r"data/logo.png" 
st.title("Visualización de Métricas de NGS")

def cargar_archivos_csv(ruta_carpeta):
    dataframes = {}
    for archivo in os.listdir(ruta_carpeta):
        if archivo.endswith("Generalal.txt"):
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            df = pd.read_csv(ruta_archivo, index_col=0, sep='\t')
            dataframes[archivo] = df
    return dataframes

# Definir estado inicial
def estado_inicial():
    st.session_state["selected_file"] = "Todas las tandas"
    st.session_state["selected_metrics"] = []
    st.session_state["selected_patient"] = "Todos"

# Inicializar la carga
if "selected_file" not in st.session_state:
    estado_inicial()

dataframes = cargar_archivos_csv(ruta_carpeta)

# Panel de filtros con logo y botón de reinicio
st.sidebar.image(ruta_logo, width=150)
st.sidebar.title("Filtros")

opciones_tanda = ["Todas las tandas"] + list(dataframes.keys())
selected_file = st.sidebar.selectbox("Selecciona una tanda", opciones_tanda, 
                                     index=opciones_tanda.index(st.session_state["selected_file"]))

metricas_disponibles = [
    "Raw Reads (All reads)", "Paired Reads", "Mapped Reads", "Fraction of Mapped Reads",
    "Mapped Data(Mb)", "Fraction of Mapped Data(Mb)", "Singletons", "Fraction of PCR duplicate reads",
    "Map quality cutoff value", "MapQuality above cutoff reads", "Fraction of MapQ reads in all reads",
    "Target Reads", "Fraction of Target Reads in all reads", "Average depth", "Coverage (>0x)",
    "Coverage (>=10x)", "Coverage (>=20x)", "Coverage (>=50x)", "Coverage (>=100x)", "Coverage (>=200x)",
    "Coverage (>=500x)"
]

selected_metrics = st.sidebar.multiselect("Selecciona métricas para visualizar", metricas_disponibles, default=st.session_state["selected_metrics"])

# Restablecer el paciente seleccionado si la tanda cambia
if selected_file != st.session_state["selected_file"]:
    st.session_state["selected_patient"] = "Todos"

if selected_file not in ["Selecciona una tanda", "Todas las tandas"]:
    opciones_pacientes = ["Todos"] + list(dataframes[selected_file].columns)
else:
    opciones_pacientes = ["Todos"]

selected_patient = st.sidebar.selectbox("Selecciona un paciente", opciones_pacientes, 
                                        index=opciones_pacientes.index(st.session_state["selected_patient"]))

# Reestablecer filtros.
if st.sidebar.button("Restablecer filtros", on_click=estado_inicial):
    pass

# Actualizar valores
st.session_state["selected_file"] = selected_file
st.session_state["selected_metrics"] = selected_metrics
st.session_state["selected_patient"] = selected_patient

# Mostrar datos según las selecciones
if selected_file == "Todas las tandas":
    # Concatenar todas las tandas en un solo DataFrame
    df_concatenado = pd.concat(dataframes.values(), axis=1)
    if selected_metrics:
        df_concatenado = df_concatenado.loc[selected_metrics]
    st.write("Mostrando todas las tandas concatenadas:")
    st.dataframe(df_concatenado, height=500)

elif selected_file != "Selecciona una tanda":
    # Filtrar por las métricas seleccionadas
    if selected_metrics:
        df_filtered = dataframes[selected_file].loc[selected_metrics]
    else:
        df_filtered = dataframes[selected_file]

    if selected_patient == "Todos":
        st.write("Mostrando todas las métricas seleccionadas para todos los pacientes:")
        st.dataframe(df_filtered, height=500)
    else:
        st.write(f"Métricas seleccionadas para el paciente {selected_patient}:")
        st.dataframe(df_filtered[[selected_patient]], height=500)

else:
    st.write("Selecciona una tanda para ver sus métricas.")
