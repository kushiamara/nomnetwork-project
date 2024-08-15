import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Restaurant Manager Home Page')

if st.button('Edit My Menu', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_View_Menu.py')

if st.button('Edit My Tags', 
            type='primary',
            use_container_width=True):
    st.switch_page('pages/22_View_Tags.py')

if st.button('View Reviews of My Restaurant', 
            type='primary',
            use_container_width=True):
    st.switch_page('pages/23_View_Reviews.py')

if st.button('Edit My Promotions', 
            type='primary',
            use_container_width=True):
    st.switch_page('pages/24_View_Promotions.py')