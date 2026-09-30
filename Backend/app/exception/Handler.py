from starlette.requests import Request
from starlette.responses import JSONResponse

from app.exception.CustomException import CustomException


async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message,"success": True,"data":None})