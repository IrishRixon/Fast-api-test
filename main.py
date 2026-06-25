from app.config.database import close_mongo_client
from app.config.database import get_db
from app.config.database import connect_to_mongodb
from contextlib import asynccontextmanager
from api import routing
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if not await connect_to_mongodb(): 
            print("❌ Failed to connect to mongoDB on startup")
        else: 
            db = await get_db()

        yield

    finally: 
        await close_mongo_client()
        print("Mongo DB connection has been closed")

app = routing(app=FastAPI(lifespan=lifespan))

