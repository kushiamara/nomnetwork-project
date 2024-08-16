import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Data Analyst, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Determine what restaurants are currently the most popular.', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Popular_Rest.py')

if st.button('Determine what tags are currently the most popular.', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Popular_Tags.py')


if st.button('Retrieve data on user behavior.', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_Customer_Behavior.py')

if st.button('Analyze customer demographics.', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/04_Demographics.py')