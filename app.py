
import streamlit as st
import pandas as pd
import os

# =====================================
# 1️⃣ Cargar la base resumen
# =====================================
def cargar_resumen():
    ruta = "Facturacion_Resumen.parquet"  # archivo dentro del repo
    if os.path.exists(ruta):
        return pd.read_parquet(ruta)
    else:
        st.error(f"❌ No se encontró el archivo '{ruta}'. Asegúrate de subirlo al mismo repo que app.py.")
        return None

resumen = cargar_resumen()

# =====================================
# 2️⃣ Configuración de la interfaz
# =====================================
st.set_page_config(page_title="Consulta de Facturas", page_icon="📦", layout="wide")
st.title("📦 Consulta de Facturas - Seguimiento")

if resumen is not None:
    st.success("✅ Base de datos cargada correctamente.")

    # Cuadro de texto para pegar facturas
    facturas_input = st.text_area(
        "✏️ Ingresa uno o varios números de factura (separados por coma, salto de línea o espacio):"
    )

    # Botón de búsqueda
    if st.button("🔍 Consultar Facturas"):
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
                st.dataframe(resultado)

                csv = resultado.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Descargar resultados en CSV",
                    data=csv,
                    file_name="resultado_facturas.csv",
                    mime="text/csv",
                )

else:
    st.stop()
