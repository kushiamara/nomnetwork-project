import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Search for Restaurants by Tags')

# Fetch tags data from the Flask API
try:
    response = requests.get('http://api:4000/d/diner/tags')
    response.raise_for_status()  # Raise an error for bad status codes
    tags_data = response.json()  # Parse the JSON response

    # Extract tag names from the data
    tag_names = [tag['tagName'] for tag in tags_data]

except requests.RequestException as e:
    st.error(f"Error fetching tags data: {e}")
    tag_names = []

# Display multiselect with tags as options
options = st.multiselect(
    "What restaurant features are you looking for?",
    tag_names,
    [],
)

# Convert list of dictionaries to a single dictionary for quick lookup
tag_dict = {item["tagName"]: item["tagId"] for item in tags_data}

# st.write("You selected:", options)
tag_ids = []

# Retrieve and store the tagId for each tagName in list B
for tag_name in options:
    tag_id = tag_dict.get(tag_name)
    if tag_id is not None:  # Check if the tagName is found in the dictionary
        # Append formatted string to list C
        tag_ids.append(f"{tag_id}")

# Join the list into a single comma-separated string
tagid_values = ",".join(tag_ids)

# st.write(tagid_values)
url = f'http://api:4000/d/diner/restaurants/search?tags={tagid_values}'
# st.write(url)
if st.button('Search',
             type='primary',
             use_container_width=True):
  results = requests.get(url).json()
  st.dataframe(results)
  

