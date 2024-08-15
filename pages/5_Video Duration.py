from services.sqlConnectionService import SQLConnection
import pandas as pd
import streamlit as st


sql_conn = SQLConnection()
video_duration = sql_conn.duration_info()
duration_df = pd.DataFrame(video_duration, columns=['Channel Name', 'Video Name', 'Duration'])
unique_vid = duration_df.drop_duplicates(subset='Video Name')
group_avg = unique_vid.groupby(['Channel Name'])['Duration'].mean()
avg_duration = group_avg.reset_index()
avg_duration.columns = ['Channel Name', 'Average']
st.table(avg_duration[['Channel Name', 'Average']])
