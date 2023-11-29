from dotenv import dotenv_values
from fastapi import FastAPI
from pymongo import MongoClient
from routes import router as replays_router

config = dotenv_values(".env")

app = FastAPI(docs_url=None,
              redoc_url=None)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(host=config["HOSTNAME"],
                                     username=config["USERNAME"],
                                     password=config["PASSWORD"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Server version:", app.mongodb_client.server_info()["version"])
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(replays_router, tags=["stats"], prefix="/stats")
