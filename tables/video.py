class Video:
    def __init__(self, **kwargs):
        self.video_id = kwargs["id"]
        self.playlist_id = kwargs["pl_id"]
        self.video_name = kwargs["name"]
        self.video_desc = kwargs["desc"]
        self.published_date = kwargs["date"]
        self.view_count = kwargs["views"]
        self.like_count = kwargs["likes"]
        self.dislike_count = kwargs["dislikes"]
        self.favorite_count = kwargs["fav"]
        self.comment_count = kwargs["comments"]
        self.duration = kwargs["dur"]
        self.thumbnail = kwargs["thumb"]
        self.caption_status = kwargs["cap"]

    def to_dict(self):
        return self.__dict__
