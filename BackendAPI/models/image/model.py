from BackendAPI.models.interfaces import Identifiable


class Image(Identifiable[str]):

    def __init__(self, id: str = None, source: bytes = None, content_type: str = None, filename: str = None):
        self._id = id
        self.source = source
        self.content_type = content_type
        self.filename = filename

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value