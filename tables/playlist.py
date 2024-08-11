class Playlist:
    def __init__(self, **kwargs):
        self.playlist_id = kwargs["id"]
        self.channel_id = kwargs["ch_id"]
        self.playlist_name = kwargs["name"]

    def to_dict(self):
        return self.__dict__
