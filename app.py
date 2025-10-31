import streamlit as st
import pandas as pd

# =====================================
# CONFIGURACIÓN INICIAL
# =====================================
st.set_page_config(page_title="Consulta de Facturas", layout="wide")

# =====================================
# LOGO Y TÍTULO
# =====================================
col1, col2 = st.columns([8, 1])
with col1:
    st.title("🔍 Consulta de Facturación")
    st.markdown("App creada por tu equipo de **Medicamentos Colsanitas 💡**")
with col2:
    st.image("/content/Logo.png", width=120)

# =====================================
# ESTILO PERSONALIZADO
# =====================================
st.markdown("""
    <style>
        /* Fondo blanco */
        .stApp {
            background-color: white !important;
        }

        /* Botones personalizados */
        div.stButton > button:first-child {
            background-color: #7AB68E;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-weight: bold;
            transition: 0.3s;
        }

        div.stButton > button:first-child:hover {
            background-color: #6CA77F;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================
# CARGA DE DATOS
# =====================================
ruta_resumen = '/content/drive/MyDrive/Parquet_Olap/Facturacion_Resumen.parquet'
resumen = pd.read_parquet(ruta_resumen)

# =====================================
# ENTRADA DE FACTURAS
# =====================================
st.markdown("### 🔢 Ingrese uno o varios números de factura (separados por coma o salto de línea):")
input_facturas = st.text_area("", placeholder="Ejemplo: 12345, 67890, 112233")

# =====================================
# BOTÓN DE BÚSQUEDA
# =====================================
buscar = st.button("Buscar Factura")

# =====================================
# PROCESO DE BÚSQUEDA
# =====================================
if buscar:
    facturas = [x.strip() for x in input_facturas.replace("\n", ",").split(",") if x.strip()]
    if facturas:
        resultados = resumen[resumen["NUMERO FACTURA NOTA"].astype(str).isin(facturas)]
        if not resultados.empty:
            st.success(f"✅ Se encontraron {len(resultados)} registros.")
            st.dataframe(resultados)

            # Botón de descarga
            csv = resultados.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Descargar Resultados en CSV",
                data=csv,
                file_name="Facturas_Encontradas.csv",
                mime="text/csv",
                key="descarga",
            )
        else:
            st.warning("⚠️ No se encontraron facturas con esos números.")
    else:
        st.error("Por favor ingresa al menos un número de factura.")
