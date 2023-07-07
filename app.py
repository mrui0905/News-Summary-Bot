import streamlit as st
import json

st.title('Daily News Summary')


email = st.text_input('Enter Subscription Email: ')

if st.button('Submit'):
    with open('email_destinations.json', 'r+') as f:
        emails = json.load(f)

        emails["emails"].append(email)

        f.seek(0)

        json.dump(emails, f, indent = 4)
    f.close()
    st.success('Email submitted successfully!')