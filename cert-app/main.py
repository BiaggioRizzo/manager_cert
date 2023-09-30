import uvicorn
from fastapi import FastAPI
from routers import manager_routers
import exceptions.exceptions as exception

app = FastAPI()

app.include_router(manager_routers.router)

app.add_exception_handler(exception.NotFoundError, exception.not_found_error_handler)
app.add_exception_handler(exception.BadRequestError, exception.bad_request_error_handler)
app.add_exception_handler(exception.InternalServerError, exception.internal_server_error_handler)
app.add_exception_handler(exception.BadGatewayError, exception.bad_gateway_error_handler)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7085)