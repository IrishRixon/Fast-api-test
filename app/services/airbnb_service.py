from app.models.schema.airbnb_schema import AirBnbSchemaCreate
from app.models.schema.airbnb_schema import AirBnbSchema
from motor.core import AgnosticClientSession
from typing import Optional
from app.models.schema.airbnb_schema import AirBnbUpdate
from bson import ObjectId
from fastapi import HTTPException
from app.models.schema.airbnb import AirBnbModel
from motor.motor_asyncio import AsyncIOMotorDatabase

class AirbnBService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.airbnb_model = AirBnbModel(db)

    async def get_airbnb_paginated(self, limit: int = 10, skip: int = 0):
       result, total_count = await self.airbnb_model.get_airbnb_paginated(limit=limit, skip=skip)

       return result, total_count

    async def get_airbnb(self, id: ObjectId | str):
        res = await self.airbnb_model.get_by_id(id)
        if not res: 
            raise HTTPException(
                status_code=404,
                detail="Airbng not found"
            )
        return res

    async def update_airbnb(self, id: str, data: AirBnbUpdate): 
        return await self.airbnb_model.update_airbnb(id, data=data)

    async def delete_airbnb(self, id: str):
        return await self.airbnb_model.delete_airbnb(id)

    async def create_airbnb(self, data: AirBnbSchemaCreate):
        return await self.airbnb_model.create_airbnb(data)