from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join(str(l) for l in err['loc'])
        msg = err['msg']
        errors.append({
            "field": loc,
            "error": msg
        })
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Error de validación en los datos enviados",
            "errors": errors
        }
    ) 