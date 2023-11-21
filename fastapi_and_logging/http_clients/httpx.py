from abc import ABC, abstractmethod
import typing
import httpx
from fastapi_and_logging.logging import get_apicall_logger


class HTTPXBaseClient(ABC):
    _request_hook: typing.Callable = None
    _response_hook: typing.Callable = None
    _request_max_len: int = None
    _response_max_len: int = None
    
    def __init__(
        self,
        request_id: typing.Any = None,
        request_max_len: int = _request_max_len,
        response_max_len: int = _response_max_len,
        *args, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        breakpoint()
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
        request_max_len = self.request_max_len if self.request_max_len else HTTPXClient._request_max_len
        response_max_len = self.response_max_len if self.response_max_len else HTTPXClient._response_max_len
        
        extra_data = {
            "request_id": self.request_id,
            "method": response.request.method,
            "url": response.request.url,
            "status_code": response.status_code,
            "request_data": str(response.request.content)[:request_max_len],
            "response_data": str(response.read())[:response_max_len],
        }
        
        if callable(HTTPXClient._response_hook):
            HTTPXClient._response_hook(response, extra_data)
        
        get_apicall_logger(extra_data=extra_data)


class HTTPXAsyncClient(HTTPXBaseClient, httpx.AsyncClient):
    
    def request_hook(self, request: httpx.Request) -> None:
        if callable(HTTPXAsyncClient._request_hook):
            HTTPXAsyncClient._request_hook(request, self.request_id)
    
    def response_hook(self, response: httpx.Response) -> None:
        request_max_len = self.request_max_len if self.request_max_len else HTTPXClient._request_max_len
        response_max_len = self.response_max_len if self.response_max_len else HTTPXClient._response_max_len
        
        extra_data = {
            "request_id": self.request_id,
            "method": response.request.method,
            "url": response.request.url,
            "status_code": response.status_code,
            "request_data": str(response.request.content)[:request_max_len],
            "response_data": str(response.read())[:response_max_len],
        }
        
        if callable(HTTPXAsyncClient._response_hook):
            HTTPXAsyncClient._response_hook(response, extra_data)
        
        get_apicall_logger(extra_data=extra_data)


class HTTPXLogger:
    
    def __init__(
        self,
        request_hook: typing.Callable = None, 
        response_hook: typing.Callable = None,
        sync_client: bool = True,
        async_client: bool = True,
        request_max_len: int = 5000,
        response_max_len: int = 5000,
    ):  
        if sync_client:
            HTTPXClient._request_hook = request_hook
            HTTPXClient._response_hook = response_hook
            HTTPXClient._request_max_len = request_max_len
            HTTPXClient._response_max_len = response_max_len
            httpx.Client = HTTPXClient
        
        if async_client:
            HTTPXAsyncClient._request_hook = request_hook
            HTTPXAsyncClient._response_hook = response_hook
            HTTPXAsyncClient._request_max_len = request_max_len
            HTTPXAsyncClient._response_max_len = response_max_len
            httpx.AsyncClient = HTTPXAsyncClient