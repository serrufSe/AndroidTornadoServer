from base64 import b64encode
from typing import Dict, List

from tornado.httputil import HTTPFile, HTTPServerRequest

from BackendAPI.models.image.exceptions import EmptyFilesError
from BackendAPI.models.image.model import Image


class ImageBuilder(object):

    def __init__(self) -> None:
        super().__init__()
        self._image = Image()

    def set_http_file(self, files: Dict[str, List[HTTPFile]]) -> 'ImageBuilder':
        try:
            image = list(files.values())[0][0]
        except IndexError:
            raise EmptyFilesError()

        self._image.source = b64encode(image['body']).decode('utf-8')
        self._image.content_type = image['content_type']
        self.image.filename = image['filename']

        return self

    @property
    def image(self) -> Image:
        return self._image

    @classmethod
    def from_request(cls, request: HTTPServerRequest) -> Image:
        inst = cls()

        inst.set_http_file(request.files)

        return inst.image
