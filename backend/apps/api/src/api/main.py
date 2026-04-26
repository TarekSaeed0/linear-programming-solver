import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.exceptions import CoreError, InvalidProblemError, NotSolvableError

from api.routers import solve

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(InvalidProblemError)
async def invalid_problem_exception_handler(
    _request: Request, exc: InvalidProblemError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )


@app.exception_handler(NotSolvableError)
async def not_solvable_exception_handler(
    _request: Request, exc: NotSolvableError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)}
    )


@app.exception_handler(CoreError)
async def core_exception_handler(_request: Request, exc: CoreError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    _request: Request, _exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=500, content={"detail": "An unexpected error occurred"}
    )


app.include_router(solve.router)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
