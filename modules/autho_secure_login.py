# autho_secure_login.py
import streamlit as st
import requests


def add_login_button(auth_url):
    html_text = f"""
        <a href="{auth_url}" target="_self">
            <button style="
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            ">
                🔐 Login via Auth0
            </button>
        </a>
        """
    return st.markdown(html_text, unsafe_allow_html=True)


class Auth0Login:
    def __init__(self):
        self.domain = st.secrets["auth0"]["domain"]
        self.client_id = st.secrets["auth0"]["client_id"]
        self.client_secret = st.secrets["auth0"]["client_secret"]
        self.redirect_uri =  "https://casualfacedetector-45z6692ee8yhuvm6j4inxc.streamlit.app/" # "http://localhost:8501/" #

    def get_auth_url(self):
        # print("Entrando no metodo get_auth_url...")
        return (
            f"https://{self.domain}/authorize?"
            f"audience=https://{self.domain}/userinfo&"
            f"response_type=code&"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}&"
            f"scope=openid profile email"
        )

    def login(self):
        query_params = st.query_params
        code = query_params.get('code', None)
        # print(f"query_params.code: {query_params.get('code')}")

        if not code:
            # Step 1: No code → Show login link
            auth_url = self.get_auth_url()
            add_login_button(auth_url)
            st.stop()  # prevent the rest from running

        if code:
            # Step 2: Code exists → exchange for token
            st.info("🔄 Logging you in...")
            try:
                token = self.exchange_code_for_token(code)
                userinfo = self.get_user_info(token)
                # print(f"userinfo: {userinfo}")

                # Clear query params so we don't loop
                # st.query_params = {}  # or keep other params if needed

                return userinfo
            except requests.exceptions.HTTPError as e:
                st.error("Failed to log in. Please try again.")
                st.exception(e)
                st.stop()

    def exchange_code_for_token(self, code):
        # print("Entrando no metodo exchange_code_for_token...")

        url = f"https://{self.domain}/oauth/token"
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = requests.post(url, data=payload, headers=headers)

        # # Debug logs
        # print("Status code:", resp.status_code)
        # print("Response text:", resp.text)
        # print(f"Payload: {payload}")
        # print("Redirect URI used:", self.redirect_uri)
        # print("Authorization code:", code)

        resp.raise_for_status()
        # print(f"""  -> Retorno do metodo exchange_code_for_token: {resp.json()["access_token"]} """)
        return resp.json()["access_token"]

    def get_user_info(self, token):
        # print("Entrando no metodo get_user_info...")

        url = f"https://{self.domain}/userinfo"
        headers = {"Authorization": f"Bearer {token}"}

        # print(f"  -> url:     {url}")
        # print(f"  -> headers: {headers}")

        resp = requests.get(url, headers=headers)
        resp.raise_for_status()

        # print(f"  -> resp: {resp}")
        userinfo = resp.json()
        # print("  -> userinfo:", userinfo)
        return resp.json()

# testando
if __name__ == '__main__':
    auth = Auth0Login()
    user = auth.login()
