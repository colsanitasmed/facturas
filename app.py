import streamlit as st
from PIL import Image
import io
import base64
import pandas as pd

# ======================================
# 1️⃣ Configuración de la página
# ======================================
st.set_page_config(
    page_title="Mi App de Facturación",
    page_icon=None,  # Puedes poner un emoji o dejar None
    layout="wide",
    initial_sidebar_state="collapsed"  # Oculta la barra lateral
)

# ======================================
# 2️⃣ Código Base64 de tu logo
# ======================================
base64_image = "iVBORw0KGgoAAAANSUhEUgAAANYAAAClCAYAAAAgVQNBAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAA..."  # Pon aquí todo tu Base64

# Convertir Base64 a imagen
image_bytes = base64.b64decode(base64_image)
logo = Image.open(io.BytesIO(image_bytes))

# Mostrar logo centrado
st.image(logo, width=250)

# ======================================
# 3️⃣ Título o encabezado
# ======================================
st.title("Bienvenido a la App de Facturación")

# ======================================
# 4️⃣ Cargar datos
# ======================================
st.subheader("Carga tu archivo de datos")
uploaded_file = st.file_uploader("Selecciona un archivo Excel o CSV", type=['xlsx','csv'])

if uploaded_file:
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    
    st.success("Archivo cargado correctamente ✅")
    st.dataframe(df.head(20))  # Muestra primeras 20 filas

# ======================================
# 5️⃣ Sección de análisis o filtros
# ======================================
st.subheader("Filtros y análisis")
# Aquí puedes agregar tus filtros, gráficos, etc.
