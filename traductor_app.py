import streamlit as st
import pandas as pd
import yaml
import os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from io import BytesIO
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr

# ----------------------------
# CREAR CONFIG.YAML SI NO EXISTE
# ----------------------------
if not os.path.exists("config.yaml"):
    with open("config.yaml", "w") as f:
        f.write("""
credentials:
  usernames: {}

cookie:
  name: eswaju_cookie
  key: clave_secreta_eswaju
  expiry_days: 7

preauthorized:
  emails: []
""")

# ----------------------------
# AUTENTICACIÓN
# ----------------------------
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login(location="main")

# ----------------------------
# REGISTRO DE USUARIO NUEVO
# ----------------------------
if authentication_status is False or authentication_status is None:
    with st.expander("¿No tienes cuenta? Regístrate"):
        new_email = st.text_input("Correo")
        new_name = st.text_input("Nombre completo")
        new_password = st.text_input("Contraseña", type="password")
        if st.button("Registrarse"):
            if new_email and new_name and new_password:
                hashed_pw = stauth.Hasher([new_password]).generate()[0]
                config['credentials']['usernames'][new_email] = {
                    'name': new_name,
                    'password': hashed_pw
                }
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success("✅ Registrado exitosamente. Ahora inicia sesión.")
                st.rerun()
            else:
                st.error("❌ Por favor, completa todos los campos.")

# ----------------------------
# APP PRINCIPAL
# ----------------------------
if authentication_status:
    authenticator.logout("Cerrar sesión", "sidebar")
    st.sidebar.success(f"Bienvenido, {name} 👋")

    # 👥 Mostrar usuarios registrados si eres admin
    if username == "mtorres60036812@gmail.com":
        st.sidebar.markdown("### 👥 Usuarios registrados")
        usuarios = []
        for correo, datos in config['credentials']['usernames'].items():
            usuarios.append({"Correo": correo, "Nombre": datos['name']})
            st.sidebar.write(f"📧 {correo} - {datos['name']}")
        st.sidebar.info(f"🧾 Total registrados: {len(usuarios)}")

        # Descargar Excel
        df_usuarios = pd.DataFrame(usuarios)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df_usuarios.to_excel(writer, index=False, sheet_name='Usuarios')
        st.sidebar.download_button(
            label="⬇️ Descargar usuarios (Excel)",
            data=excel_buffer.getvalue(),
            file_name="usuarios_eswaju.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # ----------------------------
    # INTERFAZ PRINCIPAL DE LA APP
    # ----------------------------
    FONDO_URL = "https://raw.githubusercontent.com/mesiast01/mesias-eswaju/main/fondo_eswaju.png"
    LOGOTIPO_URL = "https://raw.githubusercontent.com/mesiast01/mesias-eswaju/main/logotipo_eswaju.png"

    st.markdown(f"""
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
            margin-top: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'''
        <div style="text-align:center; margin-top:20px; margin-bottom:30px;">
            <img src="{LOGOTIPO_URL}" width="150">
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="title">📘 Traductor ESWAJU: Español – Wampis / Awajún</div>', unsafe_allow_html=True)

    @st.cache_data
    def cargar_datos():
        df = pd.read_csv("diccionario.csv")
        df.columns = df.columns.str.strip().str.lower()
        return df

    df = cargar_datos()

    idioma = st.selectbox("🌐 Selecciona el idioma de destino:", ["Awajún", "Wampis"])
    modo = st.radio("🧭 Modo de traducción:", ["Español → Lengua originaria", "Lengua originaria → Español"])
    palabra = st.text_input("🔤 Ingresa una palabra:")

    # ----------------------------
    # MICRÓFONO (Reconocimiento de voz)
    # ----------------------------
    st.markdown("🎙️ **O usa tu voz para traducir**")

    class AudioProcessor(AudioProcessorBase):
        def recv(self, frame):
            return frame

    mic_enabled = st.toggle("🎤 Activar micrófono para traducir por voz")

    if mic_enabled:
        webrtc_ctx = webrtc_streamer(
            key="speech-to-text",
            mode="SENDONLY",
            audio_receiver_size=256,
            media_stream_constraints={"audio": True, "video": False},
            async_processing=True,
        )

        if webrtc_ctx.audio_receiver:
            try:
                audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=5)
                audio = b"".join([f.to_ndarray().tobytes() for f in audio_frames])
                temp_audio_path = "temp_audio.wav"
                with open(temp_audio_path, "wb") as f:
                    f.write(audio)
                recognizer = sr.Recognizer()
                with sr.AudioFile(temp_audio_path) as source:
                    audio_data = recognizer.record(source)
                    texto_voz = recognizer.recognize_google(audio_data, language='es-PE')
                    st.success(f"🗣️ Dijiste: **{texto_voz}**")
                    palabra = texto_voz
            except Exception as e:
                st.error(f"❌ No se pudo reconocer el audio: {e}")

    # ----------------------------
    # TRADUCCIÓN Y AUDIO
    # ----------------------------
    if palabra:
        palabra_busqueda = palabra.strip().lower()
        idioma_key = "awajun" if idioma == "Awajún" else "wampis"
        columna_origen = "espanol" if "Español" in modo else idioma_key
        columna_destino = idioma_key if "Español" in modo else "espanol"

        if columna_origen in df.columns and columna_destino in df.columns:
            resultado = df[df[columna_origen].str.lower() == palabra_busqueda]
            if not resultado.empty:
                traduccion = resultado.iloc[0][columna_destino]
                st.markdown(f"<h3 style='color:#000000;'>🔁 Traducción: {traduccion}</h3>", unsafe_allow_html=True)

                traduccion_limpia = str(traduccion).strip().lower()

                # Determinar el idioma del audio
                if "Español" in modo:  # Traduciendo desde Awajún/Wampis a Español
                    audio_idioma = "espanol"
                    palabra_audio = traduccion_limpia
                else:  # Traduciendo de Español a Awajún o Wampis
                    audio_idioma = idioma_key
                    palabra_audio = traduccion_limpia

                # Construir URL de audio
                AUDIO_URL = f"https://raw.githubusercontent.com/mesiast01/mesias-eswaju/main/audios/{palabra_audio}_{audio_idioma}.mp3"
                st.audio(AUDIO_URL, format="audio/mp3")
            else:
                st.warning("❌ Palabra no encontrada en el diccionario.")
        else:
            st.error(f"❌ Columnas no válidas en el CSV: {columna_origen} o {columna_destino}")










