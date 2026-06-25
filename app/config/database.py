import logging
import logging
from pymongo.errors import ConnectionFailure
from app.config.credentials import Database
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = Database.url
DB_NAME = Database.db_name
client = None
db_instance = None

async def connect_to_mongodb():
    try:
        global client, db_instance

        if client is not None: 
            return True

        client = AsyncIOMotorClient(
            MONGODB_URI,
            maxPoolSize=10,  # Increased for transactions
            minPoolSize=2,
            connectTimeoutMS=5000,
            serverSelectionTimeoutMS=5000,
            retryWrites=True,  # Essential for transactions
            w="majority",  # Write concern for ACID
        )
        db_instance = client[DB_NAME]

        await db_instance.command({"ping": 1})
        print("✅ MongoDB connection established with transaction support")
        return True

    except ConnectionFailure as e:
        logging.error(f"❌ MongoDB connection failed: {str(e)}")
        client = None
        db_instance = None
        return False
    except Exception as e: 
        logging.exception(f"❌ An unexpected error occurred: {str(e)}")
        client = None
        db_instance = None
        return False
    
async def get_db():
    """Get database instance with connection verification"""
    if db_instance is None:
        if not connect_to_mongodb():
            raise RuntimeError("Database connection is not availble")
            
    try:
        await db_instance.command({"ping": 1})
        return db_instance
    except ConnectionFailure:
        print("MongoDb connectionlost, attempting to reconnect ...")
        if await connect_to_mongodb():
            return db_instance
        raise RuntimeError("Failed to reconnect to database")
    

async def close_mongo_client():
    global client, db_instance
    if client: 
        client.close()
        client = None
        db_instance = None
        print("✅ MongoDB connection closed")