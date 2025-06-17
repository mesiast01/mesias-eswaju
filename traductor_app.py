import streamlit as st
import pandas as pd

# ✅ Cambia estas URLs por las tuyas exactas si son diferentes
FONDO_URL = "https://raw.githubusercontent.com/mesiast01/MESIAS/main/fondo_eswaju.png"
LOGO_URL = "https://raw.githubusercontent.com/mesiast01/MESIAS/main/logo_eswaju.png"

# 🖼️ Estilo personalizado con fondo y logo
def set_background_and_logo():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{FONDO_URL}");
            background-size: cover;
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
    st.image(LOGO_URL, width=160)
    st.markdown("<div class='title'>📘 Traductor ESWAJU: Awajún / Wampis – Español</div>", unsafe_allow_html=True)

# 📥 Cargar CSV
@st.cache_data
def cargar_datos():
    df = pd.read_csv("diccionario.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

# 🧠 Ejecutar funciones
set_background_and_logo()
df = cargar_datos()

# 🌍 Selección de idioma
idioma = st.selectbox("🌐 Selecciona el idioma de destino:", ["Awajún", "Wampis"])

# 🔄 Modo de traducción
modo = st.radio("🧭 Modo de traducción:", ["Español → Lengua originaria", "Lengua originaria → Español"])

# 🔤 Entrada de palabra
palabra = st.text_input("🔤 Ingresa una palabra:")

if palabra:
    palabra_busqueda = palabra.strip().lower()
    idioma_key = "awajun" if idioma == "Awajún" else "wampis"

    if modo == "Español → Lengua originaria":
        columna_origen = "espanol"
        columna_destino = idioma_key
    else:
        columna_origen = idioma_key
        columna_destino = "espanol"

    if columna_origen in df.columns and columna_destino in df.columns:
        resultado = df[df[columna_origen].str.lower() == palabra_busqueda]
        if not resultado.empty:
            traduccion = resultado.iloc[0][columna_destino]
            st.markdown(f"<h3 style='color:#00ffcc;'>🔁 Traducción: {traduccion}</h3>", unsafe_allow_html=True)
        else:
            st.warning("❌ Palabra no encontrada en el diccionario.")
    else:
        st.error(f"❌ Columnas no válidas en el CSV: {columna_origen} o {columna_destino}")


