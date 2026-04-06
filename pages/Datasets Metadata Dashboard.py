import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from app.data.db import connect_database
from app.data.metadata import get_all_datasets_metadata
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
data = get_all_datasets_metadata(conn)
conn.close()

with st.sidebar:
    st.header('Navigation')
    slide = st.slider('No. of rows', 1000, 30000)
    
    st.divider()
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.user = {}
        st.session_state.messages = []
        st.info("You have been logged out.")
        sleep(2)
        st.switch_page("Home.py")

col1, col2 = st.columns(2)
with col1:
    st.subheader('Count of datasets uploaded by our technicians')
    counts = data.uploaded_by.value_counts()
    fig, ax = plt.subplots()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.bar(counts.index, counts)
    plt.xlabel('Technician', color='red', fontsize=12)
    plt.ylabel('Number of datasets', color='red', fontsize=12)
    st.pyplot(fig)
    st.caption('This bar chart shows that the data scientist uploaded datasets the most.')
with col2:
    st.subheader('Timeline of datasets addition', text_alignment='center')
    fig, ax = plt.subplots()
    fig.set_figheight(6.8)
    fig.set_figwidth(7)
    ax.plot(data.upload_date, data.name, 'o')
    
    plt.xlabel('upload date', color='orange', fontsize=12)
    plt.ylabel('Name of datasets', color='orange', fontsize=12)
    

    st.pyplot(fig)
    st.caption('This shows the order(from first to last) of how the datasets were added.')

st.subheader('Filtered Data')
filtered_data = data[data.rows >= slide]
filtered_data
