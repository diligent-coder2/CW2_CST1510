import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.cyber_incidents import get_all_cyber_incidents
from time import sleep

st.set_page_config(
    page_title="Dashboard", 
    page_icon="📊 ",
    layout="wide"
)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to Home page"):
        st.switch_page("Home.py")
    st.stop()

st.success(f"Hello, **{st.session_state.user['login_username']}**! You are logged in.")
st.title("📊 Dashboard")

conn = connect_database()
data = get_all_cyber_incidents(conn)
conn.close()

with st.sidebar:
    st.header('Navigation')
    severity_ = st.selectbox('Severity level', data.severity.unique())
    st.divider()
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.user = {}
        st.session_state.messages = []
        st.info("You have been logged out.")
        sleep(2)
        st.switch_page("Home.py")

data['timestamp'] = pd.to_datetime(data.timestamp)
filtered_data = data[data.severity == severity_]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f'Cyber Incidents with {severity_} severity')
    st.bar_chart(filtered_data['category'].value_counts())
    st.caption(f'This bar chart shows the count of categories of cyber incidents with {severity_} severity.')
with col2:
    st.subheader('Category Trend Over Time')
    st.line_chart(filtered_data, x='timestamp', y='category')
    st.caption(f'This line graph shows the trend of categories of cyber incidents with {severity_} severity over time.')

st.subheader('Filtered Data')
filtered_data
st.caption(f'This shows a dataframe containing rows of cyber incidents with {severity_} severity.')
