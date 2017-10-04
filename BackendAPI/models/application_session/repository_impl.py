from collections import defaultdict
from typing import List

from BackendAPI.models.application_session.model import ApplicationSession
from BackendAPI.models.application_session.repository import IApplicationSessionRepository


class InMemoryApplicationSessionRepositoryImpl(IApplicationSessionRepository):

    def __init__(self) -> None:
        super().__init__()
        self._items_hash = defaultdict(list)

    def add(self, application_session: ApplicationSession):
        self._items_hash[application_session.item].append(application_session)

    def get_by_items(self, item: str) -> List[ApplicationSession]:
        return self._items_hash[item] if item in self._items_hash else []