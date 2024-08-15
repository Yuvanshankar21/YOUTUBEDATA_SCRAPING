from services.sqlConnectionService import SQLConnection
import pandas as pd
import streamlit as st

sql_conn = SQLConnection()
rs = sql_conn.eng_metrics()

eng_met = pd.DataFrame(rs, columns=['Channel Name', 'Video Name', 'Likes', 'Dislikes', 'Comment id'])
comments_series = eng_met.groupby(['Channel Name', 'Video Name'])['Comment id'].count()
comments = comments_series.reset_index()
comments.columns = ['Channel Name', 'Video Name', 'Comments Count']

unique_vid = eng_met.drop_duplicates(subset='Video Name')
top_like = eng_met.sort_values('Likes', ascending=False)[['Channel Name', 'Video Name', 'Likes']].iloc[0]
top_comments = comments.sort_values('Comments Count', ascending=False)[['Channel Name', 'Video Name', 'Comments Count']].iloc[0]

# top likes
with st.container(height=100):
    st.write("from '{}' Channel '{}' has liked by '{}' peoples, which is considered as top most likes compared to "
             "other stored channels".format(top_like['Channel Name'], top_like['Video Name'], top_like['Likes']))

#     top comments
with st.container(height=100):
    st.write("from '{}' Channel '{}' has commented by '{}' peoples, which is considered as top most comments compared to "
             "other stored channels".
             format(top_comments['Channel Name'], top_comments['Video Name'], top_comments['Comments Count']))

st.title("comments count corresponding to their video")
with st.container(height=300):
    st.table(comments[['Video Name', 'Comments Count']])

st.title("likes and dislikes corresponding to video")
with st.container(height=300):
    st.table(unique_vid[['Video Name', 'Likes', 'Dislikes']])


