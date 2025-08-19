# autho_secure_login.py
import streamlit as st
import requests
import os

class Auth0Login:
    def __init__(self):
        self.domain = st.secrets["auth0"]["domain"]
        self.client_id = st.secrets["auth0"]["client_id"]
        self.client_secret = st.secrets["auth0"]["client_secret"]
        self.redirect_uri = "https://casualfacedetector-45z6692ee8yhuvm6j4inxc.streamlit.app/"

    def get_auth_url(self):
        return (
            f"https://{self.domain}/authorize?"
            f"audience=https://{self.domain}/userinfo&"
            f"response_type=code&"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}"
        )

    def login(self):
        query_params = st.query_params
        code = query_params.get("code")
        if code:
            token = self.exchange_code_for_token(code[0])
            userinfo = self.get_user_info(token)
            return userinfo
        else:
            auth_url = self.get_auth_url()
            st.markdown(f"[Login via Auth0]({auth_url})")
            return None

    def exchange_code_for_token(self, code):
        url = f"https://{self.domain}/oauth/token"
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()["access_token"]

    def get_user_info(self, token):
        url = f"https://{self.domain}/userinfo"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

# testando
if __name__ == '__main__':
    auth = Auth0Login()
    user = auth.login()