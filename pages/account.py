import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import mysql.connector
import streamlit_authenticator as stauth
from hashlib import sha256
import time
def get_connection():
    connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Hoang1337@",
    database="test"
    )
    return connection
if ('username' not in st.session_state):
    st.session_state['username'] = ''
if ('signout' not in st.session_state):
    st.session_state['signout'] = False
if ('loggedin' not in st.session_state):
    st.session_state['loggedin'] = False


def get_user(username):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    result = cursor.fetchone()
    connection.close()
    return result

def validate(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, sha256(password.encode('utf-8')).hexdigest()))
    result =  cursor.fetchone() is not None
    connection.close()
    return result

def login():
    connection = get_connection()
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
            cursor = connection.cursor()
            cursor.execute("UPDATE user set last_login = %s WHERE username = %s", (datetime.now(), username))
            connection.commit()
            st.session_state['username'] = username
            st.session_state['loggedin'] = True
            global usernm
            usernm = username
        else:
            #if they are not valid, show an error message
            st.write("The username or password you have entered is invalid")
    connection.close()
if not st.session_state['loggedin']:
    st.warning('You are not logged in')
    login()
    if st.session_state['loggedin']:
        st.write("You are logged in as {}".format(st.session_state['username']))
        st.balloons()
        st.sidebar.button('Sign out')
    else:
        # Display a popup if login fails
        st.sidebar.button('Login Failed. Please try again.')

else:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT stocklist FROM user WHERE username = %s", (st.session_state['username'],))
    result = cursor.fetchone()
    connection.close()
    if result is not None:
        st.write("Your watchlist: {}".format(result[0]))
    else:
        st.write("You have no watchlist")