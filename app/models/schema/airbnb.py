from app.models.schema.airbnb_schema import AirBnbSchemaCreate
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.models.schema.airbnb_schema import AirBnbSchema
from fastapi import HTTPException
from app.models.schema.airbnb_schema import AirBnbUpdate
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


    async def get_by_id(self, id: ObjectId, session: Optional[AgnosticClientSession] = None) -> Optional[Dict[str, Any]]: 
        res = await self.collection.find_one({"_id": id}, session=session)
        return self._convert_objectids_to_str(res) if res else None
        
    async def update_airbnb(self, id: str, data: AirBnbUpdate , session: Optional[AgnosticClientSession] = None) -> Dict[str, Any]:
        update_data = {k: v for k, v in data.model_dump().items() if v is not None }
        res = await self.collection.find_one_and_update({"_id": id}, {"$set": update_data}, session=session)

        if not res:
            raise HTTPException(status_code=404, detail="Airbnb not found")
        return self._convert_objectids_to_str(res)

    async def delete_airbnb(self, id: str, session: Optional[AgnosticClientSession] = None) -> bool:
        res = await self.collection.delete_one({"_id": id}, session=session)
        return res.deleted_count > 0

    async def create_airbnb(self, data: AirBnbSchemaCreate, session: Optional[AgnosticClientSession] = None) -> bool:
        created_data = data.model_dump()
        res = await self.collection.insert_one(created_data, session=session)
        
        if not res.acknowledged:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create"
            )

        return True