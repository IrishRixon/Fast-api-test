from bson import Decimal128
from motor.core import AgnosticClientSession
from typing import Optional
from typing import Dict
from typing import List
from typing import Tuple
from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

class AirBnbModel(): 
    collection_name = "listingsAndReviews"

    def __init__(self, db: AsyncIOMotorDatabase): 
        self.collection = db[self.collection_name]

    def _convert_objectids_to_str(self, doc: Any) -> Any:
        if isinstance(doc, list):
            return [self._convert_objectids_to_str(i) for i in doc]
        if isinstance(doc, dict):
            return {k: self._convert_objectids_to_str(v) for k, v in doc.items()}
        if isinstance(doc, ObjectId):
            return str(doc)
        if isinstance(doc, Decimal128):
            return float(doc.to_decimal())
        return doc        

    async def get_airbnb_paginated(self, limit: int = 10, skip: int = 0, session: Optional[AgnosticClientSession] = None) -> Tuple[List[Dict[str, Any]], int]: 
        total_count = await self.collection.count_documents({}, session=session)
        
        docs = await self.collection.aggregate([
            {"$skip": skip},
            {"$limit": limit}
        ], session=session).to_list(limit)

        result = [self._convert_objectids_to_str(doc) for doc in docs]

        return (result, total_count)




        