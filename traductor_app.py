import streamlit as st
import pandas as pd
import yaml
import os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from io import BytesIO  # Para generar Excel

# ----------------------------
# ARCHIVO DE USUARIOS
# ----------------------------
USUARIOS_FILE = "usuarios.yaml"

if not os.path.exists(USUARIOS_FILE):
    with open(USUARIOS_FILE, "w") as f:
        yaml.dump({"usernames": {}}, f)

# ----------------------------
# CARGAR DATOS DE USUARIOS
# ----------------------------
with open(USUARIOS_FILE, "r") as f:
    usuarios_data = yaml.safe_load(f)

config = {
    'credentials': {
        'usernames': usuarios_data['usernames']
    },
    'cookie': {
        'name': 'eswaju_cookie',
        'key': 'clave_secreta_eswaju',
        'expiry_days': 7
    },
    'preauthorized': {
        'emails': []
    }
}

# ----------------------------
# AUTENTICACIÓN
# ----------------------------
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login(
    form_name='Iniciar sesión',
    location='main'
)

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

                usuarios_data['usernames'][new_email] = {
                    'name': new_name,
                    'password': hashed_pw
                }

                with open(USUARIOS_FILE, 'w') as f:
                    yaml.dump(usuarios_data, f)

                st.success("✅ Registrado exitosamente. Ahora inicia sesión.")
                st.rerun()
            else:
                st.error("❌ Por favor, completa todos los campos.")

# ----------------------------
# APP PRINCIPAL (solo si hay sesión)
# ----------------------------
if authentication_status:
    authenticator.logout("Cerrar sesión", "sidebar")
    st.sidebar.success(f"Bienvenido, {name} 👋")

    # Mostrar usuarios registrados solo si eres el admin
    if username == "mtorres60036812@gmail.com":
        st.sidebar.markdown("### 👥 Usuarios registrados")

        usuarios = []
        for correo, datos in usuarios_data['usernames'].items():
            usuarios.append({"Correo": correo, "Nombre": datos['name']})
            st.sidebar.write(f"📧 {correo} - {datos['name']}")

        st.sidebar.info(f"🧾 Total registrados: {len(usuarios)}")

        # Generar archivo Excel
        df_usuarios = pd.DataFrame(usuarios)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df_usuarios.to_excel(writer, index=False, sheet_name='Usuarios')

        # Botón de descarga
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
            margin-top: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f'''
        <div style="text-align:center; margin-top:20px; margin-bottom:30px;">
            <img src="{LOGOTIPO_URL}" width="150">
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown('<div class="title">📘 Traductor ESWAJU: Español – Wampis / Awajún</div>', unsafe_allow_html=True)

    # ----------------------------
    # FUNCIONES
    # ----------------------------
    @st.cache_data
    def cargar_datos():
        df = pd.read_csv("diccionario.csv")
        df.columns = df.columns.str.strip().str.lower()
        return df

    def reproducir_audio(nombre_archivo):
        ruta_audio = os.path.join("audios", nombre_archivo)
        if os.path.exists(ruta_audio):
            with open(ruta_audio, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
        else:
            st.info("🔇 No hay audio disponible para esta palabra.")

    # ----------------------------
    # TRADUCCIÓN
    # ----------------------------
    df = cargar_datos()

    idioma = st.selectbox("🌐 Selecciona el idioma de destino:", ["Awajún", "Wampis"])
    modo = st.radio("🧭 Modo de traducción:", ["Español → Lengua originaria", "Lengua originaria → Español"])
    palabra = st.text_input("🔤 Ingresa una palabra:")

    if palabra:
        palabra_busqueda = palabra.strip().lower()

        if modo == "Español → Lengua originaria":
            idioma_key = "awajun" if idioma == "Awajún" else "wampis"
            resultado = df[df["espanol"].str.lower() == palabra_busqueda]

            if not resultado.empty:
                traduccion = resultado.iloc[0][idioma_key]
                st.markdown(f"<h3 style='color:#000000;'>🔁 Traducción: {traduccion}</h3>", unsafe_allow_html=True)
                nombre_audio = f"{traduccion.lower()}_{idioma_key}.mp3"
                reproducir_audio(nombre_audio)
            else:
                st.warning("❌ Palabra no encontrada en el diccionario.")

        elif modo == "Lengua originaria → Español":
            resultado_awajun = df[df["awajun"].str.lower() == palabra_busqueda]
            resultado_wampis = df[df["wampis"].str.lower() == palabra_busqueda]

            if not resultado_awajun.empty or not resultado_wampis.empty:
                st.markdown("<h3 style='color:#000000;'>🔁 Traducción:</h3>", unsafe_allow_html=True)

                if not resultado_awajun.empty:
                    traduccion_awa = resultado_awajun.iloc[0]["espanol"]
                    st.write(f"🗣️ Awajún → Español: {traduccion_awa}")
                    nombre_audio = f"{palabra_busqueda}_awajun.mp3"
                    reproducir_audio(nombre_audio)

                if not resultado_wampis.empty:
                    traduccion_wam = resultado_wampis.iloc[0]["espanol"]
                    st.write(f"🗣️ Wampis → Español: {traduccion_wam}")
                    nombre_audio = f"{palabra_busqueda}_wampis.mp3"
                    reproducir_audio(nombre_audio)
            else:
                st.warning("❌ Palabra no encontrada en el diccionario.")











