import streamlit as st
import json
import create_newsletter

# Ensures summary can be displayed
st.markdown("""
    <style>
        .container {
            width: 100%;
            max-width: 1500px;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title('Daily News Summary')

# Add subscription
st.subheader('Add email to daily subscription:')
email = st.text_input('Enter Subscription Email: ')
a = st.button('Submit', key = 1)
if a:
    with open('email_destinations.json', 'r+') as f:
        emails = json.load(f)

        emails["emails"].append(email)

        f.seek(0)

        json.dump(emails, f, indent = 4)
    f.close()
    st.success('Email submitted successfully!')

# Options of news summaries to choose from
st.subheader('Display news summary:')
topics = {'World' : 'world', 
            'Business' : 'business',
            'Markets' : 'markets',
            'Sustainabiltiy' : 'sustainability',
            'Legal' : 'legal',
            'Technology' : 'technology',
            'Investigations' : 'investigations',
            'United States' : 'world/us'}

# Generate news summary, display on app
option = st.selectbox('Select a news category to generate news summary: ', sorted(topics.keys()))
b = st.button('Submit', key = 2)
if b:
    st.success('Generating text')
    summary = create_newsletter.create_newsletter(topics[option])
    print(summary)

    st.write(summary)