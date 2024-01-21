import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import mysql.connector
import streamlit_authenticator as stauth
from hashlib import sha256
import time

# Create a connection object
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Hoang1337@",
    database="test"
)
if ('username' not in st.session_state):
    st.session_state['username'] = ''
if ('signout' not in st.session_state):
    st.session_state['signout'] = False
if ('loggedin' not in st.session_state):
    st.session_state['loggedin'] = False


def get_user(username):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    return cursor.fetchone()
def validate(username, password):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, sha256(password.encode('utf-8')).hexdigest()))
    return cursor.fetchone() is not None

def login():
    #create a form
    form = st.form(key='login')
    #add a username field
    username = form.text_input('Username')
    #add a password field
    password = form.text_input('Password', type='password')
    #add a submit button
    submit = form.form_submit_button('Login')

    #check if the user submitted the form
    if submit:
        #check if the username and password are valid
        if validate(username, password):
            #if they are valid, log the user in
            st.success('Logged in as {}'.format(username))
            st.session_state['username'] = username
            st.session_state['loggedin'] = True
            global usernm
            usernm = username
        else:
            #if they are not valid, show an error message
            st.write("The username or password you have entered is invalid")

if not st.session_state['loggedin']:
    st.warning('You are not logged in')
    login()
    if st.session_state['loggedin']:
        st.write("You are logged in as {}".format(st.session_state['username']))
        st.balloons()
        
    else:
        # Display a popup if login fails
        st.sidebar.button('Login Failed. Please try again.')
else:
    st.title('Watchlist')
    st.write('Welcome to the watchlist page')
    st.write('This page is under construction')
    st.write('Your watchlist is: ')
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT ticker FROM watchlist where username = %s", (st.session_state['username'],))
    result = cursor.fetchall()
    if result is not None:
        for i in result:
            st.write("{}".format(i[0]))
    else:
        st.write("You have no watchlist")
    st.write('Add stock to watchlist')
    cursor.execute("SELECT ticker FROM ticker")
    result = cursor.fetchall()
    ticker = []
    for i in result:
        ticker.append(i[0])
    option = st.selectbox('Select stock', ticker,placeholder='Select a stock')
    #add a ticker from selection list to watchlist with username
    if st.button('Add to watchlist'):
        cursor.execute("INSERT INTO watchlist (username, ticker) VALUES (%s, %s)",(st.session_state['username'],option))
        connection.commit()
        st.success('Successfully added {} to watchlist'.format(option))
    
    


