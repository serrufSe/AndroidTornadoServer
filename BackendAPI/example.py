from asyncio import get_event_loop, gather
import json
from abc import ABCMeta, abstractmethod
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus
from typing import List

from pyfcm import FCMNotification
from tornado.web import RequestHandler, Application
from tornado.platform.asyncio import AsyncIOMainLoop


api_key = 'tornadoapi-a9323'
push_service = FCMNotification(api_key=api_key)
thread_pool_executor = ThreadPoolExecutor(5)


class ApplicationSession(object):

    def __init__(self, token: str, item: str) -> None:
        super().__init__()
        self.token = token
        self.item = item


class IApplicationSessionRepository(metaclass=ABCMeta):

    @abstractmethod
    def add(self, application_session: ApplicationSession):
        pass

    @abstractmethod
    def get_by_items(self, item: str) -> List[ApplicationSession]:
        pass


class InMemoryApplicationSessionRepositoryImpl(IApplicationSessionRepository):

    def __init__(self) -> None:
        super().__init__()
        self._items_hash = {}

    def add(self, application_session: ApplicationSession):
        self._items_hash[application_session.item] = application_session

    def get_by_items(self, item: str) -> List[ApplicationSession]:
        return self._items_hash[item] if item in self._items_hash else []


repository = InMemoryApplicationSessionRepositoryImpl()


class ItemsHandler(RequestHandler):

    async def get(self, *args, **kwargs):
        self.write(json.dumps(dict(items=['item1', 'item2'])))


class ApplicationHandler(RequestHandler):

    async def post(self, *args, **kwargs):
        application_session = ApplicationSession(self.get_query_argument("token"), self.get_query_argument("item"))
        repository.add(application_session)
        self.set_status(HTTPStatus.NO_CONTENT)


class ApplicationNotificationHandler(RequestHandler):

    async def post(self, *args, **kwargs):
        applications_sessions = repository.get_by_items(self.get_query_argument("item"))

        def go(token: str):
            push_service.notify_single_device(registration_id=token, message_title="New event",
                                              message_body="New event body")

        await gather(*[get_event_loop().run_in_executor(thread_pool_executor, go, application_session.token)
                       for application_session in applications_sessions])

        self.set_status(HTTPStatus.NO_CONTENT)


if __name__ == '__main__':
    AsyncIOMainLoop().install()
    app = Application([
        ("/items", ItemsHandler),
        ("/bind", ApplicationHandler),
        ("/notify", ApplicationNotificationHandler),
    ])

    app.listen(8000)
    get_event_loop().run_forever()
