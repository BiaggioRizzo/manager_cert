from fastapi import HTTPException
from fastapi.responses import JSONResponse


########## ERROR 4XX ##########

class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Não encontrado"):
        super().__init__(status_code=404, detail=detail)

class BadRequestError(HTTPException):
    def __init__(self, detail: str = "Requisição Inválida"):
        super().__init__(status_code=400, detail=detail)
        
async def not_found_error_handler(request, exc: NotFoundError):
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)

async def bad_request_error_handler(request, exc: BadRequestError):
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)

########## ERROR 5XX ##########

class InternalServerError(HTTPException):
    def __init__(self, detail: str = "Erro interno no processamento da requisição"):
        super().__init__(status_code=500, detail=detail)

class BadGatewayError(HTTPException):
    def __init__(self, detail: str = "Erro interno no processamento da requisição"):
        super().__init__(status_code=502, detail=detail)

async def internal_server_error_handler(request, exc: InternalServerError):
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)

async def bad_gateway_error_handler(request, exc: BadGatewayError):
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)