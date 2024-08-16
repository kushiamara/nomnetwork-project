import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('NomNetwork Popular Restaurants')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}. " )
st.write(f"#### Here is a list of the 20 most popular restaurants ranked by ratings and number of reviews.")

data = requests.get('http://api:4000/da/data_analyst/rest').json()

st.dataframe(data)