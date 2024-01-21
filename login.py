import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import mysql.connector
import streamlit_authenticator as stauth
from hashlib import sha256
from streamlit import popups

# Create a connection object
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Hoang1337@",
    database="test"
)
def get_user(username):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    return cursor.fetchone()
def validate(username, password):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, sha256(password.encode('utf-8')).hexdigest()))
    return cursor.fetchone() is not None

#login form
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
            cursor = connection.cursor()
            cursor.execute("UPDATE user set last_login = %s WHERE username = %s", (datetime.now(), username))
            connection.commit()
        else:
            #if they are not valid, show an error message
            popups("The username or password you have entered is invalid")
            #if they are not valid, show an error message
            st.error('The username or password you have entered is invalid')
login()
    
