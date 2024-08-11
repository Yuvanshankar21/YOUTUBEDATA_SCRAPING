import mysql.connector as mysql
import streamlit as st


class SQLConnection:
    def __init__(self, host="localhost", user="root", password="root", database="YOUTUBE_DATA"):
        self.mydb = mysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        try:
            self.cursor = self.mydb.cursor()
        except mysql.Error as e:
            st.error("An error occurs", e)

    def get_data(self, table_name):
        query = "SELECT * FROM {}".format(table_name)
        self.cursor.execute(query)
        rs = self.cursor.fetchall()
        return rs

    def get_one(self, table_name, condition):
        query = "SELECT * FROM {} WHERE {}".format(table_name, condition)
        self.cursor.execute(query)
        rs = self.cursor.fetchall()
        return rs

    def insert_data(self, table_name, values):
        formatter = ', '.join(['%s'] * len(values[0]))
        query = "INSERT INTO {} VALUES({})".format(table_name, formatter)
        self.cursor.executemany(query, values)
        self.mydb.commit()

    def get_data_by_channel_id(self, channel_id, table_name, column_name):
        query = "SELECT {} FROM {} WHERE channel_id='{}'".format(column_name, table_name, channel_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def in_query(self, col_name, table_name, parameter, ids):
        query = "SELECT {} FROM {} WHERE {} in('{}')".format(col_name, table_name, parameter, ids)
        print(query)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.mydb.close()


