import streamlit as st
import requests
import pandas as pd
import datetime
import hashlib

import envars


@st.fragment
def add_user():
    login = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")
    email = st.text_input("Почта")
    user_type = st.selectbox("Тип пользователя", options=["administrator", "participant", "organizer"])
    if st.button("Добавить") and all([login, password, email, user_type]):
        try:
            today = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            json = {"username": login,
                    "hashed_password": hashlib.sha256(password.encode()).hexdigest(),
                    "email": email,
                    "user_type": user_type,
                    "created_date": str(today)}
            response = requests.post(f"{envars.API_BASE_URL}/users/add", json=json)
            response.raise_for_status()
            st.success("Пользователь успешно добавлен")
        except Exception:
            st.error("Ошибка добавления пользователя")


@st.fragment
def delete_user(src_df):
    df = src_df.copy()
    login_list = df["username"].to_list()
    user2delete = st.selectbox(label="Выберите логин пользователя, которого хотите удалить",
                               options=login_list,
                               placeholder="Выберите из списка",
                               index=None)
    if st.button("Удалить", type="primary") and user2delete:
        try:
            json = {"username": user2delete}
            response = requests.post(f"{envars.API_BASE_URL}/users/delete", json=json)
            response.raise_for_status()
            st.success("Пользователь успешно удален")
        except Exception:
            st.error("Ошибка удаления пользователя")


def display():
    st.title("Панель администратора")
    try:
        response = requests.post(f"{envars.API_BASE_URL}/users/")
        response.raise_for_status()
        data = response.json()
        df_users = pd.DataFrame(data)
        df_users["created_date"] = pd.to_datetime(df_users["created_date"]).dt.date
    except Exception:
        st.error("Ошибка")
        st.stop()

    st.header("Все пользователи")
    st.dataframe(df_users, use_container_width=True)

    st.subheader("Добавить пользователя")
    add_user()

    st.subheader("Удалить пользователя")
    delete_user(df_users)


display()
