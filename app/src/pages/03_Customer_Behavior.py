import logging
logger = logging.getLogger(__name__)


import streamlit as st
from modules.nav import SideBarLinks
import requests
import requests

# Call the SideBarLinks from the nav module in the modules directory
# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('NomNetwork Overview of User Behavior')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}. " )
st.write(f"#### What user behavior would you like to investigate?")

if st.button('Posting Reviews and Comments', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/05_Posting_Reviews.py')

if st.button('Following', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/06_Following.py')

