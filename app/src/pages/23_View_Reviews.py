import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

# Title for the Streamlit app
st.title('View My Reviews')

# Input fields for user input
var_restid = 1 # restaurantId for Marco's restaurant, Piccolo Forno
var_rating = st.slider("Show me reviews with ratings lower than:", min_value=0.0, max_value=5.0, step=0.1)

if st.button('View Reviews', type='primary', use_container_width=True):
    try:
        response = requests.get(f'http://api:4000/r/restaurants/reviews/{var_restid}/{var_rating}')
        response.raise_for_status()  # Raise an exception for HTTP errors

        results = response.json()

        if not results:  # Check if results are empty
            st.write('No reviews found matching your criteria.')
        else:
            st.dataframe(results)

    except requests.exceptions.RequestException:
        st.write('No reviews found matching your criteria.')