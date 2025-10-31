import streamlit as st
import pandas as pd
import os

# =====================================
# 1️⃣ Cargar la base resumen
# =====================================
def cargar_resumen():
    ruta = "Facturacion_Resumen.parquet"
    if os.path.exists(ruta):
        return pd.read_parquet(ruta)
    else:
        st.error(f"❌ No se encontró el archivo '{ruta}'.")
        return None

resumen = cargar_resumen()

# =====================================
# 2️⃣ Configuración de la página
# =====================================
st.set_page_config(
    page_title="Consulta de Facturas",
    page_icon="📦",
    layout="wide"
)

# =====================================
# 3️⃣ Estilo CSS personalizado
# =====================================
st.markdown("""
<style>
    .main {background-color: #f5f5f5; padding: 20px;}
    h1 {color: #1f4e79; font-weight: bold; font-size: 36px; text-align: center;}
    .stButton>button {background-color: #1f4e79; color: white; font-weight: bold;}
    .stTextArea textarea {
        background-color: #ffffff; 
        border: 2px solid #1f4e79; 
        border-radius: 10px; 
        color: #0F3D6E;  /* color del texto */
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# 4️⃣ Cabecera con logo centrado (imagen embebida en bytes)
# =====================================
logo_path = "Logo.PNG"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_bytes = f.read()
    st.image(logo_bytes, width=120)
else:
    st.warning("❌ No se encontró el logo.")
st.markdown("<h1>📦 Consulta de Facturas</h1>", unsafe_allow_html=True)
st.markdown("---")

# =====================================
# 5️⃣ Panel de entrada de facturas
# =====================================
st.markdown("### 🔍 Ingrese los números de factura")
facturas_input = st.text_area(
    "✏️ Separados por coma, espacio o salto de línea",
    height=150
)

# =====================================
# 6️⃣ Lógica de búsqueda y resultados
# =====================================
if st.button("🔎 Consultar Facturas", type="primary"):
    if resumen is None:
        st.warning("❌ No hay base de datos cargada.")
    elif facturas_input.strip() == "":
        st.warning("⚠️ Ingresa al menos un número de factura.")
    else:
        facturas = [
            f.strip()
            for f in facturas_input.replace(",", "\n").replace(" ", "\n").split("\n")
            if f.strip() != ""
        ]
        resultado = resumen[resumen["NUMERO FACTURA NOTA"].astype(str).isin(facturas)]

        if resultado.empty:
            st.warning("⚠️ No se encontraron coincidencias.")
        else:
            st.success(f"✅ Se encontraron {len(resultado)} registros.")
            st.dataframe(resultado, use_container_width=True)

            csv = resultado.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Descargar resultados en CSV",
                data=csv,
                file_name="resultado_facturas.csv",
                mime="text/csv",
            )
