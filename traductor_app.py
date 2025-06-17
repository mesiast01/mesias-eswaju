import streamlit as st
import pandas as pd

# Establecer fondo e imagen de logo
def set_background_and_logo():
    st.markdown("""
        <style>
            .stApp {
                background-image: url("https://raw.githubusercontent.com/mesiast01/MESIAS/main/fondo_eswaju.png");
                background-size: cover;
                background-attachment: fixed;
            }
            .title {
                font-size: 30px;
                font-weight: bold;
                color: #ffffff;
                text-shadow: 2px 2px 4px #000000;
                text-align: center;
                margin-top: -20px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.image("https://raw.githubusercontent.com/mesiast01/MESIAS/main/logo_eswaju.png", width=160)
    st.markdown("<div class='title'>📘 Traductor ESWAJU: Awajún / Wampis – Español</div>", unsafe_allow_html=True)

# Cargar datos desde CSV
@st.cache_data
def cargar_datos():
    df = pd.read_csv("diccionario.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

set_background_and_logo()
df = cargar_datos()

# Descripción
st.markdown("Herramienta de traducción intercultural basada en lenguas originarias")

# Selección de idioma
idioma = st.selectbox("🌐 Selecciona el idioma de destino:", ["Awajún", "Wampis"])

# Modo de traducción
modo = st.radio("🧭 Modo de traducción:", ["Español → Lengua originaria", "Lengua originaria → Español"])

# Entrada de palabra
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
        try:
            resultado = df[df[columna_origen].str.lower() == palabra_busqueda]
            if not resultado.empty:
                traduccion = resultado.iloc[0][columna_destino]
                # 🔵 Texto de resultado más grande y colorido
                st.markdown(f"<h3 style='color:#00ffcc;'>🔁 Traducción: {traduccion}</h3>", unsafe_allow_html=True)
            else:
                st.warning("❌ Palabra no encontrada en el diccionario.")
        except Exception as e:
            st.error(f"⚠️ Error al buscar la palabra: {e}")
    else:
        st.error(f"❌ Columnas no válidas en el CSV: {columna_origen} o {columna_destino}")


