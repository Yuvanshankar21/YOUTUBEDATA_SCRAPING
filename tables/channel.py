class Channel:
    def __init__(self, **kwargs):
        self.channel_id = kwargs["id"]
        self.channel_name = kwargs["name"]
        self.channel_type = kwargs["type"]
        self.channel_views = int(kwargs["views"])
        self.channel_desc = kwargs["desc"]
        self.channel_status = kwargs["status"]

    def to_dict(self):
        return self.__dict__
