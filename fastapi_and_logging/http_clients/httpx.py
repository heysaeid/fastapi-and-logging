import typing
from abc import ABC, abstractmethod

import httpx

from fastapi_and_logging.enums import LogPathEnum, LogTypeEnum
from fastapi_and_logging.logging import get_apicall_logger


class HTTPXBaseClient(ABC):
    _request_hook: typing.Callable = None
    _response_hook: typing.Callable = None
    _request_max_len: int = None
    _response_max_len: int = None
    _log_path: str = LogPathEnum.APICALL
    _log_type: LogTypeEnum = LogTypeEnum.FILE

    def __init__(
        self,
        request_id: typing.Any = None,
        request_max_len: int = _request_max_len,
        response_max_len: int = _response_max_len,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.request_id = request_id
        self.request_max_len = request_max_len
        self.response_max_len = response_max_len
        self.event_hooks["request"].append(self.request_hook)
        self.event_hooks["response"].append(self.response_hook)

    @abstractmethod
    def request_hook(self, request: httpx.Request) -> None:
        pass

    @abstractmethod
    def response_hook(self, response: httpx.Response) -> None:
        pass


class HTTPXClient(HTTPXBaseClient, httpx.Client):
    def request_hook(self, request: httpx.Request) -> None:
        if callable(HTTPXClient._request_hook):
            HTTPXClient._request_hook(request, self.request_id)

    def response_hook(self, response: httpx.Response) -> None:
        request_max_len = (
            self.request_max_len
            if self.request_max_len
            else HTTPXClient._request_max_len
        )
        response_max_len = (
            self.response_max_len
            if self.response_max_len
            else HTTPXClient._response_max_len
        )

        extra_data = {
            "request_id": self.request_id,
            "method": response.request.method,
            "url": response.request.url,
            "status_code": response.status_code,
            "request_data": str(response.request.content)[:request_max_len],
            "response_data": str(response.read())[:response_max_len],
            "headers": dict(response.request.headers),
        }

        if callable(HTTPXClient._response_hook):
            HTTPXClient._response_hook(response, extra_data)

        get_apicall_logger(
            file_path=HTTPXClient._log_path,
            log_type=HTTPXClient._log_type,
            extra_data=extra_data,
        )


class HTTPXAsyncClient(HTTPXBaseClient, httpx.AsyncClient):
    _request_hook: typing.Callable[..., typing.Coroutine] = None
    _response_hook: typing.Callable[..., typing.Coroutine] = None

    async def request_hook(self, request: httpx.Request) -> None:
        if callable(HTTPXAsyncClient._request_hook):
            HTTPXAsyncClient._request_hook(request, self.request_id)

    async def response_hook(self, response: httpx.Response) -> None:
        request_max_len = (
            self.request_max_len
            if self.request_max_len
            else HTTPXClient._request_max_len
        )
        response_max_len = (
            self.response_max_len
            if self.response_max_len
            else HTTPXClient._response_max_len
        )

        extra_data = {
            "request_id": self.request_id,
            "method": response.request.method,
            "url": response.request.url,
            "status_code": response.status_code,
            "request_data": str(response.request.content)[:request_max_len],
            "response_data": str(await response.aread())[:response_max_len],
            "headers": dict(response.request.headers),
        }

        if callable(HTTPXAsyncClient._response_hook):
            HTTPXAsyncClient._response_hook(response, extra_data)

        get_apicall_logger(
            file_path=HTTPXClient._log_path,
            log_type=HTTPXClient._log_type,
            extra_data=extra_data,
        )


class HTTPXLogger:
    def __init__(
        self,
        request_hook: typing.Union[
            typing.Callable, typing.Callable[..., typing.Coroutine]
        ] = None,
        response_hook: typing.Union[
            typing.Callable, typing.Callable[..., typing.Coroutine]
        ] = None,
        sync_client: bool = True,
        async_client: bool = True,
        request_max_len: int = 5000,
        response_max_len: int = 5000,
        log_path: str = LogPathEnum.APICALL,
        log_type: LogTypeEnum = LogTypeEnum.FILE,
    ):
        if sync_client:
            HTTPXClient._request_hook = request_hook
            HTTPXClient._response_hook = response_hook
            HTTPXClient._request_max_len = request_max_len
            HTTPXClient._response_max_len = response_max_len
            HTTPXClient._log_path = log_path
            HTTPXClient._log_type = log_type
            httpx.Client = HTTPXClient

        if async_client:
            HTTPXAsyncClient._request_hook = request_hook
            HTTPXAsyncClient._response_hook = response_hook
            HTTPXAsyncClient._request_max_len = request_max_len
            HTTPXAsyncClient._response_max_len = response_max_len
            HTTPXAsyncClient._log_path = log_path
            HTTPXAsyncClient._log_type = log_type
            httpx.AsyncClient = HTTPXAsyncClient
