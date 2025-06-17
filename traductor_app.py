import streamlit as st
import pandas as pd

# Fondo personalizado
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://raw.githubusercontent.com/mesiast01/MESIAS/main/fondo_eswaju.png');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #fdfdfd;
    }
    .title-text {
        font-size: 36px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
    }
    .sub-text {
        font-size: 18px;
        color: #eeeeee;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Mostrar logo centrado
st.markdown("""
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/mesiast01/MESIAS/main/logo_eswaju.png" alt="Logo ESWAJU" width="150">
    </div>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="title-text">📘 Traductor ESWAJU: Awajún / Wampis – Español</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Herramienta de traducción intercultural basada en lenguas originarias</div><br>', unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("diccionario.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = cargar_datos()

# Selección de idioma
idioma = st.selectbox("🌐 Selecciona el idioma de destino:", ["Awajún", "Wampis"])

# Modo de traducción
modo = st.radio("🧭 Modo de traducción:", ["Español → Lengua originaria", "Lengua originaria → Español"])

# Entrada
palabra = st.text_input("🔤 Ingresa una palabra:")

# Procesar traducción
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
            st.success(f"🔁 Traducción: {traduccion}")
        else:
            st.warning("❌ Palabra no encontrada en el diccionario.")
    else:
        st.error(f"❌ Columnas no válidas en el CSV: {columna_origen} o {columna_destino}")

