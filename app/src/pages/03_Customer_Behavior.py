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
st.write(f"#### Here is data for comment and view count of every review posted on the app.")

data = requests.get('http://api:4000/da/data_analyst/behavior').json()

st.dataframe(data)
