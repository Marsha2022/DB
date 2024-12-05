import streamlit as st
import requests
import pandas as pd

import envars


@st.fragment
def display_schedule():
    try:
        response = requests.post(f"{envars.API_BASE_URL}schedule")
        response.raise_for_status()
        data = response.json()
        df_schedule = pd.DataFrame(data)
        st.dataframe(df_schedule, use_container_width=True)
    except Exception:
        st.error("Ошибка")
        st.stop()


@st.fragment
def display_team_data(src_df):
    df = src_df.copy()
    team_name = st.selectbox("Выберите название команды", options=df["team_name"].to_list())
    df = df[df["team_name"] == team_name].reset_index(drop=True)
    df.index += 1
    st.dataframe(df, use_container_width=True)


def display():
    st.title("Данные турниров")
    st.header("Расписание матчей")
    display_schedule()

    st.header("Состав команд")
    try:
        response = requests.post(f"{envars.API_BASE_URL}teams")
        response.raise_for_status()
        data = response.json()
        df_teams = pd.DataFrame(data)
    except Exception:
        st.error("Ошибка")
        st.stop()
    display_team_data(df_teams)


display()
