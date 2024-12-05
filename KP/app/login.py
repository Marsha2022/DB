import streamlit as st
import requests
import hashlib

import envars


def display():
    st.title("Авторизация")
    with st.form("login_form"):
        username = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type="password")
        submit_button = st.form_submit_button("Войти")
        if submit_button:
            try:
                json = {"username": username,
                        "hashed_password": hashlib.sha256(password.encode()).hexdigest()}
                response = requests.post(f"{envars.API_BASE_URL}/login", json=json)
                response.raise_for_status()
                data = response.json()
                st.session_state.login = True
                st.session_state.user_type = data["user_type"]
                st.rerun()
            except Exception:
                st.error("Неправильный логин или пароль")
                st.stop()


display()
