import os

from falcon import API, Request, Response
from falcon.errors import HTTPInternalServerError
from logging import getLogger
import sentry_sdk

__all__ = ['BaseAPI']


class LogMiddleware:

    def __init__(self):
        self._logger = getLogger(self.__module__)

    def process_request(self, req: Request, *_args, **_kwargs):
        if req.params and len(req.params):
            self._logger.info(
                f"Request from {req.access_route} {req.method}:{req.path} params={str(req.params.items())}")
        else:
            self._logger.info(f"Request from {req.access_route} {req.method}:{req.path}")

    def process_response(self, req: Request, resp: Response, *_args, **_kwargs):
        self._logger.info(f"Responding to {req.access_route} {req.method}:{req.path} | {resp.status}")


class LogMiddlewareAsync:

    def __init__(self):
        self._logger = getLogger(self.__module__)

    async def process_request(self, req: Request, *_args, **_kwargs):
        if req.params and len(req.params):
            self._logger.info(
                f"Request from {req.access_route} {req.method}:{req.path} params={str(req.params.items())}")
        else:
            self._logger.info(f"Request from {req.access_route} {req.method}:{req.path}")

    async def process_response(self, req: Request, resp: Response, *_args, **_kwargs):
        self._logger.info(f"Responding to {req.access_route} {req.method}:{req.path} | {resp.status}")


class BaseAPI(API):
    def __init__(self):
        middleware = [LogMiddleware()]

        if os.getenv('ENV', 'dev') == 'prd':
            sentry_sdk.init(
                dsn="https://df9cae77f01454d726eb97a90be0909d@o4506743044505600.ingest.sentry.io/4506743046668288",
                traces_sample_rate=1.0,
                profiles_sample_rate=1.0,
            )

        super().__init__(middleware=middleware, cors_enable=True)
        self._logger = getLogger(self.__module__)
        self.add_error_handler(Exception, self.handle_error)


    def handle_error(self, req, resp, error, *_args, **_kwargs):
        self._logger.exception(f'{error!r}')
        self._compose_error_response(req, resp, HTTPInternalServerError())
