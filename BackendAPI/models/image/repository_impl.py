import uuid

from BackendAPI.models.exceptions import NotFoundError
from BackendAPI.models.image.model import Image
from BackendAPI.models.image.repository import IImageRepository


class InMemoryImageRepository(IImageRepository):

    def __init__(self) -> None:
        super().__init__()
        self._hash = {}

    def get(self, id: str) -> Image:
        try:
            return self._hash[id]
        except KeyError:
            raise NotFoundError("Image {} not found".format(id))

    def save(self, image: Image) -> Image:
        image.id = self._generate_id()

        self._hash[image.id] = image

        return image

    @classmethod
    def _generate_id(cls) -> str:
        return str(uuid.uuid4())