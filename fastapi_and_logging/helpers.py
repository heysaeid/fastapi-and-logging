import json
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from user_agents.parsers import UserAgent


async def get_request_data(request: Request):
    body = await request.body()
    if len(body) > 0:
        try:
            return json.dumps(await request.body())
        except Exception as e:
            return ""
    return ""
    
    
def get_response_data(response: Response) -> dict | str:
    response_max_len = 1000
    
    if not isinstance(response, StreamingResponse):
        body = response.body
        if len(body) < response_max_len:
            try:
                response_data = json.loads(response.body)
            except Exception as e:
                response_data = str(body)[response_max_len:]
        else:
            response_data = str(body)[response_max_len:]
    else:
        response_data = "StreamingResponse"
    
    return response_data


def log_builder(
    request: Request,
    response: Response,
    request_data: dict | str,
    response_data: dict | str,
    user_agent: UserAgent,
    start_time: int,
    end_time: int,
    duration: int,
):
    scope = request.scope
    return {
        "request_id": request.state.request_id,
        "endpoint": scope.get("route").name,
        "path": scope.get("path"),
        "status_code": response.status_code,
        "query": dict(request.query_params),
        "request": request_data,
        "response": response_data,
        "headers": dict(request.headers),
        "request_time": start_time,
        "response_time": end_time,
        "duration": duration,
        "browser": f"{user_agent.browser.family}:{user_agent.browser.version_string}",
        "os": f"{user_agent.os.family}:{user_agent.os.version_string}",
        "device": user_agent.device.family,
    }