import typing

import aiohttp
import wrapt

from fastapi_and_logging.enums import LogPathEnum, LogTypeEnum
from fastapi_and_logging.logging import get_apicall_logger


class AioHttpLogger:
    def __init__(
        self,
        request_hook: typing.Optional[
            typing.Callable[..., typing.Coroutine]
        ] = None,
        response_hook: typing.Optional[
            typing.Callable[..., typing.Coroutine]
        ] = None,
        request_max_len: int = 5000,
        response_max_len: int = 5000,
        log_path: str = LogPathEnum.APICALL,
        log_type: LogTypeEnum = LogTypeEnum.FILE,
    ) -> None:
        self.request_hook = request_hook or self.default_request_hook
        self.response_hook = response_hook or self.default_response_hook
        self.request_max_len = request_max_len
        self.response_max_len = response_max_len
        self.log_path = log_path
        self.log_type = log_type
        wrapt.wrap_function_wrapper(
            aiohttp.ClientSession, "__init__", self.init
        )

    def init(self, wrapped, instance, args, kwargs):
        trace_config = aiohttp.TraceConfig()
        trace_config.on_request_start.append(self.request_hook)
        trace_config.on_request_end.append(self.response_hook)
        kwargs["trace_configs"] = [trace_config]
        wrapped(*args, **kwargs)

    async def default_request_hook(self, session, trace_config_ctx, params):
        ...

    async def default_response_hook(self, session, trace_config_ctx, params):
        response = params.response
        request_data, request_id = {}, {}
        if trace_config_ctx.trace_request_ctx:
            request_data = trace_config_ctx.trace_request_ctx.pop(
                "request_data", None
            )
            request_id = trace_config_ctx.trace_request_ctx.pop(
                "request_id",
            )
        response_data = await response.read()
        extra_data = {
            "request_id": request_id,
            "method": response.method,
            "url": str(response.url),
            "status_code": response.status,
            "request_data": self._get_data(request_data, self.request_max_len),
            "response_data": self._get_data(
                response_data, self.response_max_len
            ),
            "trace_request_ctx": trace_config_ctx.trace_request_ctx,
            "headers": dict(params.headers),
        }

        get_apicall_logger(
            file_path=self.log_path,
            log_type=self.log_type,
            extra_data=extra_data,
        )

    def _get_data(self, data: typing.Any, max_length: int):
        if data:
            data_length = len(str(data))
            if data_length > max_length:
                return str(data)[:max_length]
        return data
