import json
from loguru import FormatFunction, logger
from fastapi_and_logging.enums import LogTypeEnum


def create_logger(name: str, file_path: str, **kwargs):
    logger.remove()
    logger.bind(name=name)
    logger.add(file_path, **kwargs)
    return logger

def incoming_formatter(record: dict):
    record["extra"]["serialized"] = json.dumps(record["extra"]["data"], default=str)
    return "{extra[serialized]}\n"

def get_incoming_logger(
    file_path: str = "incoming.log", 
    enqueue: bool = True, 
    bind_data: dict = {},
    message: str = "Incoming request",
    format: FormatFunction = incoming_formatter,
    log_type: LogTypeEnum = LogTypeEnum.FILE,
):
    if log_type == LogTypeEnum.FILE:     
        incoming_logger = create_logger(
            name = "incoming",
            file_path = file_path,
            enqueue = enqueue,
            format = format,
        )
        incoming_logger.bind(data=bind_data).info(message)
    elif log_type == LogTypeEnum.CONSOLE:
        logger.bind(**bind_data).info(message)