import os
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from starlette.responses import JSONResponse

from routes import router as replays_router

app = FastAPI(docs_url=None,
              redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"{os.environ['CORS_ORIGIN']}",
    ],
)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(host=os.environ["HOSTNAME"],
                                     username=os.environ["USERNAME"],
                                     password=os.environ["PASSWORD"])
    app.database = app.mongodb_client[os.environ["DB_NAME"]]
    print("Server version:", app.mongodb_client.server_info()["version"])
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=jsonable_encoder({"code": 500, "msg": "Internal Server Error"}))


app.include_router(replays_router, tags=["stats"], prefix="/stats")
