from fastapi import FastAPI
from fastapi_and_logging.enums import LogTypeEnum
from fastapi_and_logging.helpers import (
    log_builder, 
    get_request_data, 
    get_response_data,
)
from fastapi_and_logging.logging_route import LoggingRoute



class FastAPIIncomingLog:
    
    def __init__(
        self, 
        app: FastAPI,
        request_id_builder = None,
        log_builder = log_builder,
        get_request_data = get_request_data,
        get_response_data = get_response_data,
        response_max_len: int = 5000,
        log_path: str = "incoming.log",
        log_type: LogTypeEnum = LogTypeEnum.FILE,
    ) -> None:
        self.app = app
        LoggingRoute.response_max_len = response_max_len
        LoggingRoute.request_id_builder = request_id_builder
        LoggingRoute.get_request_data = get_request_data
        LoggingRoute.get_response_data = get_response_data
        LoggingRoute.log_builder = log_builder
        LoggingRoute.log_path = log_path
        LoggingRoute.log_type = log_type
        self.app.router.route_class = LoggingRoute