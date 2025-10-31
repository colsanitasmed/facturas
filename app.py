# app.py
import streamlit as st
import pandas as pd
from PIL import Image
import os

# =====================================
# Configuración de la página
# =====================================
st.set_page_config(
    page_title="Consulta de Facturas",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"  # Oculta la barra lateral
)

# =====================================
# Mostrar logo
# =====================================
logo_path = "logo.png"  # Debe estar en la misma carpeta que app.py
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=250)
else:
    st.warning("⚠️ Logo no encontrado en la carpeta de la app")

st.title("💊 Consulta de Facturas")

# =====================================
# Cargar base de datos
# =====================================
st.subheader("📂 Cargar archivo de facturación")
uploaded_file = st.file_uploader("Selecciona un archivo Parquet o Excel", type=["parquet", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".parquet"):
            df = pd.read_parquet(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ Archivo cargado correctamente")
        st.dataframe(df.head(10))  # Muestra las primeras 10 filas

        # Ejemplo: filtrado por número de factura
        factura = st.text_input("Buscar por número de factura:")
        if factura:
            df_filtrado = df[df["NUMERO FACTURA"].astype(str).str.contains(factura)]
            st.write(f"Resultados para factura: {factura}")
            st.dataframe(df_filtrado)

    except Exception as e:
        st.error(f"❌ Ocurrió un error al leer el archivo: {e}")
else:
    st.info("📌 Por favor, carga un archivo para empezar")

# =====================================
# Footer o información adicional
# =====================================
st.markdown("---")
st.markdown("App creada por tu equipo de Analítica 💡")
