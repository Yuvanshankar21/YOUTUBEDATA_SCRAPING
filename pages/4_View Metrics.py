from services.sqlConnectionService import SQLConnection
import pandas as pd
import streamlit as st


sql_conn = SQLConnection()

view_met = sql_conn.view_metrics()

view_metrics_df = pd.DataFrame(view_met, columns=['Channel Name', 'Channel Views', 'Video Name', 'View Count'])

st.title("Channel with view count")
with st.container(height=300):
    unique_ch_vi_df = view_metrics_df.drop_duplicates(subset='Channel Name')
    st.table(unique_ch_vi_df[['Channel Name', 'Channel Views']])

st.title("Top 10 Views of video")
with st.container(height=300):
    top10 = view_metrics_df.sort_values('View Count', ascending=False).head(10).reset_index()
    st.table(top10[['Video Name', 'View Count', 'Channel Name']])

