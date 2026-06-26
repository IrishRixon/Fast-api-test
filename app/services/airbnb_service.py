from app.models.schema.airbnb import AirBnbModel
from motor.motor_asyncio import AsyncIOMotorDatabase

class AirbnbService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.airbnb_model = AirBnbModel(db)

    async def get_airbnb_paginated(self, limit: int = 10, skip: int = 0):
       result, total_count = await self.airbnb_model.get_airbnb_paginated(limit=limit, skip=skip)

       return result, total_count