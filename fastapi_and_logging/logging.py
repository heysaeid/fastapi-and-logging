import json
from loguru import logger
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
    extra_data: dict = {},
    message: str = "Incoming Request",
    format = incoming_formatter,
    log_type: LogTypeEnum = LogTypeEnum.FILE,
):
    if log_type == LogTypeEnum.FILE:     
        incoming_logger = create_logger(
            name = "incoming",
            file_path = file_path,
            enqueue = enqueue,
            format = format,
        )
        incoming_logger.bind(data=extra_data).info(message)
    elif log_type == LogTypeEnum.CONSOLE:
        logger.info({"message":message, "data":extra_data})

def apicall_formatter(record: dict):
    record["extra"]["serialized"] = json.dumps(record["extra"]["data"], default=str)
    return "{extra[serialized]}\n"

def get_apicall_logger(
    file_path: str = "apicall.log", 
    enqueue: bool = True, 
    extra_data: dict = {},
    message: str = "APICall Request",
    format = apicall_formatter,
    log_type: LogTypeEnum = LogTypeEnum.FILE,
):
    if log_type == LogTypeEnum.FILE:     
        apicall_logger = create_logger(
            name = "apicall",
            file_path = file_path,
            enqueue = enqueue,
            format = format,
        )
        apicall_logger.bind(data=extra_data).info(message)
    elif log_type == LogTypeEnum.CONSOLE:
        logger.info({"message":message, "data":extra_data})
        
def error_formatter(record: dict):
    record["extra"]["serialized"] = json.dumps(record["extra"]["data"], default=str)
    return "{extra[serialized]}\n"

def get_error_logger(
    file_path: str = "error.log", 
    enqueue: bool = True, 
    extra_data: dict = {},
    message: str = "Error",
    format = error_formatter,
    log_type: LogTypeEnum = LogTypeEnum.FILE,
):
    if log_type == LogTypeEnum.FILE:     
        error_logger = create_logger(
            name = "error",
            file_path = file_path,
            enqueue = enqueue,
            format = format,
        )
        error_logger.bind(data=extra_data).info(message)
    elif log_type == LogTypeEnum.CONSOLE:
        logger.info({"message":message, "data":extra_data})