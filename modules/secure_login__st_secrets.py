# secrets_secure_login.py
from __future__ import annotations

import streamlit as st
import hashlib
import time


def hash_password(password: str) -> str:
    """Retorna o hash SHA256 da senha."""
    return hashlib.sha256(password.encode()).hexdigest()


class SecretsLogin:
    def __init__(self, session_timeout: int = 3600):
        """
        Args:
            session_timeout (int): tempo máximo da sessão em segundos (default = 1h).
        """
        self.valid_users = st.secrets["credentials"]["users"]
        self.session_timeout = session_timeout

        if "auth_user" not in st.session_state:
            st.session_state["auth_user"] = None
            st.session_state["auth_expiry"] = None

    def login_form(self):
        """Renderiza o formulário de login."""
        st.subheader("🔐 Login com credenciais")

        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar")

        if submitted:
            if self.authenticate(username, password):
                st.session_state["auth_user"] = username
                st.session_state["auth_expiry"] = time.time() + self.session_timeout
                st.success(f"✅ Bem-vindo, {username}!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    def authenticate(self, username: str, password: str) -> bool:
        """Valida usuário e senha."""
        if username not in self.valid_users:
            return False

        stored_hash = self.valid_users[username]
        return stored_hash == hash_password(password)

    def is_authenticated(self) -> bool:
        """Checa se o usuário ainda está logado e sessão válida."""
        user = st.session_state.get("auth_user", None)
        expiry = st.session_state.get("auth_expiry", None)

        if not user or not expiry:
            return False

        if time.time() > expiry:
            self.logout()
            return False

        return True

    def get_user(self) -> str | None:
        """Retorna o usuário logado, ou None se não houver."""
        return st.session_state.get("auth_user", None)

    def logout(self):
        """Finaliza a sessão do usuário."""
        st.session_state["auth_user"] = None
        st.session_state["auth_expiry"] = None
        st.success("🚪 Sessão encerrada.")
        st.rerun()

# Exemplo de uso
if __name__ == "__main__":
    auth = SecretsLogin(session_timeout=600)  # 10 min para teste rápido

    if not auth.is_authenticated():
        auth.login_form()
    else:
        st.write(f"🎉 Você está logado como **{st.session_state['auth_user']}**")
        user = auth.get_user()
        st.write(f"📂 Pasta de trabalho: training/{user}/")
        if st.button("Logout"):
            auth.logout()
