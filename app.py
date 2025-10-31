import streamlit as st
import pandas as pd
from PIL import Image

# ======================================
# CONFIGURACIÓN GENERAL
# ======================================
st.set_page_config(
    page_title="Consulta de Facturas - Medicamentos Colsanitas",
    page_icon="💊",
    layout="centered"
)

# ======================================
# ENCABEZADO CON LOGO
# ======================================
try:
    logo = Image.open("logo_colsanitas.png")  # debe estar en la misma carpeta que app.py
    st.image(logo, width=180)
except Exception as e:
    st.warning("⚠️ No se encontró el logo (logo_colsanitas.png). Verifica el nombre y ubicación.")

st.markdown(
    """
    <h1 style='text-align: center; color: #0F3D6E;'>
        🔎 Consulta de Facturas - Medicamentos Colsanitas
    </h1>
    """,
    unsafe_allow_html=True
)

# ======================================
# CAMPO DE ENTRADA DE FACTURAS
# ======================================
st.markdown(
    """
    <p style='color: #0F3D6E; font-size: 18px;'>
        Ingresa una o varias facturas (una por línea o separadas por comas):
    </p>
    """,
    unsafe_allow_html=True
)

facturas_input = st.text_area(
    "Facturas", 
    placeholder="Ejemplo:\nF001234\nF001235\nF001236", 
    height=150, 
    label_visibility="collapsed"
)

# ======================================
# BOTÓN DE BÚSQUEDA
# ======================================
buscar = st.button("🔍 Buscar Facturas", use_container_width=True)

if buscar:
    if facturas_input.strip() == "":
        st.warning("⚠️ Por favor ingresa al menos un número de factura.")
    else:
        facturas = [f.strip() for f in facturas_input.replace(",", "\n").split("\n") if f.strip()]
        st.success(f"Se recibieron **{len(facturas)}** facturas para búsqueda:")
        st.dataframe(pd.DataFrame(facturas, columns=["NÚMERO FACTURA"]))

# ======================================
# PIE DE PÁGINA
# ======================================
st.markdown(
