import streamlit as st
import pandas as pd
import yaml
import os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

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

name, authentication_status, username = authenticator.login(
    form_name='Iniciar sesión',
    location='main'
)

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
                st.experimental_rerun()
            else:
                st.error("❌ Por favor, completa todos los campos.")

if authentication_status:
    authenticator.logout("Cerrar sesión", "sidebar")
    st.sidebar.success(f"Bienvenido, {name} 👋")

    # ----------------------------
    # TU APP PRINCIPAL
    # ----------------------------

    # Rutas desde GitHub
    FONDO_URL = "https://raw.githubusercontent.com/mesiast01/mesias-eswaju/main/fondo_eswaju.png"
    LOGOTIPO_URL = "https://raw.githubusercontent.com/mesiast01/mesias-eswaju/main/logotipo_eswaju.png"

    # Fondo con CSS
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

    # Logo centrado con espacio inferior
    st.markdown(
        f'''
        <div style="text-align:center; margin-top:20px; margin-bottom:30px;">
            <img src="{LOGOTIPO_URL}" width="150">
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Título
    st.markdown('<div class="title">📘 Traductor ESWAJU: Awajún / Wampis – Español</div>', unsafe_allow_html=True)

    # Cargar CSV
    @st.cache_data
    def cargar_datos():
        df = pd.read_csv("diccionario.csv")
        df.columns = df.columns.str.strip().str.lower()
        return df

    df = cargar_datos()

    # Interfaz
    idioma = st.selectbox("🌐 Selecciona el idioma de destino:", ["Awajún", "Wampis"])
    modo = st.radio("🧭 Modo de traducción:", ["Español → Lengua originaria", "Lengua originaria → Español"])
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
                st.markdown(f"<h3 style='color:#000000;'>🔁 Traducción: {traduccion}</h3>", unsafe_allow_html=True)
            else:
                st.warning("❌ Palabra no encontrada en el diccionario.")
        else:
            st.error(f"❌ Columnas no válidas en el CSV: {columna_origen} o {columna_destino}")








