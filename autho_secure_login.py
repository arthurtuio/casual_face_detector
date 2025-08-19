import streamlit as st
import requests
from urllib.parse import urlencode

# 🔑 Configurações (do secrets.toml)
AUTH0_DOMAIN = st.secrets["auth0"]["domain"]
CLIENT_ID = st.secrets["auth0"]["client_id"]
CLIENT_SECRET = st.secrets["auth0"]["client_secret"]
REDIRECT_URI = "http://localhost:8505"  # depois trocar para seu .streamlit.app
AUDIENCE = st.secrets["auth0"]["audience"]

# URLs
AUTHORIZE_URL = f"https://{AUTH0_DOMAIN}/authorize"
TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"

def login_button():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "audience": AUDIENCE,
    }
    url = f"{AUTHORIZE_URL}?{urlencode(params)}"
    st.markdown(f"[🔑 Login com Auth0]({url})", unsafe_allow_html=True)

def get_token(auth_code):
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }
    return requests.post(TOKEN_URL, json=payload).json()

def get_user_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(USERINFO_URL, headers=headers).json()

# ------------------------
st.title("App Seguro com Auth0 🔐")

query_params = st.query_params
if "code" in query_params:
    token_data = get_token(query_params["code"][0])
    if "access_token" in token_data:
        st.session_state["user"] = get_user_info(token_data["access_token"])
        st.success(f"Bem-vindo, {st.session_state['user']['email']}")
        st.write(st.session_state["user"])
    else:
        st.error("Erro na autenticação")
elif "user" in st.session_state:
    st.success(f"Logado como {st.session_state['user']['email']}")
    if st.button("Logout"):
        st.session_state.pop("user")
else:
    login_button()
