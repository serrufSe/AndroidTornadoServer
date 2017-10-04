from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar


T = TypeVar('T')


class Identifiable(Generic[T], metaclass=ABCMeta):

    @property
    @abstractmethod
    def id(self) -> T:
        pass

    @id.setter
    @abstractmethod
    def id(self, value: T):
        pass