import json
from loguru import logger
from fastapi_and_logging.enums import LogPathEnum, LogTypeEnum


def create_logger(name: str, file_path: str, **kwargs):
    logger.remove()
    logger.bind(name=name)
    logger.add(file_path, **kwargs)
    return logger

def incoming_formatter(record: dict):
    record["extra"]["serialized"] = json.dumps(record["extra"]["data"], default=str)
    return "{extra[serialized]}\n"

def get_incoming_logger(
    file_path: str = LogPathEnum.INCOMING, 
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
    file_path: str = LogPathEnum.APICALL, 
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
        
def exception_formatter(record: dict):
    record["extra"]["serialized"] = json.dumps(record["extra"]["data"], default=str)
    return "{extra[serialized]}\n"

def get_exception_logger(
    file_path: str = LogPathEnum.EXCEPTION, 
    enqueue: bool = True, 
    extra_data: dict = {},
    message: str = "Exception",
    format = exception_formatter,
    log_type: LogTypeEnum = LogTypeEnum.FILE,
):
    if log_type == LogTypeEnum.FILE:     
        error_logger = create_logger(
            name = "exception.log",
            file_path = file_path,
            enqueue = enqueue,
            format = format,
        )
        error_logger.bind(data=extra_data).info(message)
    elif log_type == LogTypeEnum.CONSOLE:
        logger.info({"message":message, "data":extra_data})