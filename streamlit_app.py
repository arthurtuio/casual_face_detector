import os
import streamlit as st

from app_core_logic import main_logic
from modules.secure_login__autho import Auth0Login

os.environ["STREAMLIT_WATCHDOG_DISABLE"] = "true" # acho que nao to usando pra nada

st.title("📸 Ferramenta de Reconhecimento Facial - Sala de Aula")

# ===============================
# SEÇÃO 0: Login seguro com AuthO
# ===============================

# inicializa session_state
if "user" not in st.session_state:
    st.session_state.user = None

# login só acontece se ainda não tiver user
if st.session_state.user is None:
    print("### User ainda nao definido, entrando na classe Auth0Login...")
    auth = Auth0Login()
    st.session_state.user = auth.login()

# se já tem user, roda lógica principal
if st.session_state.user:
    st.write("Bem-vindo!")
    main_logic()