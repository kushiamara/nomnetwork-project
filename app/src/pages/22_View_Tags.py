import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("Edit My Restaurant's Tags")

# View Current Tags
st.header('View Associated Tags')

var_restid = 1 # restaurantId for Marco's restaurant, Piccolo Forno

if st.button('View Tags', type = 'primary', use_container_width=True):
  results = requests.get(f'http://api:4000/r/restaurants/tags/{var_restid}').json()
  st.dataframe(results)


# Add New Tags
st.header('Associate a New Tag')

# Fetch available tags for selection
try:
    response = requests.get('http://api:4000/r/restaurants/gettags')
    response.raise_for_status()  # Raise an HTTPError for bad responses
    all_tags = response.json()
    
    # Extract tag IDs and names for selection
    tag_options = {tag['tagName']: tag['tagId'] for tag in all_tags}
    tag_names = list(tag_options.keys())
except requests.exceptions.RequestException as e:
    st.error(f"An error occurred while fetching available tags: {e}")
    tag_names = []

with st.form(key='add_tag_form'):
    selected_tag = st.selectbox('Select a Tag to Add', ['Select a tag'] + tag_names)
    
    # Submit button for the form
    submit_button = st.form_submit_button(label='Add Tag')

    if submit_button:
        if selected_tag == 'Select a tag':
            st.error("Please select a tag to add.")
        else:
            try:
                # Prepare data for the API request
                payload = {
                    'tagId': tag_options[selected_tag],
                    'restId': var_restid
                }
                
                # Make POST request to add the tag
                response = requests.post('http://api:4000/r/restaurants/tags', json=payload)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                
                result = response.json()
                st.success(result.get('result', 'Tag added successfully!'))
            except requests.exceptions.RequestException as e:
                st.error("This tag is already associated with your restaurant.")


# Delete an Existing Tag
st.header('Delete a Tag')

# Fetch current tags for deletion
try:
    response = requests.get(f'http://api:4000/r/restaurants/tags/{var_restid}')
    response.raise_for_status()
    tags = response.json()
    tag_names = [tag['tagName'] for tag in tags]
    
    # Select a tag currently associated with the restaurant to delete
    selected_tag_to_delete = st.selectbox('Select a Tag to Delete', ['Choose an option'] + tag_names)

    if selected_tag_to_delete != 'Choose an option':
        try:
            # Find the tagId of the selected tag in the Tags table
            response = requests.get(f'http://api:4000/r/restaurants/findtag/{selected_tag_to_delete}')
            response.raise_for_status()
            found_tagId = response.json()
            
            # Check if the response contains a valid tagId
            if found_tagId and isinstance(found_tagId, list) and len(found_tagId) > 0:
                tag_id = found_tagId[0].get('tagId')
                
                if tag_id is not None:
                    tag_id = int(tag_id)  # Ensure tag_id is an integer
                    
                    # Perform the DELETE request
                    delete_url = f'http://api:4000/r/restaurants/tags/{var_restid}/{tag_id}'
                    delete_button = st.button('Delete Tag', type='primary', use_container_width=True)

                    if delete_button:
                        try:
                            response = requests.delete(delete_url)
                            response.raise_for_status()
                            st.success('Tag deleted successfully!')
                        except requests.exceptions.RequestException as e:
                            st.error(f"An error occurred while deleting the tag: {e}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while fetching tagId: {e}")
    else:
        st.info("Please select a tag to delete.")

except requests.exceptions.RequestException as e:
    st.error(f"An error occurred while fetching tags: {e}")
