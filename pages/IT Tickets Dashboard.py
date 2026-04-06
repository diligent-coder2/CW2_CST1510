import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from app.data.db import connect_database
from app.data.it_tickets import get_all_it_tickets
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
data = get_all_it_tickets(conn)
conn.close()

with st.sidebar:
    st.header('Navigation')
    priority_ = st.selectbox('Severity level', data.priority.unique())
    status_ = st.selectbox('Status', data.status.unique())
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
    st.subheader("Tickets by Priority and Status", text_alignment='center')
    fig, ax = plt.subplots()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    resolved = data.query("status == 'Resolved'")
    sum_sts = resolved.groupby(['priority']).priority.count()
    
    open_ = data[data.status == 'Open']
    sum_sto = open_.groupby(['priority']).priority.count()

    ip_ = data[data.status == 'In Progress']
    sum_sti = ip_.groupby(['priority']).priority.count()

    wait_user = data[data.status == 'Waiting for User']
    sum_stw = wait_user.groupby(['priority']).priority.count()

    ax.bar(sum_sts.index, sum_sts, label='Resolved')
    ax.bar(sum_sto.index, sum_sto, label='Open', bottom=sum_sts)
    ax.bar(sum_sti.index, sum_sti, label='In Progress', bottom=sum_sts + sum_sto)
    ax.bar(sum_stw.index, sum_stw, label='Waiting for User', bottom=sum_sts + sum_sto + sum_sti)
    plt.legend()
    plt.xlabel('Priority', color='red', fontsize=12)
    plt.ylabel('Number of tickets', color='red', fontsize=12)
    
    st.pyplot(fig)
    st.caption('This bar chart shows that most tickets were of "Medium" priority and most tickets were resolved.')

with col2:
    st.subheader('Proportion of it tickets assigned to our support team')
    
    import plotly.express as px
    support_series = data.assigned_to.value_counts()
    st.plotly_chart(px.pie(names=support_series.index, values=support_series))
    st.caption('This pie chart shows that most tickets were assigned to IT Support A.')

filtered_data = data[(data.priority == priority_) & (data.status == status_)]

st.subheader('Filtered Data')
filtered_data
