import uvicorn

from fastapi import FastAPI

from lib.payme.endpoints import router

app = FastAPI()
app.include_router(router, prefix="/api/payme")


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000
    )
