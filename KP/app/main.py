import streamlit as st

import logout


def main():
    if "login" not in st.session_state:
        st.session_state.login = False

    is_logged_in = st.session_state.login
    if is_logged_in:
        user_type = st.session_state.user_type
        pages = [st.Page("tournament.py", title="Данные турниров")]
        if user_type == "administrator":
            pages.append(st.Page("admin.py", title="Панель администратора"))
    else:
        pages = [st.Page("login.py", title="Авторизация")]
    display_pages = st.navigation(pages)
    if is_logged_in and st.sidebar.button("Выйти", use_container_width=True):
        logout.display()
    display_pages.run()


if __name__ == "__main__":
    main()
