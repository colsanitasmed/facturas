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
    initial_sidebar_state="collapsed"
)

# =====================================
# Mostrar logo
# =====================================
logo_path = "logo.png"  # Debe estar en la misma carpeta que app.py
try:
    logo = Image.open(logo_path)
    st.image(logo, width=250)
except Exception as e:
    st.warning(f"⚠️ Logo no cargado: {e}")

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

        # =====================================
        # Cuadro para ingresar números de factura
        # =====================================
        st.subheader("🔍 Buscar facturas")
        factura_input = st.text_area(
            "Ingresa los números de factura (separados por comas, espacios o saltos de línea):",
            height=150
        )

        if st.button("Buscar"):
            if factura_input.strip() == "":
                st.warning("⚠️ Por favor, ingresa al menos un número de factura")
            else:
                # Limpiar y separar las facturas ingresadas
                facturas = [f.strip() for f in factura_input.replace("\n", ",").replace(" ", ",").split(",") if f.strip()]
                
                # Filtrar el dataframe
                df_filtrado = df[df["NUMERO FACTURA"].astype(str).isin(facturas)]
                
                if df_filtrado.empty:
                    st.info("No se encontraron facturas con esos números")
                else:
                    st.write(f"Resultados para {len(df_filtrado)} factura(s) encontrada(s):")
                    st.dataframe(df_filtrado)

    except Exception as e:
        st.error(f"❌ Ocurrió un error al leer el archivo: {e}")
else:
    st.info("📌 Por favor, carga un archivo para empezar")

# =====================================
# Footer
# =====================================
st.markdown("---")
st.markdown("App creada por tu equipo de Medicamentos Colsnitas 💡")
