import streamlit as st
import pandas as pd

# Cargar datos desde el CSV
@st.cache_data
def cargar_datos():
    df = pd.read_csv("diccionario.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = cargar_datos()

# Estilos de fondo y fuente
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://raw.githubusercontent.com/mesiast01/MESIAS/main/fondo_eswaju.png');  /* cambia por tu ruta si está local */
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Segoe UI', sans-serif;
        color: #2F2F2F;
    }
    h1, .title {
        color: #8B0000;
    }
    .big-text {
        font-size: 25px;
        font-weight: bold;
        color: #8B0000;
    }
    </style>
""", unsafe_allow_html=True)

# Mostrar logo en la parte superior
st.image("logo_eswaju.png", width=180)  # Asegúrate que el logo esté en el mismo directorio o usa ruta completa

# Título principal
st.markdown('<p class="big-text">📘 Traductor ESWAJU: Awajún / Wampis – Español</p>', unsafe_allow_html=True)

# Selección de idioma
idioma = st.selectbox("🌐 Selecciona el idioma de destino:", ["Awajún", "Wampis"])

# Modo de traducción
modo = st.radio("⚙️ Modo de traducción:", ["Español → Lengua originaria", "Lengua originaria → Español"])

# Entrada de palabra
palabra = st.text_input("🔤 Ingresa una palabra:")

# Lógica de traducción
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
                st.success(f"🔁 Traducción: {traduccion}")
            else:
                st.warning("❌ Palabra no encontrada en el diccionario.")
        except Exception as e:
            st.error(f"⚠️ Error al buscar la palabra: {e}")
    else:
        st.error(f"❌ Columnas no válidas en el CSV: {columna_origen} o {columna_destino}")
