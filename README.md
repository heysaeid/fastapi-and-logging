# fastapi-and-logging
![FastAPI And Logging](https://raw.githubusercontent.com/heysaeid/fastapi-and-logging/main/docs/img/Color%20logo%20with%20background.svg)

[![Package version](https://img.shields.io/pypi/v/fastapi-and-logging?color=%2334D058&label=pypi%20package)](https://pypi.org/project/fastapi-and-logging/)
[![Downloads](https://img.shields.io/pypi/dm/fastapi-and-logging)](https://pypi.org/project/fastapi-and-logging/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/fastapi-and-logging.svg?color=%2334D058)](https://pypi.org/project/fastapi-and-logging/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/heysaeid/fastapi-and-logging/blob/master/LICENSE)

FastAPI-and-Logging simplifies log handling, allowing for effective organization, tracking, and analysis of logs in FastAPI applications, aiding in debugging and issue resolution.


Support for:
- Incoming Logger
- Exception Logger
- APICall Logger (HTTPX, AIOHttp, requests (coming soon...))
- Kafka (coming soon...)


# Install
```
pip install fastapi-and-logging
```


# Incomiong Logger

This `FastAPIIncomingLog` class is designed to log incoming system requests using FastAPI.

## Parameters:

- `app`: It is used to set route_class.
- `request_id_builder`: A function to build a request identifier, if specified(It uses uuid4 by default).
- `log_builder`: A function used to construct logs.
- `get_request_data`: A function used to retrieve request information.
- `get_response_data`: A function used to retrieve response information.
- `response_max_len`: The maximum length of a response stored in the log (default is 5000).
- `log_path (optional)`: Log file path.
- `log_type`: The type of logging, which can be one of various types (default is LogTypeEnum.FILE).

## How to Use:

To use this class, you can create an instance of it and set it as the `route_class` for your relevant Router in your FastAPI application.

```python
from fastapi import FastAPI
from fastapi_and_logging import FastAPIIncomingLog

app = FastAPI()
FastAPIIncomingLog(app)
```
# Customizing and Using Default Functions

The provided default functions (`get_request_data`, `get_response_data`, and `log_builder`) serve as customizable components for the `FastAPIIncomingLog` class. Here's how you can customize and use them:

## `get_request_data`

This function is responsible for extracting and formatting request data.

```python
from fastapi_and_logging import Request
from fastapi_and_logging.fastapi import get_request_data


async def customize_get_request_data(request: Request):
    # You can also use the output of the default function
    data = await get_request_data(request)
    return data
```

## `get_response_data`

This function handles the processing of response data.


```python
from fastapi import Response
from fastapi_and_logging.fastapi import get_response_data


def customize_get_response_data(response: Response) -> dict | str:
    # You can also use the output of the default function
    data = get_response_data(response)
    return data
```

## `log_builder`

The log_builder function constructs the log data based on various parameters.


```python
from fastapi import Request, Response
from user_agents.parsers import UserAgent
from fastapi_and_logging.fastapi import log_builder


def customize_log_builder(
    request: Request,
    response: Response,
    request_data: dict | str,
    response_data: dict | str,
    user_agent: UserAgent,
    start_time: int,
    end_time: int,
    duration: int,
):
    # You can also use the output of the default function
    data = log_builder(**)
    return data
```

# Exception Logger
To log all exceptions, simply use the ExceptionLogger class.

## Parameters:
- `app`: It is used to add exception handlers.
- `log_path (optional)`: Log file path.
- `log_type`: The type of logging, which can be one of various types (default is LogTypeEnum.FILE).
- `set_default_handlers`: Whether to set default exception handlers (default: True).

## How to Use:
```python
from fastapi import FastAPI
from fastapi_and_logging import ExceptionLogger

app = FastAPI()
ExceptionLogger(app)
```

You can also add your own exception handlers as follows:
```python
from fastapi import FastAPI, Request
from fastapi_and_logging import ExceptionLogger

app = FastAPI(debug=False)
exception_logger = ExceptionLogger(app=app)

async def test_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        content={"message": "Internal Server Error"},
    )

exception_logger.add_exception_handler(Exception, test_exception_handler)
```



# APICall Logger

**Note**: Currently it only supports httpx and aiohttp.

## HTTPXLogger
You can easily log all apicalls using httpx by adding the HTTPXLogger class.

### Parameters:

- `request_hook (optional)`: A callable object that serves as a hook for capturing and logging HTTP requests. It takes a single parameter, the request object, and does not return any value. Defaults to None..
- `response_hook (optional)`: A callable object that acts as a hook to capture and log HTTP responses. Any value returned will be logged.
- `sync_client (optional)`: A boolean value indicating whether the logging functionality should be applied to synchronous HTTP clients. If True, the hooks and configuration will be set for synchronous clients. Defaults to True.
- `async_client (optional)`: A boolean value indicating whether the logging functionality should be applied to asynchronous HTTP clients. If True, the hooks and configuration will be set for asynchronous clients. Defaults to True.
- `request_max_len (optional)`: An integer specifying the maximum length of the request body to be logged. If the request body exceeds this length, it will be truncated. Defaults to 5000 .
- `response_max_len (optional)`: An integer specifying the maximum length of the response body to be logged. If the response body exceeds this length, it will be truncated. Defaults to 5000.
- `log_path (optional)`: Log file path.
- `log_type (optional)`: Specifies the type of logging, currently it takes two values: console and file.

### How to Use:

```python
from fastapi import FastAPI
import httpx
from fastapi_and_logging.http_clients import HTTPXLogger


app = FastAPI()
HTTPXLogger()


@app.get("/")
def index():
    with httpx.Client() as client:
        response = client.get("http://localhost:8000/path")
```


## AioHttpLogger
You can easily log all apicalls using httpx by adding the AioHttpLogger class.

### Parameters:

- `request_hook (optional)`: A callable object that serves as a hook for capturing and logging HTTP requests. It takes a single parameter, the request object, and does not return any value. Defaults to None..
- `response_hook (optional)`: A callable object that acts as a hook to capture and log HTTP responses. Any value returned will be logged.
- `request_max_len (optional)`: An integer specifying the maximum length of the request body to be logged. If the request body exceeds this length, it will be truncated. Defaults to 5000 .
- `response_max_len (optional)`: An integer specifying the maximum length of the response body to be logged. If the response body exceeds this length, it will be truncated. Defaults to 5000.
- `log_path (optional)`: Log file path.
- `log_type (optional)`: Specifies the type of logging, currently it takes two values: console and file.

### How to Use:

```python
from fastapi import FastAPI
import httpx
from fastapi_and_logging.http_clients import AioHttpLogger


app = FastAPI()
AioHttpLogger()


@app.get("/")
def index():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://localhost:8000/path", 
        ) as response:
            ...
```

To be able to have the request data or request ID associated with the incoming log in the apicall log, you need to follow the following steps. Additionally, you can send your desired parameters to log in the trace_request_ctx as well.
```python
from fastapi import Request


@app.get("/")
def index(request: Request):
    payload = {"name": "FastAPI And Logging"}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/path",
            json = payload,
            trace_request_ctx = {
                "request_id": request.state.request_id, 
                "request_data": payload,
            } 
        ) as response:
            ...
```