# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon='🏠')

def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

#### ------------------------ Examples for Role of Data Analyst  ------------------------
def DataAnalystHomeNav():
    st.sidebar.page_link("pages/00_Data_Analyst_Home.py", label="Data Analyst Home", icon='👤')

def PopularRest():
    st.sidebar.page_link("pages/01_Popular_Rest.py", label="Popular Restaurants", icon='🥡')

def PopularTags():
    st.sidebar.page_link("pages/02_Popular_Tags.py", label="Popular Tags", icon='🔗')

def CustomerBehavior():
    st.sidebar.page_link("pages/03_Customer_Behavior.py", label="Customer Behavior", icon='📊')

def Demographics():
    st.sidebar.page_link("pages/04_Demographics.py", label="Diner Demographics", icon='👨‍👩‍👧‍👦')

## ------------------------ Examples for Role of Diner ------------------------
def DinerHomeNav():
    st.sidebar.page_link("pages/10_Diner_Home.py", label="Diner Home", icon='👤')

def FolloweeReviews():
    st.sidebar.page_link("pages/12_Followee_Reviews.py", label="See My Feed", icon='✨')

def SearchRest():
    st.sidebar.page_link("pages/11_Search_Restaurants.py", label="Search Restaurants", icon='🔍')

def NewReviews():
    st.sidebar.page_link("pages/13_Post_New_Review.py", label="Post New Review", icon='✍️')

#### ------------------------ System Admin Role ------------------------
def RestaurantHome():
    st.sidebar.page_link("pages/20_Restaurant_Home.py", label="Restaurant Home", icon='👤')

def EditMenu():
    st.sidebar.page_link("pages/21_View_Menu.py", label="Edit My Menu", icon='🍽️')

def EditTags():
    st.sidebar.page_link("pages/22_View_Tags.py", label="Edit My Tags", icon='🔗')

def ViewReviews():
    st.sidebar.page_link("pages/23_View_Reviews.py", label="Read Reviews", icon='⭐')

def EditPromo():
    st.sidebar.page_link("pages/24_View_Promotions.py", label="Edit Promotions", icon='💵')




# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in. 
    """    

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width = 250)

    # If there is no logged in user, redirect to the Home (Landing) page
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page('Home.py')
        
    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state['role'] == 'data_analyst':
            DataAnalystHomeNav()
            PopularRest()
            PopularTags()
            CustomerBehavior()
            Demographics()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state['role'] == 'diner':
            DinerHomeNav()
            FolloweeReviews() 
            SearchRest()
            NewReviews()
        
        # If the user is an administrator, give them access to the administrator pages
        if st.session_state['role'] == 'restaurant':
            RestaurantHome()
            EditMenu()
            EditTags()
            ViewReviews()
            EditPromo()
            
    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state['role']
            del st.session_state['authenticated']
            st.switch_page('Home.py')

