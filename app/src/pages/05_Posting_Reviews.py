import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('NomNetwork Overview of User Behavior:')
st.write(f"## Posting Reviews")
st.write(' ')
# You can access the session state to make a more customized/personalized app experience
st.write(f"##### This is the list of the number of views and comments of each review. ")

data = requests.get('http://api:4000/da/data_analyst/behavior').json()

st.dataframe(data)

if st.button('Click here to see the reviews with the highest views and interactions.', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/08_High.py')

if st.button('Click here to see the reviews with high views but low interactions.', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/09_Low.py')