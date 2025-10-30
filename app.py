import streamlit as st
import pandas as pd

# =====================================
# 1️⃣ Cargar la base resumen
# =====================================
ruta_resumen = '/content/drive/MyDrive/Parquet_Olap/Facturacion_Resumen.parquet'
resumen = pd.read_parquet(ruta_resumen)

st.set_page_config(page_title="Consulta de Facturas", layout="wide")

st.title("🔍 Consulta de Estado de Facturas")
st.markdown("Ingrese uno o varios números de factura para ver su estado actual:")

# =====================================
# 2️⃣ Entrada de búsqueda
# =====================================
input_facturas = st.text_area(
    "Números de factura (separados por comas o saltos de línea)",
    placeholder="Ejemplo: 10002345, 10007891, 10009900"
)

if st.button("Buscar"):
    if input_facturas.strip() == "":
        st.warning("Por favor ingrese al menos un número de factura.")
    else:
        # Limpiar y normalizar los números de factura ingresados
        facturas_buscar = [f.strip() for f in input_facturas.replace("\n", ",").split(",") if f.strip()]
        facturas_buscar = [f for f in facturas_buscar if f in resumen['NUMERO FACTURA NOTA'].astype(str).tolist()]

        if not facturas_buscar:
            st.error("❌ Ninguna de las facturas ingresadas fue encontrada.")
        else:
            # Filtrar el DataFrame
            resultado = resumen[resumen['NUMERO FACTURA NOTA'].isin(facturas_buscar)]

            # Mostrar resultados
            st.success(f"Se encontraron {len(resultado)} registros.")
            st.dataframe(resultado)

            # Opción para descargar
            csv = resultado.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Descargar resultados en CSV", data=csv, file_name="consulta_facturas.csv", mime="text/csv")
