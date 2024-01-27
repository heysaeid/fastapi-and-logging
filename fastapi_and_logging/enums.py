from strenum import StrEnum


class LogTypeEnum(StrEnum):
    FILE = "file"
    CONSOLE = "console"


class LogPathEnum(StrEnum):
    INCOMING = "incoming.log"
    APICALL = "apicall.log"
    EXCEPTION = "exception.log"
