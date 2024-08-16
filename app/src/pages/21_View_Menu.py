import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import time

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("Edit My Restaurant's Menu")

# View Menu Items
st.header('View Menu Items')

var_restid = 1 # restaurantId for Marco's restaurant, Piccolo Forno

if st.button('View Menu Items', type = 'primary', use_container_width=True):
  results = requests.get(f'http://api:4000/r/restaurants/menuitems/{var_restid}').json()
  st.dataframe(results)


# Add New Menu Item
st.header('Add New Menu Item')

with st.form(key='add_menu_item_form'):
    item_name = st.text_input('Item Name')
    price = st.number_input('Price', min_value=0.00, format="%.2f")
    calories = st.number_input('Calories', min_value=0)
    photo_url = st.text_input('Photo URL')
    
    # Submit button for the form
    submit_button = st.form_submit_button(label='Add Menu Item')

    if submit_button:
        if not item_name or not price or not calories:
            st.error("Please fill out all required fields.")
        else:
            try:
                # Prepare data for the API request
                payload = {
                    'itemName': item_name,
                    'restId': var_restid,
                    'price': price,
                    'calories': calories,
                    'photo': photo_url
                }
                
                # Make POST request to add the new menu item
                response = requests.post('http://api:4000/r/restaurants/menuitems', json=payload)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                
                result = response.json()
                st.success(result.get('result', 'Menu item added successfully!'))
            except requests.exceptions.RequestException as e:
                st.error("An item with this name already exists. Consider choosing a new name.")


# Updating Existing Menu Item
st.header('Update Existing Menu Item')

# Fetch menu items for updating
try:
    response = requests.get(f'http://api:4000/r/restaurants/menuitems/{var_restid}')
    response.raise_for_status()  # Raise an HTTPError for bad responses
    menu_items = response.json()
    
    # Extract item names for selection
    item_names = [item['itemName'] for item in menu_items]
    
    # Form to select and update menu item
    with st.form(key='update_menu_item_form'):
        selected_item = st.selectbox('Select Item to Update', ['Select an item to update'] + item_names)
        new_price = st.number_input('New Price', min_value=0.00, format="%.2f", value=0.00)
        new_calories = st.number_input('New Calories', min_value=0, value=0)
        new_photo = st.text_input('New Photo URL', placeholder='Enter new photo URL')
        
        # Submit button for the form
        update_button = st.form_submit_button(label='Update Menu Item')

        if update_button:
            if selected_item == 'Select an item to update':
                st.error("Please select an item to update.")
            else:
                try:
                    # Prepare data for the API request
                    payload = {
                        'itemName': selected_item,
                        'price': new_price,
                        'calories': new_calories,
                        'photo': new_photo
                    }
                    
                    # Make PUT request to update the menu item
                    update_url = f'http://api:4000/r/restaurants/menuitem/{var_restid}/{selected_item}'
                    response = requests.put(update_url, json=payload)
                    response.raise_for_status()  # Raise an HTTPError for bad responses
                    
                    st.success('Menu item updated successfully!')
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
except requests.exceptions.RequestException as e:
    st.error(f"An error occurred while fetching menu items: {e}")

# Delete an Existing Menu Item
st.header('Delete a Menu Item')

try:
    response = requests.get(f'http://api:4000/r/restaurants/menuitems/{var_restid}')
    response.raise_for_status()
    menu_items = response.json()
    item_names = [item['itemName'] for item in menu_items]

    if item_names:
        selected_item = st.selectbox('Select Item to Delete', ['Select an item to delete'] + item_names)

        delete_button = st.button('Delete Menu Item', key='delete_menu_item')

        if delete_button:
            if selected_item == 'Select an item to delete':
                st.error("Please select an item to delete.")
            else:
                try:
                    delete_url = f'http://api:4000/r/restaurants/menuitem/{var_restid}/{selected_item}'
                    response = requests.delete(delete_url)
                    response.raise_for_status()
                    st.success('Menu item deleted successfully!')
                    time.sleep(1)
                    st.switch_page('pages/21_View_Menu.py')
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.warning("No menu items available to delete.")
except requests.exceptions.RequestException as e:
    st.error(f"An error occurred while fetching menu items: {e}")
