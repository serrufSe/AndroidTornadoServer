class ApplicationSession(object):

    def __init__(self, token: str, item: str) -> None:
        super().__init__()
        self.token = token
        self.item = item