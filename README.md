# fastapi-and-logging
![FastAPI And Logging](https://raw.githubusercontent.com/heysaeid/fastapi-and-logging/main/docs/img/Color%20logo%20with%20background.svg?token=GHSAT0AAAAAACKL66NW3EGUQNEBNWWN7XHSZK3JVAA)


FastAPI-and-Logging simplifies log handling, allowing for effective organization, tracking, and analysis of logs in FastAPI applications, aiding in debugging and issue resolution.


# Install
```
pip install fastapi-and-logging
```


# IncomiongLog

This `FastAPIIncomingLog` class is designed to log incoming system requests using FastAPI.

## Parameters:

- `app`: It is used to set route_class.
- `request_id_builder`: A function to build a request identifier, if specified(It uses uuid4 by default).
- `log_builder`: A function used to construct logs.
- `get_request_data`: A function used to retrieve request information.
- `get_response_data`: A function used to retrieve response information.
- `response_max_len`: The maximum length of a response stored in the log (default is 5000).
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
from fastapi_and_logging.helpers import get_request_data


async def customize_get_request_data(request: Request):
    # You can also use the output of the default function
    data = await get_request_data(request)
    return data
    
```

## `get_response_data`

This function handles the processing of response data.


```python
from fastapi import Response
from fastapi_and_logging.helpers import get_response_data


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
from fastapi_and_logging.helpers import log_builder


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