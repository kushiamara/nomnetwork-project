import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Edit My Promotions')

# View my Promotions
st.header('View All of My Promotions')

var_restid = 1 # restaurantId for Marco's restaurant, Piccolo Forno

if st.button('View Promotions', type = 'primary', use_container_width=True):
  results = requests.get(f'http://api:4000/r/restaurants/promotions/{var_restid}').json()
  st.dataframe(results)


# Add New Promotion
st.header('Add New Promotion')

with st.form(key='add_menu_item_form'):
    name = st.text_input('Promo Name')
    description = st.text_input('Promo Description')
    active = st.checkbox("Mark as Active?", value=False)
    
    # Submit button for the form
    submit_button = st.form_submit_button(label='Add Promo')

    if submit_button:
        if not name or not description:
            st.error("Please fill out all required fields.")
        else:
            try:
                # Prepare data for the API request
                payload = {
                    'name': name,
                    'description': description,
                    'restId' : var_restid,
                    'active' : active
                }
                
                # Make POST request to add the new menu item
                response = requests.post('http://api:4000/r/restaurants/promotions', json=payload)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                
                result = response.json()
                st.success(result.get('result', 'Promotion added successfully!'))
            except requests.exceptions.RequestException as e:
                st.error("A promotion with this name already exists. Consider changing the name.")


# Updating Existing Promotion
st.header('Update Existing Promotion')

# Fetch promotions for updating
try:
    response = requests.get(f'http://api:4000/r/restaurants/promotions/{var_restid}')
    response.raise_for_status()  # Raise an HTTPError for bad responses
    promos = response.json()
    
    # Extract promotion names for selection
    promo_names = [promo['name'] for promo in promos]
    
    # Form to select and update promotions
    with st.form(key='update_promo_form'):
        selected_item = st.selectbox('Select Promotion to Update', ['Select a promo to update'] + promo_names)
        new_desc = st.text_input('New Description', placeholder='Enter description')
        new_active = st.radio("Set Promotion Active Status", ["Active", "Inactive"])
        # Convert radio button selection to integer
        active_status = 1 if new_active == "Active" else 0
        
        # Submit button for the form
        update_button = st.form_submit_button(label='Update Menu Item')

        if update_button:
            if selected_item == 'Select a promo to update':
                st.error("Please select an item to update.")
            else:
                try:
                    # Prepare data for the API request
                    payload = {
                        'name': selected_item,
                        'description': new_desc,
                        'active': active_status,
                        'restId': var_restid
                    }
                    # Make PUT request to update the promotion
                    update_url = f'http://api:4000/r/restaurants/promotions/{var_restid}/{selected_item}'
                    response = requests.put(update_url, json=payload)
                    response.raise_for_status()  # Raise an HTTPError for bad responses
                    
                    st.success('Promotion updated successfully!')
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
except requests.exceptions.RequestException as e:
    st.error(f"An error occurred while fetching promotions: {e}")