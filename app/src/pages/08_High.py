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
st.write(f"#### Here is a list of 15 reviews with the highest views and interactions.")

data = requests.get('http://api:4000/da/data_analyst/behavior/high').json()

st.dataframe(data)