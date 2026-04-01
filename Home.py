import streamlit as st
from pathlib import Path
from app.services.user_service import register_user, login_user
from app.data.db import connect_database
from time import sleep

st.set_page_config(
    page_title="Home page", 
    page_icon="🔑 ",
    layout="centered"
)

st.title("🔐 Welcome to the Multi-Domain Intelligence Platform")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.user['login_username']}**.")
else:

    tab_register, tab_login = st.tabs(["Register", "Login"])

    with tab_login:
        st.subheader("Login")
        with st.form(key='login_form', clear_on_submit=True):
            login_username = st.text_input("Username")
            login_password = st.text_input(
                "Password", 
                type="password"
            )
            log_btn = st.form_submit_button('Login')
            if log_btn:
                conn = connect_database()
                res = login_user(conn, login_username, login_password)
                conn.close()
                if res[0]:
                    st.session_state.user = {}
                    st.session_state.user['login_username'] = login_username
                    st.session_state.logged_in = True
                    st.success(f"{res[1]} 🎉")
                    sleep(2)
                    st.switch_page(Path('pages') / 'Cyber Incidents Dashboard.py')
                else:
                    st.warning(res[1])
                    
    with tab_register:
        st.subheader("Register")
        with st.form(key='register_form', clear_on_submit=True):
            new_username = st.text_input("Username")
            new_password = st.text_input(
                "Password",
                type="password",
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password"
            )
            reg_btn = st.form_submit_button('Register')
            if reg_btn:
                conn = connect_database()
                if not new_username or not new_password:
                    st.warning("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    res = register_user(conn, new_username, new_password)
                    conn.close()
                    if res[0]:
                        st.success(f"{res[1]} You can now log in from the Login tab.")
                    else:
                        st.warning(res[1])
