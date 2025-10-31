import streamlit as st
import pandas as pd
import os

# ==============================
# 1️⃣ Cargar base de facturación
# ==============================
@st.cache_data
def cargar_resumen():
    ruta = '/content/drive/MyDrive/Parquet_Olap/Facturacion_Resumen.parquet'
    if not os.path.exists(ruta):
        st.error(f"❌ No se encontró el archivo en la ruta: {ruta}")
        return pd.DataFrame()
    return pd.read_parquet(ruta)

resumen = cargar_resumen()

st.title("📦 Consulta de Facturas - Seguimiento")
st.write("Pega los números de factura que deseas consultar (uno por línea o separados por comas):")

# ==============================
# 2️⃣ Cuadro de texto para ingresar facturas
# ==============================
entrada = st.text_area("✏️ Ingresa los números de factura aquí:")

if entrada.strip():
    # Normalizar entrada (puede venir separada por comas, espacios o saltos de línea)
    facturas_input = [x.strip() for x in entrada.replace(",", "\n").split("\n") if x.strip()]

    # Buscar facturas
    resultado = resumen[resumen["NUMERO FACTURA NOTA"].astype(str).isin(facturas_input)]

    # Mostrar resultados
    st.success(f"🔍 Se encontraron {len(resultado)} registros coincidentes.")
    st.dataframe(resultado)

    # Botón para descarga
    csv = resultado.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Descargar resultados", csv, "Resultados_Facturas.csv", "text/csv")
else:
    st.info("📎 Esperando que ingreses los números de factura.")
