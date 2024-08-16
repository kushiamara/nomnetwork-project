import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Post a New Review!')

# pull emily's userID
author = requests.get('http://api:4000/d/diner/author/emilyThompson').json()

# pull the list of restuarants in the database
data = requests.get('http://api:4000/d/diner/restaurants').json()

# Create a dictionary for dropdown options with names as keys and IDs as values
options = {"Select a restaurant": None}
options.update({restaurant['Name']: restaurant['ID'] for restaurant in data})

# Create a dropdown in Streamlit
selected_name = st.selectbox('Where did you dine?', list(options.keys()))

# Get the corresponding ID for the selected restaurant
selected_id = options[selected_name]

# input rating value
var_rating = st.slider("Rate your experience from 1 to 5", min_value=0.0, max_value=5.0, step=0.1)

# Create a multi-line text input box for user to enter their review
user_review = st.text_area(
    "Share your thoughts",  # Label for the text area
    value="",  # Default value (can be an empty string)
    height=200  # Height of the text area in pixels
)


# Create a multi-line text input box for user to enter image link
review_photo = st.text_input(
    "Enter your photo link",  # Label for the text area
)


# Construct the request payload
request_payload = {
    "rating": var_rating,
    "text": user_review,
    "authorId": author["userId"],
    "restId": selected_id,
    "photo": review_photo
}

# Create a button and handle its click event
if st.button('Post Review', type='primary', use_container_width=True):
    # Send the POST request with the request_payload as JSON data
    try:
        response = requests.post('http://api:4000/d/diner', json=request_payload)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            results = response.json()
            # st.dataframe(results)
            st.write(results["result"])
        else:
            st.error(f"Request failed with status code {response.status_code}")
    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")
  