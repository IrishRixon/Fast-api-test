from typing import List, Optional
from pydantic import Field, BaseModel

class AirBnbSchema(BaseModel): 
    id: str = Field(alias="_id")
    name: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    house_rules: Optional[str] = None
    property_type: Optional[str] = None
    room_type: Optional[str] = None
    minimum_nights: Optional[str] = None
    maximum_nights: Optional[str] = None
    price: Optional[float] = None
    weekly_price: Optional[float] = None
    monthly_price: Optional[float] = None
    cleaning_fee: Optional[float] = None

class PaginatedAirbnbResponse(BaseModel):
    data: List[AirBnbSchema]
    total_count: int

class AirBnbUpdate(BaseModel): 
    name: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    house_rules: Optional[str] = None
    property_type: Optional[str] = None
    room_type: Optional[str] = None
    minimum_nights: Optional[str] = None
    maximum_nights: Optional[str] = None
    price: Optional[float] = None
    weekly_price: Optional[float] = None
    monthly_price: Optional[float] = None
    cleaning_fee: Optional[float] = None

class AirBnbSchemaCreate(BaseModel): 
    name: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    house_rules: Optional[str] = None
    property_type: Optional[str] = None
    room_type: Optional[str] = None
    minimum_nights: Optional[str] = None
    maximum_nights: Optional[str] = None
    price: Optional[float] = None
    weekly_price: Optional[float] = None
    monthly_price: Optional[float] = None
    cleaning_fee: Optional[float] = None