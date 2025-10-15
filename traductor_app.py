import streamlit as st
import pandas as pd
import os
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="Traductor ESWAJU", page_icon="🌎", layout="centered")

# ================================
# 🟦 FUNCIÓN PARA CARGAR LOS DATOS
# ================================
@st.cache_data
def cargar_datos():
    """
    Carga los datos desde diccionario.xlsx (si existe)
    o desde diccionario.csv (como respaldo).
    Combina todas las hojas si hay varias.
    """
    if os.path.exists("diccionario.xlsx"):
        try:
            hojas = pd.read_excel("diccionario.xlsx", sheet_name=None)
            df = pd.concat(hojas.values(), ignore_index=True)
            st.success("📘 Archivo Excel cargado correctamente.")
        except Exception as e:
            st.warning(f"⚠️ Error al leer el Excel: {e}. Se usará el CSV en su lugar.")
            df = pd.read_csv("diccionario.csv")
    elif os.path.exists("diccionario.csv"):
        df = pd.read_csv("diccionario.csv")
        st.info("📄 Cargando desde diccionario.csv (modo clásico).")
    else:
        st.error("❌ No se encontró ningún archivo de diccionario (ni CSV ni XLSX).")
        df = pd.DataFrame(columns=["espanol", "awajun", "wampis"])

    df.columns = df.columns.str.strip().str.lower()
    return df


# ================================
# 🔊 FUNCIÓN PARA REPRODUCIR AUDIO
# ================================
def reproducir_audio(texto, idioma):
    if not texto:
        st.warning("No hay texto para reproducir.")
        return
    try:
        tts = gTTS(text=texto, lang=idioma)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        st.audio(audio_bytes.getvalue(), format="audio/mp3")
    except Exception as e:
        st.error(f"Error al generar audio: {e}")


# ================================
# 🎙️ FUNCIÓN PARA RECONOCER VOZ
# ================================
def reconocer_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Habla ahora (presiona 'Detener' cuando termines)...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        st.success(f"🔎 Texto reconocido: {texto}")
        return texto
    except sr.UnknownValueError:
        st.warning("No se entendió lo que dijiste.")
        return ""
    except sr.RequestError:
        st.error("Error con el servicio de reconocimiento de voz.")
        return ""


# ================================
# 🧩 FUNCIÓN PRINCIPAL DE TRADUCCIÓN
# ================================
def traducir(df, palabra, origen, destino):
    palabra = palabra.strip().lower()
    if palabra == "":
        return "Introduce una palabra."
    if origen not in df.columns or destino not in df.columns:
        return f"No se encontró la columna {origen} o {destino}."
    
    fila = df[df[origen].str.lower() == palabra]
    if not fila.empty:
        traduccion = fila[destino].values[0]
        return traduccion
    else:
        return "No se encontró la traducción."


# ================================
# 🧭 INTERFAZ PRINCIPAL
# ================================
st.title("🌎 Traductor ESWAJU: Español – Wampis / Awajún")

df = cargar_datos()

modo = st.radio("Selecciona el modo de traducción:", [
    "Español → Awajún",
    "Español → Wampis",
    "Awajún → Español",
    "Wampis → Español"
])

col1, col2 = st.columns([2, 1])

with col1:
    palabra = st.text_input("Escribe una palabra o usa el micrófono 🎙️:")

with col2:
    if st.button("🎤 Reconocer voz"):
        palabra = reconocer_voz()

if modo == "Español → Awajún":
    origen, destino, lang = "espanol", "awajun", "es"
elif modo == "Español → Wampis":
    origen, destino, lang = "espanol", "wampis", "es"
elif modo == "Awajún → Español":
    origen, destino, lang = "awajun", "espanol", "es"
else:
    origen, destino, lang = "wampis", "espanol", "es"

if st.button("🔍 Traducir"):
    traduccion = traducir(df, palabra, origen, destino)
    if traduccion:
        st.success(f"**Traducción:** {traduccion}")

        colA, colB = st.columns(2)
        with colA:
            if st.button("🔊 Escuchar palabra original"):
                reproducir_audio(palabra, "es" if origen == "espanol" else "es")
        with colB:
            if st.button("🔊 Escuchar traducción"):
                reproducir_audio(traduccion, "es" if destino == "espanol" else "es")

















