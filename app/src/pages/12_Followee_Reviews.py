import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# Viewing Posts from People I Follow")

# """
# Simply retrieving data from a REST api running in a separate Docker Container.

# If the container isn't running, this will be very unhappy.  But the Streamlit app 
# should not totally die. 
# """
data = {} 
try:
  data = requests.get('http://api:4000/d/diner/emilyThompson').json()
 
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "test"}, "z": {"b": "456", "c": "goodbye"}}

#data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

# st.dataframe(data)

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Function to convert URLs to image HTML
def url_to_image_html(url):
    if pd.isna(url) or url is None:
        return ""
    return f'<img src="{url}" width="100" />'

# Apply the function to the 'photo' column
df['photo'] = df['photo'].apply(url_to_image_html)

# Display the DataFrame in Streamlit\
st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
