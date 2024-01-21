import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import mysql.connector
import streamlit_authenticator as stauth
from hashlib import sha256


connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Hoang1337@",
    database="test"
)
def signup():
    #create a form
    form = st.form(key='signup')
    #add a username field
    username = form.text_input('Username')
    #add a password field
    password = form.text_input('Password', type='password')
    cf_password = form.text_input('Confirm Password', type='password')
    #add a submit button
    submit = form.form_submit_button('Signup')
    
    #check if the user submitted the form
    if submit:
        #check if the username already exists
        if (get_user(username) == False):
            #if it doesn't exist, create the user
            cursor = connection.cursor()
            cursor.execute("INSERT INTO user (username, password,create_time) VALUES (%s, %s, %s)",(username,sha256(password.encode('utf-8')).hexdigest() , datetime.now()))
            connection.commit()
            st.success('Successfully created user: {}'.format(username))
        else:
            #if it exists, show an error message
            st.error('That username already exists')
def get_user(username):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    return cursor.fetchone() is not None
signup()