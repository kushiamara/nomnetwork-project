##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('The NomNetwork App')
st.write('\n\n')
st.write('### Hi! Which user type would you like to log in as?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Act as Tom Anderson, a Data Analyst", 
            type = 'primary', 
            use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'data_analyst'
    # we add the first name of the user (so it can be displayed on 
    # subsequent pages). 
    st.session_state['first_name'] = 'Tom'
    # finally, we ask streamlit to switch to another page, in this case, the 
    # landing page for this particular user type
    logger.info("Logging in as Data Analyst Persona")
    st.switch_page('pages/00_Data_Analyst_Home.py')

if st.button('Act as Emily Thompson, a Diner', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'diner'
    st.session_state['first_name'] = 'Emily'
    st.switch_page('pages/10_Diner_Home.py')

if st.button('Act as Marco Fontenot, a Restaurant Owner', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'restaurant'
    st.session_state['first_name'] = 'Marco'
    st.switch_page('pages/20_Restaurant_Home.py')



