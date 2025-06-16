import streamlit as st
import pandas as pd

# Cargar los datos desde el CSV
@st.cache_data
def cargar_datos():
    df = pd.read_csv("diccionario.csv")
    df.columns = df.columns.str.strip().str.lower()  # normaliza nombres de columnas
    return df

df = cargar_datos()

# Ver columnas reales (solo para depurar)
# st.write("Columnas detectadas:", df.columns.tolist())

# Título principal
st.markdown("📘 **Traductor ESWAJU: Awajún / Wampis – Español**")

# Selección de idioma
idioma = st.selectbox("Selecciona el idioma de destino:", ["Awajún", "Wampis"])

# Modo de traducción
modo = st.radio("Modo de traducción:", ["Español → Lengua originaria", "Lengua originaria → Español"])

# Entrada de palabra
palabra = st.text_input("🔤 Ingresa una palabra:")

if palabra:
    palabra_busqueda = palabra.strip().lower()

    # Convertir idioma visual a clave de columna
    idioma_key = "awajun" if idioma == "Awajún" else "wampis"

    if modo == "Español → Lengua originaria":
        columna_origen = "espanol"
        columna_destino = idioma_key
    else:
        columna_origen = idioma_key
        columna_destino = "espanol"

    # Validar si las columnas existen antes de acceder
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
