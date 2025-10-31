import streamlit as st
import pandas as pd
from PIL import Image
import os

# ======================================
# CONFIGURACIÓN GENERAL
# ======================================
st.set_page_config(
    page_title="Consulta de Facturas - Medicamentos Colsanitas",
    page_icon="💊",
    layout="wide"
)

# ======================================
# ESTILOS PERSONALIZADOS (FONDO BLANCO)
# ======================================
st.markdown("""
    <style>
        .main {
            background-color: white !important;
        }
        [data-testid="stAppViewContainer"] {
            background-color: white !important;
        }
        [data-testid="stHeader"], [data-testid="stSidebar"] {
            background-color: white !important;
        }
        h1, h2, h3, p, label {
            color: #0F3D6E !important;
        }
        .stButton>button {
            background-color: #0F3D6E;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            height: 3em;
        }
    </style>
""", unsafe_allow_html=True)

# ======================================
# CARGA DE BASE
# ======================================
@st.cache_data
def cargar_resumen():
    ruta = "Facturacion_Resumen.parquet"
    if os.path.exists(ruta):
        return pd.read_parquet(ruta)
    else:
        st.error(f"❌ No se encontró el archivo '{ruta}'.")
        return None

resumen = cargar_resumen()

# ======================================
# ENCABEZADO CON LOGO A LA DERECHA
# ======================================
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(
        """
        <h1 style='text-align: center; color: #0F3D6E; margin-top: 20px;'>
            🔎 Consulta de Facturas - Medicamentos Colsanitas
        </h1>
        """,
        unsafe_allow_html=True
    )
with col2:
    try:
        logo = Image.open("Logo.png")  # asegúrate que esté en la misma carpeta
        st.image(logo, width=150)
    except Exception:
        st.warning("⚠️ Logo no encontrado (Logo.png).")

st.markdown("<hr>", unsafe_allow_html=True)

# ======================================
# CAMPO DE ENTRADA DE FACTURAS
# ======================================
st.markdown(
    """
    <p style='font-size: 18px;'>
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
    if resumen is None:
        st.error("❌ No hay base de datos cargada.")
    elif facturas_input.strip() == "":
        st.warning("⚠️ Por favor ingresa al menos un número de factura.")
    else:
        facturas = [
            f.strip()
            for f in facturas_input.replace(",", "\n").split("\n")
            if f.strip() != ""
        ]
        
        resultado = resumen[
            resumen["NUMERO FACTURA NOTA"].astype(str).isin(facturas)
        ]

        if resultado.empty:
            st.warning("⚠️ No se encontraron coincidencias.")
        else:
            st.success(f"✅ Se encontraron {len(resultado)} registros.")
            st.dataframe(resultado, use_container_width=True)

            # Botón de descarga CSV
            csv = resultado.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Descargar resultados en CSV",
                data=csv,
                file_name="resultado_facturas.csv",
                mime="text/csv",
            )

# ======================================
# PIE DE PÁGINA
# ======================================
st.markdown(
    """
    <hr>
    <p style='text-align: center; color: gray;'>
        App creada por tu equipo de <b>Medicamentos Colsanitas 💡</b>
    </p>
    """,
    unsafe_allow_html=True
)
