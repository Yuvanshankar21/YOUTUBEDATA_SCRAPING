import streamlit as st;
from googleapiclient.discovery import build;
import pandas as pd;
from mongoConnection import MongoConnection 


channel_data = ""

# fetching api data method
def fetch_data(channelId):
    API_KEY="AIzaSyCuekQFfYgP8dPgShVZRyQg3havu7kN6jA"
    youtube = build("youtube","v3",developerKey=API_KEY);
    # channelId = "UC9dQjP9Vp1swi-UBA8vxu3g"
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channelId
    )
    return request.execute()


# main area for streamlit application
title = st.text_input("Enter channel ID")
if st.button('Get'):
    channel_data = fetch_data(title)
    if channel_data.get('pageInfo').get('totalResults') == 0:
        st.write("enter valid channel ID")
    else:
        st.write(channel_data)
        if st.button('Store'):
            mongo_conn = MongoConnection()
            if mongo_conn.insert_data(channel_data):
                st.success("Data stored successfully!")
            else:
                st.error("Failed to store data.")