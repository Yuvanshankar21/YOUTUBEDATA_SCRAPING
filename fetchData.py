import streamlit as st
from googleapiclient.discovery import build
from datetime import datetime
import isodate

from services.dataService import DataService
from services.mongoConnectionService import MongoConnectionService
from services.sqlConnectionService import SQLConnection

from tables.channel import Channel
from tables.playlist import Playlist
from tables.video import Video
from tables.comment import Comments

st.set_page_config(
    page_title="Fetch Data"
)
playlist_ids = []
video_pl_pair = {}


# fetching api data method
def fetch_data(channelId):
    API_KEY = "AIzaSyCuekQFfYgP8dPgShVZRyQg3havu7kN6jA"
    youtube = build("youtube", "v3", developerKey=API_KEY)
    # channelId = "UC9dQjP9Vp1swi-UBA8vxu3g"
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics,status",
        id=channelId
    )
    return request.execute()


fetch, unstructured, structured = st.tabs(["fetch", "unstructured", "structured"])

with fetch:
    st.title("Fetch data from youtube.")
    if "channel_id" not in st.session_state:
        st.session_state["channel_id"] = ""

    if "channel_data" not in st.session_state:
        st.session_state["channel_data"] = ""

    if "store_button" not in st.session_state:
        st.session_state["store_button"] = False

    channel_id = st.text_input("Enter channel ID")
    get_button = st.button("Get")

    if get_button:
        st.write(channel_id)
        channel_data = fetch_data(channel_id)
        if channel_data.get('pageInfo').get('totalResults') == 0:
            st.write("enter valid channel ID")
        else:
            st.session_state["channel_data"] = channel_data
            st.success("Data fetched successfully")

with unstructured:
    with st.container(height=300):
        st.write(st.session_state["channel_data"])
    if st.session_state["channel_data"]:
        store_button = st.button("Store")
        if store_button:
            mongo_conn = MongoConnectionService()
            if mongo_conn.insert_data(st.session_state["channel_data"]):
                st.success("Data stored successfully!")
            else:
                st.error("Failed to store data.")

with structured:
    st.write("Structure the data and store in SQL")
    with st.container(height=300):
        st.write(st.session_state["channel_data"])
    if st.button("Store to SQL"):
        # store channel data
        channel_value = []
        channel_items = st.session_state["channel_data"].get('items')[0]
        channel_json = Channel(
            id=channel_id,
            type='',
            name=channel_items.get('snippet').get('title'),
            views=channel_items.get('statistics').get('viewCount'),
            desc=channel_items.get('snippet').get('description'),
            status=channel_items.get('status').get('privacyStatus'),
        ).to_dict()
        channel_value.append(tuple(channel_json.values()))
        sql_conn = SQLConnection()
        sql_conn.insert_data("channel", channel_value)
        sql_conn.close_connection()

        # store playlist data
        data_service = DataService()
        playlist = data_service.fetch_playlist_ids(channel_id)
        playlist_items = playlist['items']
        list_playlist_tuple = []
        for items in playlist_items:
            pl_dict = Playlist(
                id=items['id'],
                ch_id=items['snippet']['channelId'],
                name=items['snippet']['title']
            ).to_dict()

            list_playlist_tuple.append(tuple(pl_dict.values()))
            playlist_ids.append(pl_dict['playlist_id'])
        sql_conn = SQLConnection()
        sql_conn.insert_data("playlist", list_playlist_tuple)
        sql_conn.close_connection()

        # store video data
        for ids in playlist_ids:
            play_list_item = data_service.fetch_playlist_by_id(ids)['items']
            for items in play_list_item:
                vid = items.get('snippet', {}).get('resourceId', {}).get('videoId', {})
                pid = items.get('snippet', {}).get('playlistId', {})
                if vid and pid:
                    video_pl_pair[vid] = pid
        video_values = []
        for video_id in video_pl_pair.keys():
            videos = data_service.fetch_video_by_id(video_id)
            video_items = videos['items']
            for item in video_items:
                date = datetime.fromisoformat(item['snippet']['publishedAt'].replace("Z", "+00:00")).strftime(
                    "%Y-%m-%d %H:%M:%S")
                duration = int(isodate.parse_duration(item['contentDetails']['duration']).total_seconds())
                video_dict = Video(
                    id=item['id'],
                    pl_id=video_pl_pair[item['id']],
                    name=item['snippet']['title'],
                    desc=item['snippet']['description'],
                    date=date,
                    views=item['statistics']['viewCount'],
                    likes=item['statistics']['likeCount'],
                    dislikes=item['statistics'].get('dislikeCount', 0),
                    fav=item['statistics'].get('favoriteCount', 0),
                    comments=item['statistics'].get('commentCount', 0),
                    dur=duration,
                    thumb=item['snippet']['thumbnails']['default']['url'],
                    cap=item['contentDetails']['caption']
                ).to_dict()
                video_values.append(tuple(video_dict.values()))
        sql_conn = SQLConnection()
        sql_conn.insert_data("video", video_values)
        sql_conn.close_connection()

        # store comments data
        comment_values = []
        for vi_id in video_pl_pair.keys():
            comments = data_service.fetch_comments(vi_id)
            comments_item = comments['items']
            if comments_item:
                for item in comments_item:
                    comments_dict = Comments(
                        id=item['id'],
                        vid_id=item['snippet']['videoId'],
                        text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        auth=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        date=datetime.fromisoformat(item['snippet']['topLevelComment']['snippet']['publishedAt'].replace("Z", "+00:00")).strftime(
                            "%Y-%m-%d %H:%M:%S")
                    ).to_dict()
                    comment_values.append(tuple(comments_dict.values()))
        sql_conn = SQLConnection()
        sql_conn.insert_data("comment", comment_values)
        sql_conn.close_connection()
        st.write("successful")
