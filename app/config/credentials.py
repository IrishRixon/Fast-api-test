import os
from dotenv import load_dotenv

load_dotenv()
class Database: 
    url = os.getenv("MONGODB_URI")
    db_name = os.getenv("DB_NAME")