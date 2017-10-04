from asyncio import get_event_loop, gather
import json
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus
from logging import getLogger, StreamHandler, INFO

from pyfcm import FCMNotification
from tornado.web import RequestHandler, Application, HTTPError
from tornado.platform.asyncio import AsyncIOMainLoop
import lya

from BackendAPI.models import ApplicationSession, InMemoryApplicationSessionRepositoryImpl
from BackendAPI.models.exceptions import NotFoundError
from BackendAPI.models.image.builde import ImageBuilder
from BackendAPI.models.image.exceptions import EmptyFilesError
from BackendAPI.models.image.repository_impl import InMemoryImageRepository

cfg = lya.AttrDict.from_yaml('../config.yaml')

push_service = FCMNotification(api_key=cfg.firebase.server_key)

thread_pool_executor = ThreadPoolExecutor(5)

logger = getLogger('tornado')
logger.addHandler(StreamHandler())
logger.setLevel(INFO)


application_session_repository = InMemoryApplicationSessionRepositoryImpl()
image_repository = InMemoryImageRepository()


class ItemsHandler(RequestHandler):

    async def get(self, *args, **kwargs):
        self.write(json.dumps(dict(items=['item1', 'item2'])))


class ApplicationHandler(RequestHandler):

    async def post(self, *args, **kwargs):
        application_session = ApplicationSession(self.get_query_argument("token"), self.get_query_argument("item"))
        application_session_repository.add(application_session)
        self.set_status(HTTPStatus.NO_CONTENT)


class ApplicationNotificationHandler(RequestHandler):

    async def post(self, *args, **kwargs):
        applications_sessions = application_session_repository.get_by_items(self.get_query_argument("item"))

        try:
            image = ImageBuilder.from_request(self.request)
            image_repository.save(image)

            logger.info('Save {} image'.format(image.id))
        except EmptyFilesError:
            raise HTTPError(HTTPStatus.BAD_REQUEST, "Missing image")

        def go(token: str):
            logger.info("Notify {} application".format(token))

            push_service.notify_single_device(registration_id=token, message_title="New event",
                                              message_body="New event body",
                                              data_message=dict(image_id=image.id))

        await gather(*[get_event_loop().run_in_executor(thread_pool_executor, go, application_session.token)
                       for application_session in applications_sessions])

        self.set_status(HTTPStatus.NO_CONTENT)


class ImageHandler(RequestHandler):

    async def get(self, id: str, *args, **kwargs):
        try:
            image = image_repository.get(id)
        except NotFoundError as e:
            raise HTTPError(HTTPStatus.NOT_FOUND, str(e))

        self.set_header('Content-Type', image.content_type)
        self.set_header('Content-Disposition', 'attachment; filename={}'.format(image.filename))
        self.write(image.source)


if __name__ == '__main__':
    AsyncIOMainLoop().install()
    app = Application([
        ("/items", ItemsHandler),
        ("/bind", ApplicationHandler),
        ("/notify", ApplicationNotificationHandler),
        ("/image/(?P<id>[a-zA-Z0-9-_]+)", ImageHandler),
    ])

    app.listen(8000)
    get_event_loop().run_forever()

