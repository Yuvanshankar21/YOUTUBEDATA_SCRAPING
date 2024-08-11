from googleapiclient.discovery import build


class DataService:
    def __init__(self):
        API_KEY = "AIzaSyCuekQFfYgP8dPgShVZRyQg3havu7kN6jA"
        self.youtube = build("youtube", "v3", developerKey=API_KEY)

    def fetch_channel_data(self, channelId):
        request = self.youtube.channels().list(
            part="snippet, statistics, status",
            id=channelId
        )
        return request.execute()

    def fetch_playlist_ids(self, channelId):
        request = self.youtube.playlists().list(
            part="id, snippet",
            channelId=channelId
        )
        return request.execute()

    def fetch_playlist_by_id(self, playlistId):
        request = self.youtube.playlistItems().list(
            part="snippet, status",
            playlistId=playlistId
        )
        return request.execute()

    def fetch_video_by_id(self, videoId):
        request = self.youtube.videos().list(
            part="snippet, statistics, contentDetails",
            id=videoId
        )
        return request.execute()

    def fetch_comments(self, videoId):
        request = self.youtube.commentThreads().list(
            part="snippet, id",
            videoId=videoId
        )
        return request.execute()
