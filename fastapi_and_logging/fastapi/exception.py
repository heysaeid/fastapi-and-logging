import datetime
from typing import Callable

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from fastapi_and_logging.enums import LogPathEnum, LogTypeEnum
from fastapi_and_logging.logging import get_exception_logger


def get_exception_logger_default_values(
    request: Request,
    status_code: int,
    exc: Exception,
) -> dict:
    scope = request.scope
    return {
        "exception": exc.__class__.__name__,
        "error_time": str(datetime.datetime.now()),
        "request_id": request.state.request_id,
        "endpoint": scope.get("route").name,
        "path": scope.get("path"),
        "status_code": status_code,
    }


class ExceptionLogger:
    exception_handlers: dict[Exception, Callable] = {}

    def __init__(
        self,
        app: FastAPI,
        log_path: str = LogPathEnum.EXCEPTION,
        log_type: LogTypeEnum = LogTypeEnum.FILE,
        set_default_handlers: bool = True,
    ):
        self.app = app
        self.log_path = log_path
        self.log_type = log_type

        if set_default_handlers:
            self.add_default_exception_handlers()

    async def unhandled_exception_handler(
        self,
        request: Request,
        exc: Exception,
    ):
        get_exception_logger(
            file_path=self.log_path,
            log_type=self.log_type,
            extra_data={
                "error_message": str(exc),
                **get_exception_logger_default_values(
                    request=request,
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    exc=exc,
                ),
            },
        )
        return JSONResponse(
            {
                "detail": "An unexpected error occurred",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    async def handle_http_exception(
        self, request: Request, exc: HTTPException
    ):
        get_exception_logger(
            file_path=self.log_path,
            log_type=self.log_type,
            extra_data={
                "error_message": exc.detail,
                **get_exception_logger_default_values(
                    request=request,
                    status_code=exc.status_code,
                    exc=exc,
                ),
            },
        )
        return JSONResponse(
            {"detail": exc.detail}, status_code=exc.status_code
        )

    def add_exception_handler(
        self,
        exception_class: HTTPException,
        handler: Callable,
    ):
        ExceptionLogger.exception_handlers[exception_class.__name__] = handler
        self.app.add_exception_handler(exception_class, handler)

    def add_default_exception_handlers(
        self,
        unhandled_exception: bool = True,
        http_exception: bool = True,
    ) -> None:
        if unhandled_exception:
            self.add_exception_handler(
                Exception, self.unhandled_exception_handler
            )

        if http_exception:
            self.add_exception_handler(
                HTTPException, self.handle_http_exception
            )
