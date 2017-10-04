from abc import ABCMeta, abstractmethod

from BackendAPI.models.image.model import Image


class IImageRepository(metaclass=ABCMeta):

    @abstractmethod
    def save(self, image: Image) -> Image:
        pass

    @abstractmethod
    def get(self, id: str) -> Image:
        pass