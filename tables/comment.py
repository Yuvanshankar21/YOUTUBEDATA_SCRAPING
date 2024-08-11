class Comments:
    def __init__(self, **kwargs):
        self.comment_id = kwargs["id"]
        self.video_id = kwargs["vid_id"]
        self.comment_text = kwargs["text"]
        self.comment_author = kwargs["auth"]
        self.comment_published_date = kwargs["date"]

    def to_dict(self):
        return self.__dict__
