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
        st.error(f"❌ No se encontró el archivo '{ruta}'. Asegúrate de subirlo al mismo repo que app.py.")
        return None

resumen = cargar_resumen()

# =====================================
# 2️⃣ Configuración de la interfaz
# =====================================
st.set_page_config(
    page_title="Consulta de Facturas",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# 3️⃣ Cabecera con logo
# =============================
col1, col2 = st.columns([1, 5])
with col1:
    st.image("/content/Diapositiva1.PNG", width=80)  # logo de tu empresa
with col2:
    st.markdown(
        "<h1 style='color:#2F4F4F;'>📦 Consulta de Facturas - Seguimiento</h1>",
        unsafe_allow_html=True
    )

st.markdown("---")

# =============================
# 4️⃣ Sidebar opcional
# =============================
with st.sidebar:
    st.header("⚙️ Opciones")
    st.markdown("Este panel permite filtrar y buscar facturas fácilmente.")
    st.markdown("Sube tu archivo `.parquet` si deseas reemplazar la base actual.")
    archivo_subido = st.file_uploader("📂 Subir Facturacion_Resumen.parquet", type=["parquet"])
    if archivo_subido is not None:
        resumen = pd.read_parquet(archivo_subido)
        st.success("✅ Base reemplazada correctamente.")

# =============================
# 5️⃣ Lógica de búsqueda
# =============================
if resumen is not None:
    st.success("✅ Base de datos cargada correctamente.")

    st.markdown("### 🔍 Ingresar facturas a consultar")
    facturas_input = st.text_area(
        "✏️ Ingresa uno o varios números de factura (separados por coma, salto de línea o espacio):",
        height=150
    )

    if st.button("🔎 Consultar Facturas", type="primary"):
        if facturas_input.strip() == "":
            st.warning("⚠️ Por favor ingresa al menos un número de factura.")
        else:
            facturas = [
                f.strip()
                for f in facturas_input.replace(",", "\n").replace(" ", "\n").split("\n")
                if f.strip() != ""
            ]
            resultado = resumen[resumen["NUMERO FACTURA NOTA"].astype(str).isin(facturas)]

            if resultado.empty:
                st.warning("⚠️ No se encontraron coincidencias para las facturas ingresadas.")
            else:
                st.success(f"✅ Se encontraron {len(resultado)} registros.")

                # Mostrar resultado en tabla con scroll horizontal
                st.dataframe(resultado, use_container_width=True)

                # Descargar CSV
                csv = resultado.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Descargar resultados en CSV",
                    data=csv,
                    file_name="resultado_facturas.csv",
                    mime="text/csv",
                )
else:
    st.stop()
