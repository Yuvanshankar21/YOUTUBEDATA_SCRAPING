import pymongo 
import streamlit as st


class MongoConnection:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="youtube", collection_name="youtube_data"):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data):
        try:
            self.collection.insert_one(data)
            return True
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return False