from services.sqlConnectionService import SQLConnection
import pandas as pd
import streamlit as st
import plotly.express as px

ch_vi_df = pd.DataFrame()
sql_conn = SQLConnection()

rs = sql_conn.vc_info()
ch_vi_df = pd.DataFrame(rs, columns=['Channel Name', 'Video Name', 'Published Date'])

vid_count_series = ch_vi_df.groupby('Channel Name')['Video Name'].count()
vid_count = vid_count_series.reset_index()
vid_count.columns = ['Channel Name', 'Video Count']

ch_2022 = ch_vi_df[ch_vi_df['Published Date'].dt.year == 2022]
ch_vi_df = ch_vi_df.reset_index()

st.title("Videos corresponding to Channel name")
with st.container(height=300):
    st.table(ch_vi_df[['Channel Name', 'Video Name']])

st.title("Video count corresponding to channel")
with st.container(height=300):
    st.table(vid_count)

st.title("Channel published video in 2022")
with st.container(height=300):
    for name in ch_2022['Channel Name'].unique():
        st.write(name)
