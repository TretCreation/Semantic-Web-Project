from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.general import router
from uvicorn import run


app = FastAPI()
app.include_router(router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
