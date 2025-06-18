import streamlit as st
import pandas as pd
import base64
from PIL import Image

# Función para convertir imagen a base64
def imagen_a_base64(ruta):
    with open(ruta, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Establecer fondo desde imagen local convertida a base64
fondo_base64 = imagen_a_base64("fondo_eswaju.png")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{fondo_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .title {{
        font-size: 32px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 2px 2px 4px #000000;
        text-align: center;
        margin-top: -20px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Mostrar logo local
LOGO_URL = "https://raw.githubusercontent.com/mesiast01/MESIAS/main/logo_eswaju.png"
st.image(LOGO_URL, width=150)

# Título
st.markdown('<div class="title">📘 Traductor ESWAJU: Awajún / Wampis – Español</div>', unsafe_allow_html=True)

# Cargar diccionario
@st.cache_data
def cargar_datos():
    df = pd.read_csv("diccionario.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = cargar_datos()

# Interfaz
st.markdown("\n")  # Espacio
idioma = st.selectbox("🌐 Selecciona el idioma de destino:", ["Awajún", "Wampis"])
modo = st.radio("🧭 Modo de traducción:", ["Español → Lengua originaria", "Lengua originaria → Español"])
palabra = st.text_input("🔤 Ingresa una palabra:")

# Lógica de traducción
if palabra:
    palabra_busqueda = palabra.strip().lower()
    idioma_key = "awajun" if idioma == "Awajún" else "wampis"
    columna_origen = "espanol" if "Español" in modo else idioma_key
    columna_destino = idioma_key if "Español" in modo else "espanol"

    if columna_origen in df.columns and columna_destino in df.columns:
        resultado = df[df[columna_origen].str.lower() == palabra_busqueda]
        if not resultado.empty:
            traduccion = resultado.iloc[0][columna_destino]
            st.markdown(f"<h3 style='color:#00ffcc;'>🔁 Traducción: {traduccion}</h3>", unsafe_allow_html=True)
        else:
            st.warning("❌ Palabra no encontrada en el diccionario.")
    else:
        st.error(f"❌ Columnas no válidas en el CSV: {columna_origen} o {columna_destino}")


