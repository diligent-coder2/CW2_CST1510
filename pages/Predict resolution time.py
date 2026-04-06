import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from app.data.db import connect_database
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
st.title("Linear Regression model")
st.caption('The model is trained on the data in the it_tickets table.')
st.caption('The model has 3 features(priority, status, and assigned_to).')

conn = connect_database()

def get_all_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    data = pd.read_sql(sql, conn, index_col='ticket_id')

    return data

data = get_all_it_tickets(conn)
conn.close()

df = (data
    .drop(columns=['description', 'created_at'])
)

priority_code = {'Low': 0, 'Medium': 1, 'High': 2, 'Critical': 3}
status_code = {'Open': 0, 'Waiting for User': 1, 'In Progress': 2, 'Resolved': 3}
assigned_code = {'IT_Support_A': 0, 'IT_Support_B': 1, 'IT_Support_C': 2}

st.subheader('Encoding the data for simple inputs')
st.write(f'priority_code: {priority_code}')
st.write(f'status_code: {status_code}')
st.write(f'assigned_code: {assigned_code}')

df_encoded = (df
  .assign(priority = df.priority.map(priority_code))
  .assign(status = df.status.map(status_code))
  .assign(assigned_to = df.assigned_to.map(assigned_code))
)

df_encoded1 = pd.get_dummies(
    df,
    columns=['priority', 'status', 'assigned_to'],
    dtype=int
)

df_encoded2 = pd.get_dummies(
    df,
    columns=['priority', 'status'],
    dtype=int
).drop(columns=['assigned_to'])

df_encoded3 = pd.get_dummies(
    df,
    columns=['priority', 'assigned_to'],
    dtype=int
).drop(columns=['status'])

df_encoded4 = pd.get_dummies(
    df,
    columns=['status', 'assigned_to'],
    dtype=int
).drop(columns=['priority'])

def features_target(df):
    y = np.array(df['resolution_time_hours'])
    x = np.array(df.drop(columns=['resolution_time_hours']))
    return x, y

with st.sidebar:
    st.header('Navigation')
    run_model = st.button('Run model')
    st.divider()
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.user = {}
        st.session_state.messages = []
        st.info("You have been logged out.")
        sleep(2)
        st.switch_page("Home.py")

if run_model:
    x, y = features_target(df_encoded)
    model = LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    model.fit(x_train, y_train)

col1, col2 = st.columns(2)
with col1:
    st.subheader('Model\'s attributes')
    try:
        st.write(f'Model\'s intercept: {model.intercept_}')
        st.write(f'Model\'s coefficients: {model.coef_}')
        st.write(f'Train data score: {model.score(x_train, y_train)}')
        st.write(f'Test data score: {model.score(x_test, y_test)}')
    except NameError:
        st.info('check Input and Prediction column')
        
with col2:
    st.subheader('Input and Prediction')
    val = st.text_input('Enter your inputs', placeholder='e.g. 0 1 2')
    val_list = val.split()
    xval = np.array([int(i) for i in val_list])

    try:
        st.write(f'Model\'s prediction: {model.predict(xval.reshape(1, 3))[0]}')
        st.caption(f'''This means that, according to the model, a ticket with 
                   {list(priority_code.keys())[list(priority_code.values()).index(0)]} prioirity,
                   {list(status_code.keys())[list(status_code.values()).index(0)]} status, and 
                    assigned to {list(assigned_code.keys())[list(assigned_code.values()).index(0)]}
                    has a resolution time of {model.predict(xval.reshape(1, 3))[0]} hours.
        '''
        )
    except NameError:
        st.info('First, input your values then click the "Run model" button')
    
