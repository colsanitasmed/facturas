import streamlit as st
import pandas as pd

def cargar_resumen():
    ruta = "/content/drive/MyDrive/Parquet_Olap/Facturacion_Resumen.parquet"
    return pd.read_parquet(ruta)

resumen = cargar_resumen()

st.title("📦 Consulta de Facturas - Seguimiento")
st.write("Sube tu archivo Excel con los números de factura a consultar:")

archivo = st.file_uploader("Selecciona tu archivo Excel", type=["xlsx"])
if archivo is not None:
    facturas = pd.read_excel(archivo)
    resultado = resumen[resumen['NUMERO FACTURA NOTA'].isin(facturas.iloc[:, 0].astype(str))]
    st.write("✅ Resultados encontrados:")
    st.dataframe(resultado)
