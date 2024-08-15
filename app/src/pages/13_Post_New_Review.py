import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Post a New Review!')

author = requests.get('http://api:4000/d/diner/author/emilyThompson').json()

data = requests.get('http://api:4000/d/diner/restaurants').json()
# Create a dictionary for dropdown options with names as keys and IDs as values
options = {"Select a restaurant": None}
options.update({restaurant['Name']: restaurant['ID'] for restaurant in data})

# Create a dropdown in Streamlit
selected_name = st.selectbox('Where did you dine?:', list(options.keys()))

# Get the corresponding ID for the selected restaurant
selected_id = options[selected_name]

# create a 2 column layout
# col1, col2 = st.columns(2)

# add one number input for variable 1 into column 1
# with col1:
var_rating = st.number_input('Rating:',
                           step=0.1)

# add another number input for variable 2 into column 2
# with col2:
  
# Create a multi-line text input box
user_review = st.text_area(
    "Enter your review here:",  # Label for the text area
    value="",  # Default value (can be an empty string)
    height=200  # Height of the text area in pixels
)

# logger.info(f'var_01 = {var_01}')
# logger.info(f'var_02 = {var_02}')

# add a button to use the values entered into the number field to send to the 
# prediction function via the REST API
# Construct the request payload
request_payload = {
    "rating": var_rating,
    "text": user_review,
    "authorId": author["userId"],
    "restId": selected_id
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
  