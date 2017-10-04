from abc import ABCMeta, abstractmethod
from typing import List

from BackendAPI.models import ApplicationSession


class IApplicationSessionRepository(metaclass=ABCMeta):

    @abstractmethod
    def add(self, application_session: ApplicationSession):
        pass

    @abstractmethod
    def get_by_items(self, item: str) -> List[ApplicationSession]:
        pass