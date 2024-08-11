from services.sqlConnectionService import SQLConnection
import pandas as pd
import streamlit as st


sql_conn = SQLConnection()

channel_data = {}
playlist_data = pd.DataFrame()
video_data = pd.DataFrame()

ch_vid = pd.DataFrame()

rs = sql_conn.get_data('channel')
channel_data['channel_id'] = [row[0] for row in rs]
channel_data['channel_name'] = [row[1] for row in rs]

print(tuple(channel_data['channel_id']))

# pl_rows = sql_conn.in_query("playlist_id, channel_id", "playlist", "channel_id", channel_data['channel_id'].values)
# print("plr:", pl_rows)
# playlist_data['playlist_id'] = [row[0] for row in pl_rows]
# playlist_data['channel_id'] = [row[1] for row in pl_rows]
#
# columns = ["playlist_id", "video_name", "published_date"]
# vid_row = sql_conn.in_query(columns, "video", playlist_data['playlist_id'])
# video_data['playlist_id'] = [row[0] for row in vid_row]
# video_data['video_name'] = [row[1] for row in vid_row]
# video_data['published_date'] = [row[2] for row in vid_row]
#
# channel_df = pd.DataFrame(channel_data)
# print("channel_data:", channel_data)
# print("channel_df", channel_df)




