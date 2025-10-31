import streamlit as st
import pandas as pd
import os

@st.cache_data
def cargar_resumen():
    try:
        base_dir = os.path.dirname(__file__)
    except NameError:
        base_dir = os.getcwd()

    ruta = os.path.join(base_dir, "Facturacion_Resumen.parquet")

    if not os.path.exists(ruta):
        st.error(f"❌ No se encontró el archivo en: {ruta}")
        st.stop()

    return pd.read_parquet(ruta)

resumen = cargar_resumen()

st.title("📦 Consulta de Facturas - Seguimiento")
st.write("Sube tu archivo Excel o CSV con los números de factura a consultar:")

archivo = st.file_uploader("📤 Selecciona tu archivo", type=["xlsx", "csv"])

if archivo is not None:
    try:
        if archivo.name.endswith(".xlsx"):
            facturas = pd.read_excel(archivo)
        else:
            facturas = pd.read_csv(archivo)
        
        facturas.columns = [c.strip().upper() for c in facturas.columns]

        if "NUMERO FACTURA NOTA" not in facturas.columns:
            st.error("❌ El archivo debe tener una columna llamada 'NUMERO FACTURA NOTA'")
        else:
            lista_facturas = facturas["NUMERO FACTURA NOTA"].astype(str).unique().tolist()
            resultado = resumen[resumen["NUMERO FACTURA NOTA"].astype(str).isin(lista_facturas)]

            st.success(f"🔍 Se encontraron {len(resultado)} registros coincidentes.")
            st.dataframe(resultado, use_container_width=True)

            csv = resultado.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Descargar resultados", csv, "Resultados_Facturas.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Error al procesar el archivo: {e}")

else:
    st.info("📎 Esperando que subas tu archivo con las facturas.")
