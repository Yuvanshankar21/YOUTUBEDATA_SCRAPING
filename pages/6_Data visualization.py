from services.sqlConnectionService import SQLConnection
import pandas as pd
import streamlit as st
import plotly.express as px

sql_conn = SQLConnection()
rs = sql_conn.views_by_year()
views_df = pd.DataFrame(rs, columns=['Channel Name', 'video_name', 'Published Date', 'Views'])

views_df['Published Date'] = pd.to_datetime(views_df['Published Date']).dt.year

group = views_df.groupby(['Channel Name', 'Published Date'])['Views'].sum().reset_index()

print(group)
fig = px.line(
    group,
    x='Published Date',
    y='Views',
    color='Channel Name',
    title='Total Views by Published Year for Each Channel',
    labels={'Views': 'Number of Views', 'Published Year': 'Year'},
)
st.plotly_chart(fig)
