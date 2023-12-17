from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi_and_logging.enums import LogTypeEnum
from fastapi_and_logging.logging import get_exception_logger


def get_exception_logger_default_values(request: Request) -> dict:
    scope = request.scope
    return {
        "request_id": request.state.request_id,
        "endpoint": scope.get("route").name,
        "path": scope.get("path"),
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

class ExceptionLogger:
    
    def __init__(
        self, 
        app: FastAPI,
        log_path: str = "error.log",
        log_type: LogTypeEnum = LogTypeEnum.FILE,
    ):
        self.log_path = log_path
        self.log_type = log_type
        app.add_exception_handler(Exception, self.unhandled_exception_handler)
        
    async def unhandled_exception_handler(
        self,
        request: Request, 
        exc: Exception,
    ):
        get_exception_logger(
            file_path = self.log_path,
            log_type = self.log_type,
            extra_data = {
                "error_message": str(exc),
                **get_exception_logger_default_values(request),
            }
        )
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {"error_message": "Internal Server Error"},
        )