from app.models.schema.airbnb_schema import AirBnbSchemaCreate
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.status import HTTP_404_NOT_FOUND
from app.models.schema.airbnb_schema import AirBnbUpdate
from fastapi import HTTPException
from bson import ObjectId
from app.models.schema.airbnb_schema import PaginatedAirbnbResponse
from typing import List
from app.models.schema.airbnb_schema import AirBnbSchema
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.encoders import jsonable_encoder
from fastapi import status
from fastapi.responses import JSONResponse
from app.services.airbnb_service import AirbnBService
from app.config.database import get_db
from fastapi import Depends
from pymongo.asynchronous.database import AsyncDatabase
from fastapi import APIRouter
router = APIRouter(tags=["Test AirBnb"])

@router.get("", response_model=PaginatedAirbnbResponse)
async def index(skip: int = 0, limit: int = 10, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        air_bnb_service = AirbnBService(db)
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

@router.get("/{id}", response_model=AirBnbSchema)
async def show(id: str, db: AsyncIOMotorDatabase = Depends(get_db)): 
    try: 
        airbnb_service = AirbnBService(db)
        res = await airbnb_service.get_airbnb(id)
 
        return AirBnbSchema(**res)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/{id}", response_model=AirBnbSchema, dependencies=[Depends(get_db)])
async def update(
    id: str,
    data: AirBnbUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
): 
    try:
        airbnb_service = AirbnBService(db)
        res = await airbnb_service.update_airbnb(id=id, data=data)
        return res

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{id}")
async def delete(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)  
): 
    try:
        airbnb_service = AirbnBService(db)
        res = await airbnb_service.delete_airbnb(id)

        if not res:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Airbnb not found")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({"message": "Airbnb deleted successfully"})
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("")
async def post(
    data: AirBnbSchemaCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    try:
        airbnb_service = AirbnBService(db)
        res = await airbnb_service.create_airbnb(data)

        if not res: 
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="failed to create air bnb")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({"message": "Airbnb created successfully"})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))