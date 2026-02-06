from typing import Literal, Optional, Any
from fastapi.responses import JSONResponse


def json_response(
    status: Literal["success", "error"],
    message: str,
    status_code: int = 200,
    *,
    data: Optional[Any] = None,
    error: Optional[Any] = None,
) -> JSONResponse:
    response = {
        "status": status,
        "message": message,
    }

    if data is not None:
        response["data"] = data

    if error is not None:
        response["error"] = error

    return JSONResponse(response, status_code)


def error(message: str, error: Any = None, status_code: int = 400):
    return json_response("error", message, status_code, error=error)


def success(message: str, data: Any = None, status_code: int = 200):
    return json_response("success", message, status_code, data=data)