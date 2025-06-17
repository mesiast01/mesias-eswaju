import streamlit as st
import pandas as pd

# URLs directas
FONDO_URL = "https://raw.githubusercontent.com/mesiast01/MESIAS/main/fondo_eswaju.png"
LOGO_URL = "https://raw.githubusercontent.com/mesiast01/MESIAS/main/logo_eswaju.png"

# Estilos y logo
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{FONDO_URL}");
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
st.markdown(f'<div style="text-align:center;"><img src="{LOGO_URL}" width="150"></div>', unsafe_allow_html=True)
st.markdown('<div class="title">📘 Traductor ESWAJU: Awajún / Wampis – Español</div>', unsafe_allow_html=True)

# Carga de datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("diccionario.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = cargar_datos()

# Interfaz
st.markdown("\n")  # Separador visual
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


