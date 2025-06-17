import streamlit as st
import pandas as pd

# Fondo desde imagen en GitHub (puedes cambiar el link a tu imagen)
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://raw.githubusercontent.com/mesiast01/MESIAS/main/mi_traductor/img/fondo_eswaju.png');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f5f5f5;
    }
    h1, .stTextInput>div>div>input {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Mostrar logo centrado
st.markdown("""
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/mesiast01/MESIAS/main/mi_traductor/img/logo_eswaju.png" width="180">
    </div>
""", unsafe_allow_html=True)

# Cargar CSV
@st.cache_data
def cargar_datos():
    df = pd.read_csv("diccionario.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = cargar_datos()

# Título principal
st.markdown("## 📘 Traductor **ESWAJU**: Awajún / Wampis – Español")

# Selección de idioma
idioma = st.selectbox("🌐 Selecciona el idioma de destino:", ["Awajún", "Wampis"])

# Modo de traducción
modo = st.radio("🧭 Modo de traducción:", ["Español → Lengua originaria", "Lengua originaria → Español"])

# Entrada de texto
palabra = st.text_input("🔤 Ingresa una palabra:")

# Traducción
if palabra:
    palabra_busqueda = palabra.strip().lower()
    idioma_key = "awajun" if idioma == "Awajún" else "wampis"

    columna_origen = "espanol" if "Español" in modo else idioma_key
    columna_destino = idioma_key if "Español" in modo else "espanol"

    if columna_origen in df.columns and columna_destino in df.columns:
        resultado = df[df[columna_origen].str.lower() == palabra_busqueda]
        if not resultado.empty:
            traduccion = resultado.iloc[0][columna_destino]
            st.success(f"🔁 Traducción: {traduccion}")
        else:
            st.warning("❌ Palabra no encontrada en el diccionario.")
    else:
        st.error("⚠️ Error con las columnas en el archivo CSV.")
