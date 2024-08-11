import pymongo
import streamlit as st


class MongoConnectionService:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="youtube", collection_name="youtube_data"):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data):
        try:
            self.collection.insert_one(data)
            return True
        except GeneratorExit as e:
            st.error("An error occurred:", e)
            return False

    def get_data(self):
        try:
            doc = self.collection.find()
            return doc
        except GeneratorExit as e:
            st.error("An error occurred:", e)
            return ""
