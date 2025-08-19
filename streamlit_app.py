import os
import streamlit as st

from app_core_logic import main_logic
from modules.autho_secure_login import Auth0Login

os.environ["STREAMLIT_WATCHDOG_DISABLE"] = "true"

st.title("📸 Ferramenta de Reconhecimento Facial - Sala de Aula")

# ===============================
# SEÇÃO 0: Login seguro com AuthO
# ===============================
auth = Auth0Login()
user = auth.login()

if user:
    st.write(f"Bem-vindo, {user['name']}!")
    # resto do app aqui
    main_logic()