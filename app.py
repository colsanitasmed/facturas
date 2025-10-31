import streamlit as st
import pandas as pd
import os

# ==============================
# 1️⃣ Cargar base de facturación
# ==============================
@st.cache_data
def cargar_resumen():
    # Usar ruta absoluta dentro del entorno Colab
    ruta = os.path.abspath("/content/Facturacion_Resumen.parquet")
    st.write(f"📁 Ruta detectada: {ruta}")  # Muestra la ruta en la app (solo para depurar)
    if not os.path.exists(ruta):
        st.error(f"❌ No se encontró el archivo en la ruta: {ruta}")
        return pd.DataFrame()
    return pd.read_parquet(ruta)

resumen = cargar_resumen()

st.title("📦 Consulta de Facturas - Seguimiento")
st.write("Pega los números de factura que deseas consultar (uno por línea o separados por comas):")

# ==============================
# 2️⃣ Cuadro de texto + botón de búsqueda
# ==============================
entrada = st.text_area("✏️ Ingresa los números de factura aquí:")
buscar = st.button("🔍 Buscar facturas")

if buscar:
    if not entrada.strip():
        st.warning("⚠️ Debes ingresar al menos un número de factura.")
    else:
        # Normalizar entrada (puede venir separada por comas, espacios o saltos de línea)
        facturas_input = [x.strip() for x in entrada.replace(",", "\n").split("\n") if x.strip()]

        if resumen.empty:
            st.error("⚠️ No se pudo cargar la base de facturación.")
        else:
            # Buscar coincidencias
            resultado = resumen[resumen["NUMERO FACTURA NOTA"].astype(str).isin(facturas_input)]

            if len(resultado) > 0:
                st.success(f"✅ Se encontraron {len(resultado)} registros coincidentes.")
                st.dataframe(resultado)

                # Botón para descarga
                csv = resultado.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Descargar resultados", csv, "Resultados_Facturas.csv", "text/csv")
            else:
                st.info("🔎 No se encontraron coincidencias para las facturas ingresadas.")
else:
    st.info("📎 Esperando que ingreses los números de factura y presiones 'Buscar'.")
