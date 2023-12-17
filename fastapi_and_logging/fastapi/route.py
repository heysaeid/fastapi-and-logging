import time, uuid
from typing import Callable, Coroutine
from fastapi import Request, Response
from fastapi.routing import APIRoute
from user_agents.parsers import parse
from fastapi_and_logging.enums import LogTypeEnum
from fastapi_and_logging.fastapi.exception import ExceptionLogger
from fastapi_and_logging.logging import get_incoming_logger


class LoggingRoute(APIRoute): 
    response_max_len: int
    request_id_builder: Callable
    get_request_data: Callable[..., Coroutine]
    get_response_data: Callable
    log_builder: Callable
    log_path: str
    log_type: LogTypeEnum
            
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        
        async def custom_route_handler(request: Request) -> Response:
            request_id = LoggingRoute.request_id_builder() if LoggingRoute.request_id_builder else str(uuid.uuid4())
            request.state.request_id = request_id
            start_time = time.time()
            
            try:
                response = await original_route_handler(request)
            except Exception as exc:
                exc_name = exc.__class__.__name__
                handler = ExceptionLogger.exception_handlers.get(exc_name) or ExceptionLogger.exception_handlers.get("Exception")
                if handler:
                    response = await handler(request, exc)
                else:
                    raise exc
                
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            
            user_agent = parse(request.headers["user-agent"])
            log_dict = LoggingRoute.log_builder(
                request = request,
                request_data = await LoggingRoute.get_request_data(request),
                response = response,
                response_data = LoggingRoute.get_response_data(response),
                user_agent = user_agent,
                start_time = start_time,
                end_time = end_time,
                duration = duration,
            )
            get_incoming_logger(
                file_path=LoggingRoute.log_path,
                log_type=LoggingRoute.log_type,
                extra_data=log_dict, 
            )
            return response
        
        return custom_route_handler