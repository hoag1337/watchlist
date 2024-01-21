import pandas as pd
import numpy as np
import datetime
import streamlit as st
import mysql.connector
import streamlit_authenticator as stauth
import streamlit as st

# Create a connection object

connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Hoang1337@",
    database="test"
)
#button to run login.py
if st.button('Login'):
    exec(open('login.py').read())

#button to run signup.py
if st.button('Signup'):
    exec(open('signup.py').read())

st.title('mainpage')
st.write('Welcome to the mainpage')
