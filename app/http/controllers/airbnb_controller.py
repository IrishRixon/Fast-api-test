from app.models.schema.airbnb_schema import PaginatedAirbnbResponse
from typing import List
from app.models.schema.airbnb_schema import AirBnbSchema
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.encoders import jsonable_encoder
from fastapi import status
from fastapi.responses import JSONResponse
from app.services.airbnb_service import AirbnbService
from app.config.database import get_db
from fastapi import Depends
from pymongo.asynchronous.database import AsyncDatabase
from fastapi import APIRouter
router = APIRouter(tags=["Test AirBnb"])

@router.get("", response_model=PaginatedAirbnbResponse)
async def index(skip: int = 0, limit: int = 10, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        air_bnb_service = AirbnbService(db)
        air_bnb_data, total_count = await air_bnb_service.get_airbnb_paginated(skip=skip, limit=limit)

        # Validate raw MongoDB dicts through Pydantic schema to filter fields
        validated_data = [AirBnbSchema(**item) for item in air_bnb_data]

        return PaginatedAirbnbResponse(
            data=validated_data,
            total_count=total_count
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({"message": str(e)})
        )
