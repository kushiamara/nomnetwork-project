import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Diner, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Reviews from People I Follow', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Followee_Reviews.py')

if st.button('Search for Restaurants', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Search_Restaurants.py')

if st.button("Post a New Review",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Post_New_Review.py')