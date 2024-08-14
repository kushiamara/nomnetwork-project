import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    This is a demo app for CS 3200 Course Project.  

    Our app merges the visual excitement of Instagram with the detailed insights of Yelp. 
    Users get to capture and share their food experiences with their friends and followers through posts while 
    also exploring and discovering restaurants tailored to their preferences. This will be done by allowing users 
    to share their culinary adventures but also tag the restaurants they eat at with categories such as the type of 
    food, price range, ambiance, performances of live-music, outdoor seating, or one of the many other possible 
    identifiers. This tagging system will allow other users to have a more streamlined and customized search for 
    dining, especially in cities like Boston which is home to approximately 4000 restaurants. Restaurant profiles 
    on the app allow restaurant managers to create  targeted promotions and real-time engagement, creating a dynamic 
    platform for food lovers and businesses alike. This is not just a review app—it's a blend of social sharing and 
    discovery to transform how people find and enjoy their dining experiences.


    Stay tuned for more information and features to come!
    """
        )
